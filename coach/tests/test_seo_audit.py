import sys, json, pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import seo_audit


class TestCheckMeta:
    def test_fetch_soup(self):
        result, resp = seo_audit.fetch_soup("https://example.com")
        assert result is not None
        assert resp.status_code == 200

    def test_check_meta_found(self):
        soup, _ = seo_audit.fetch_soup("https://example.com")
        meta = seo_audit.check_meta(soup)
        assert "title" in meta
        assert meta["title"] == "Example Domain"

    def test_check_meta_missing(self):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup("<html><head></head><body></body></html>", "lxml")
        meta = seo_audit.check_meta(soup)
        assert meta["title"] is None
        assert meta["description"] is None
        assert meta["canonical"] is None

    def test_check_headings(self):
        soup, _ = seo_audit.fetch_soup("https://example.com")
        h = seo_audit.check_headings(soup)
        assert h["h1_count"] == 1
        assert "Example Domain" in h["h1_tags"][0]


class TestCheckInfra:
    def test_check_robots(self):
        result = seo_audit.check_robots("https://example.com")
        assert result["status"] == "ok" or result["status"] == "missing"

    def test_check_sitemap(self):
        result = seo_audit.check_sitemap("https://example.com")
        assert "status" in result

    def test_categorize_url(self):
        assert seo_audit.categorize_url("https://x.com/blog/post", "x.com") == "blog"
        assert seo_audit.categorize_url("https://x.com/products/foo", "x.com") == "product"
        assert seo_audit.categorize_url("https://x.com/", "x.com") == "home"
        assert seo_audit.categorize_url("https://x.com/about", "x.com") == "page"


class TestCheckContent:
    def test_check_images_empty(self):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup("<html><body></body></html>", "lxml")
        imgs = seo_audit.check_images(soup, "https://x.com")
        assert imgs["total"] == 0
        assert imgs["missing_alt"] == 0

    def test_check_content(self):
        soup, _ = seo_audit.fetch_soup("https://example.com")
        c = seo_audit.check_content(soup)
        assert c["word_count"] > 0
        assert c["paragraph_count"] > 0

    def test_check_page_quality(self):
        soup, _ = seo_audit.fetch_soup("https://example.com")
        q = seo_audit.check_page_quality(soup)
        assert "no_products" in q
        assert "coming_soon" in q
        assert "placeholder_lorem" in q


class TestLinks:
    def test_check_internal_links(self):
        soup, _ = seo_audit.fetch_soup("https://example.com")
        links = seo_audit.check_internal_links(soup, "example.com", "https://example.com")
        assert "internal" in links
        assert "external" in links

    def test_check_schema(self):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup('<html><body><script type="application/ld+json">{"@type":"WebSite","url":"https://x.com"}</script></body></html>', "lxml")
        s = seo_audit.check_schema(soup)
        assert s["present"] is True
        assert s["count"] == 1
        assert "WebSite" in s["types"]


class TestSocial:
    def test_check_social_tags(self):
        soup, _ = seo_audit.fetch_soup("https://example.com")
        social = seo_audit.check_social_tags(soup)
        assert "og" in social
        assert "twitter" in social


class TestIssueGeneration:
    def test_add_meta_issues_title_missing(self):
        issues = []
        seo_audit._add_meta_issues({"title": None}, issues)
        assert any(i["issue"] == "Missing <title> tag" for i in issues)

    def test_add_meta_issues_title_short(self):
        issues = []
        seo_audit._add_meta_issues({"title": "Hi", "title_length": 2}, issues)
        assert any("Title too short" in i["issue"] for i in issues)

    def test_add_meta_issues_no_description(self):
        issues = []
        seo_audit._add_meta_issues({"title": "Fine Title Here", "title_length": 15, "description": None}, issues)
        assert any(i["issue"] == "Missing meta description" for i in issues)

    def test_add_heading_issues_no_h1(self):
        issues = []
        seo_audit._add_heading_issues({"h1_count": 0}, issues)
        assert any(i["issue"] == "No H1 tag on page" for i in issues)

    def test_add_heading_issues_multiple_h1(self):
        issues = []
        seo_audit._add_heading_issues({"h1_count": 3}, issues)
        assert any("Multiple H1s" in i["issue"] for i in issues)


class TestFormatReport:
    def test_format_report_success(self):
        r = {"url": "https://example.com", "status_code": 200, "page_size_kb": 1.0,
             "meta": {"title": "Test", "description": "Desc", "viewport": True},
             "headings": {"h1_count": 1, "h2_count": 2, "h3_count": 0},
             "content": {"word_count": 100, "paragraph_count": 5},
             "images": {"total": 0, "with_alt": 0, "missing_alt": 0, "empty_alt": 0},
             "internal_links": {"internal": 5, "external": 2, "nofollow": 0, "unique_linked_pages": 3},
             "schema": {"present": False, "count": 0, "types": [], "parse_errors": 0},
             "social": {"og": {}, "twitter": {}},
             "robots": {"status": "ok"}, "sitemap": {"status": "ok"},
             "ssl": {"https": True},
             "issues": [], "issue_count": 0,
             "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        output = seo_audit.format_report(r)
        assert "=== SEO Audit: https://example.com ===" in output
        assert "Test" in output

    def test_format_report_error(self):
        r = {"url": "https://x.com", "error": "Page fetch failed: timeout"}
        output = seo_audit.format_report(r)
        assert "ERROR" in output
