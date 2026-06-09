"""Create a new coaching plan from template. Usage:
  python tools/new_plan.py "<title>"
Saves to process/plans/active/<slug>-YYYYMMDD-HHMMSS.md
"""
import sys, datetime, re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PLANS_DIR = PROJECT_ROOT / "process" / "plans" / "active"
TEMPLATE = PROJECT_ROOT / "process" / "plans" / "_template.md"

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/new_plan.py '<title>'")
        sys.exit(1)

    title = sys.argv[1]
    now = datetime.datetime.now(datetime.timezone.utc)
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    filename = f"{slug}-{now.strftime('%Y%m%d-%H%M%S')}.md"
    filepath = PLANS_DIR / filename

    if TEMPLATE.exists():
        content = TEMPLATE.read_text(encoding="utf-8")
        content = content.replace('title: ""', f'title: "{title}"')
        content = content.replace('created: ""', f'created: "{now.isoformat()}"')
    else:
        content = f"""---
title: "{title}"
created: "{now.isoformat()}"
status: active
phase: research
---

## Objective

## Approach

## Deliverables

## Success Criteria
"""

    filepath.write_text(content, encoding="utf-8")
    print(f"Plan created: {filepath}")

if __name__ == "__main__":
    main()
