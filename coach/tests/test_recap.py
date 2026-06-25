import sys, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import recap


class TestRecapHelpers:
    def test_parse_session_file(self):
        text = """date: "2026-06-25"
skill: seo-audit
rating: 8
duration_min: 45
notes: "Fixed meta descriptions"
- decision: "Switched to argparse"
"""
        data = recap._parse_session_file(text)
        assert data["date"] == "2026-06-25"
        assert data["skill"] == "seo-audit"
        assert data["rating"] == "8"
        assert data["duration"] == "45"
        assert data["notes"] == "Fixed meta descriptions"
        assert "Switched to argparse" in data["decisions"]

    def test_generate_recap(self):
        r = recap.generate_recap(365)
        assert "Recap: Last 365 Days" in r
        assert "Sessions:" in r
        assert "Activity Summary" in r


class TestLoadFunctions:
    def test_load_recent_sessions(self):
        s = recap.load_recent_sessions(365)
        assert isinstance(s, list)
        if s:
            assert "skill" in s[0]

    def test_load_recent_decisions(self):
        d = recap.load_recent_decisions(365)
        assert isinstance(d, list)
