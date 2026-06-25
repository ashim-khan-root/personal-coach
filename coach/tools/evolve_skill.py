"""Cluster high-confidence insights into new skill suggestions.
Usage:
  python tools/evolve_skill.py [--min-cluster 3] [--min-confidence 0.7]
"""
import sys, uuid, datetime, argparse, re
from pathlib import Path
from collections import defaultdict

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
EVOLVE_PATH = MEM_DIR / "evolution_suggestions.md"

_FIELD_PARSERS = {
    "pattern": ("pattern", str),
    "category": ("category", str),
    "confidence": ("confidence", float),
    "evidence_count": ("evidence_count", int),
    "summary": ("summary", str),
    "suggestion": ("suggestion", str),
}


def _parse_keyvalue_lines(text: str, field_map: dict) -> list[dict]:
    items = []
    current = {}
    for line in text.splitlines():
        if line.startswith("- id:"):
            if current:
                items.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif current:
            for prefix, (key, typ) in field_map.items():
                if line.startswith(f"  {prefix}:"):
                    raw = line.split(":", 1)[1].strip()
                    try:
                        current[key] = typ(raw) if typ != str else raw
                    except (ValueError, TypeError):
                        current[key] = typ() if typ else raw
                    break
    if current:
        items.append(current)
    return items


def parse_insights():
    path = MEM_DIR / "insights.md"
    if not path.exists():
        return []
    return _parse_keyvalue_lines(path.read_text(encoding="utf-8"), _FIELD_PARSERS)


def cluster_for_evolution(insights, min_confidence, min_cluster):
    clusters = defaultdict(list)
    for ins in insights:
        if ins.get("confidence", 0) < min_confidence:
            continue
        pattern = ins.get("pattern", "")
        match = re.match(r"(struggles_with|strong_at|frequent|topic)_(.+)", pattern)
        if match:
            domain = match.group(2)
            clusters[domain].append(ins)
        else:
            clusters[pattern].append(ins)

    suggestions = []
    for domain, cluster in clusters.items():
        if len(cluster) >= min_cluster:
            categories = [c.get("category", "") for c in cluster]
            avg_conf = sum(c.get("confidence", 0) for c in cluster) / len(cluster)
            suggestions.append({
                "source_insights": [c.get("id", "?") for c in cluster],
                "suggested_skill_name": domain.replace("_", "-"),
                "confidence": round(avg_conf, 2),
                "cluster_size": len(cluster),
                "categories": list(set(categories)),
                "summary": f"Cluster: {domain} ({len(cluster)} insights, avg confidence {avg_conf:.2f})",
            })
    return suggestions


def skill_exists(name):
    for d in SKILLS_DIR.iterdir():
        if d.is_dir() and d.name == name:
            return True
    return False


def write_suggestions(suggestions):
    lines = [
        "# Evolution Suggestions\n",
        "Auto-generated skill recommendations from insight clusters.\n",
        "Review and convert to actual skills by creating `skills/<name>/SKILL.md`.\n",
    ]
    for sug in suggestions:
        exists = skill_exists(sug["suggested_skill_name"])
        status = "exists" if exists else "draft"
        lines.append(f"- id: sug_{uuid.uuid4().hex[:8]}")
        lines.append(f"  suggested_skill_name: {sug['suggested_skill_name']}")
        lines.append(f"  confidence: {sug['confidence']}")
        lines.append(f"  cluster_size: {sug['cluster_size']}")
        lines.append(f"  categories: [{', '.join(sug['categories'])}]")
        lines.append(f"  summary: {sug['summary']}")
        lines.append(f"  status: {status}")
        if not exists:
            lines.append(f"  action: Create skills/{sug['suggested_skill_name']}/SKILL.md")
        else:
            lines.append(f"  action: Skill already exists — consider updating")
        lines.append(f"  created: {datetime.date.today().isoformat()}")
        lines.append(f"  source_insights: [{', '.join(sug['source_insights'][:5])}]")
        lines.append("")
    EVOLVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVOLVE_PATH.write_text("\n".join(lines), encoding="utf-8")
    return len(suggestions)


def main():
    parser = argparse.ArgumentParser(description="Evolve insights into skill suggestions")
    parser.add_argument("--min-cluster", type=int, default=3, help="Minimum insight cluster size")
    parser.add_argument("--min-confidence", type=float, default=0.7, help="Minimum insight confidence")
    args = parser.parse_args()

    insights = parse_insights()
    if not insights:
        print("No insights found. Run extract_insights.py first.")
        return

    suggestions = cluster_for_evolution(insights, args.min_confidence, args.min_cluster)
    count = write_suggestions(suggestions)
    print(f"Analyzed {len(insights)} insights, generated {count} skill suggestions (min cluster {args.min_cluster})")
    for s in suggestions:
        print(f"  {s['suggested_skill_name']} (confidence {s['confidence']}, cluster size {s['cluster_size']})")


if __name__ == "__main__":
    main()
