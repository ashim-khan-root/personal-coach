"""MOI Site Survey tool: track site visits, findings, and follow-ups.
Usage:
  py -3 coach/tools/site_survey.py add "<client>" "<location>" [contact] [notes]
  py -3 coach/tools/site_survey.py list [--all|--open|--today]
  py -3 coach/tools/site_survey.py view <id>
  py -3 coach/tools/site_survey.py close <id> [summary]
"""
import sys, datetime, re
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
fp = MEM_DIR / "site_surveys.md"

TEMPLATE = """# MOI Site Surveys

Records of site survey visits for quotation and installation projects.
"""


def _ensure_file():
    if not fp.exists():
        fp.write_text(TEMPLATE, encoding="utf-8")


def _load_all():
    _ensure_file()
    text = fp.read_text(encoding="utf-8")
    surveys = []
    buffer = []
    for line in text.split("\n"):
        if line.startswith("- id:"):
            if buffer:
                surveys.append(_parse(buffer))
            buffer = [line]
        elif line.startswith("  ") and buffer:
            buffer.append(line)
    if buffer:
        surveys.append(_parse(buffer))
    return surveys


def _parse(lines):
    s = {}
    for line in lines:
        if m := re.match(r"- id:\s*(.+)", line):
            s["id"] = m.group(1).strip()
        elif m := re.match(r"\s+client:\s*\"(.+)\"", line):
            s["client"] = m.group(1)
        elif m := re.match(r"\s+location:\s*\"(.+)\"", line):
            s["location"] = m.group(1)
        elif m := re.match(r"\s+date:\s*(.+)", line):
            s["date"] = m.group(1).strip()
        elif m := re.match(r"\s+contact:\s*(.+)", line):
            s["contact"] = m.group(1).strip()
        elif m := re.match(r"\s+status:\s*(.+)", line):
            s["status"] = m.group(1).strip()
        elif m := re.match(r"\s+notes:\s*\"(.+)\"", line):
            s["notes"] = m.group(1)
        elif m := re.match(r"\s+summary:\s*\"(.+)\"", line):
            s["summary"] = m.group(1)
    return s


def _save_all(surveys):
    _ensure_file()
    lines = [TEMPLATE.rstrip()]
    for s in surveys:
        lines.append(f"- id: {s.get('id', '?')}")
        lines.append(f'  client: "{s.get("client", "")}"')
        lines.append(f'  location: "{s.get("location", "")}"')
        lines.append(f"  date: {s.get('date', '')}")
        lines.append(f"  contact: {s.get('contact', '')}")
        lines.append(f"  status: {s.get('status', 'open')}")
        if s.get("notes"):
            lines.append(f'  notes: "{s["notes"]}"')
        if s.get("summary"):
            lines.append(f'  summary: "{s["summary"]}"')
    fp.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _next_id(surveys):
    nums = []
    for s in surveys:
        m = re.search(r"survey-(\d+)", s.get("id", ""))
        if m:
            nums.append(int(m.group(1)))
    return f"survey-{(max(nums) + 1) if nums else 1}"


def cmd_add(client, location, contact="", notes=""):
    surveys = _load_all()
    new_id = _next_id(surveys)
    entry = {
        "id": new_id,
        "client": client,
        "location": location,
        "date": datetime.date.today().isoformat(),
        "contact": contact,
        "status": "open",
        "notes": notes,
    }
    surveys.append(entry)
    _save_all(surveys)
    print(f"Site survey added: [{new_id}] {client} @ {location}")


def cmd_list(filter_mode="open"):
    surveys = _load_all()
    if not surveys:
        print("No site surveys recorded.")
        return

    if filter_mode == "open":
        surveys = [s for s in surveys if s.get("status") != "closed"]
    elif filter_mode == "today":
        today = datetime.date.today().isoformat()
        surveys = [s for s in surveys if s.get("date") == today]

    if not surveys:
        print(f"No {filter_mode} surveys.")
        return

    for s in sorted(surveys, key=lambda x: x.get("date", ""), reverse=True):
        status = s.get("status", "?")
        contact = f" ({s['contact']})" if s.get("contact") else ""
        print(f"  [{s['id']}] [{status}] {s.get('client','?')}{contact}")
        print(f"         {s.get('date','?')} @ {s.get('location','?')}")
        if s.get("notes"):
            print(f"         {s['notes'][:60]}")
        print()


def cmd_view(survey_id):
    surveys = _load_all()
    for s in surveys:
        if s["id"] == survey_id:
            print(f"ID:       {s['id']}")
            print(f"Client:   {s.get('client', '?')}")
            print(f"Location: {s.get('location', '?')}")
            print(f"Date:     {s.get('date', '?')}")
            print(f"Contact:  {s.get('contact', '?') or 'N/A'}")
            print(f"Status:   {s.get('status', '?')}")
            print(f"Notes:    {s.get('notes', '')}")
            print(f"Summary:  {s.get('summary', '')}")
            return
    print(f"Survey not found: {survey_id}")


def cmd_close(survey_id, summary=""):
    surveys = _load_all()
    for s in surveys:
        if s["id"] == survey_id:
            s["status"] = "closed"
            if summary:
                s["summary"] = summary
            _save_all(surveys)
            print(f"Survey closed: [{survey_id}] {s['client']}")
            return
    print(f"Survey not found: {survey_id}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    cmd = args[0]
    rest = args[1:]

    if cmd == "add":
        if len(rest) < 2:
            print("Usage: site_survey.py add '<client>' '<location>' [contact] [notes]")
            sys.exit(1)
        cmd_add(rest[0], rest[1], rest[2] if len(rest) > 2 else "", rest[3] if len(rest) > 3 else "")
    elif cmd == "list":
        mode = rest[0] if rest else "open"
        mode = mode.lstrip("-")
        cmd_list(mode)
    elif cmd == "view":
        if not rest:
            print("Usage: site_survey.py view <id>")
            sys.exit(1)
        cmd_view(rest[0])
    elif cmd == "close":
        if not rest:
            print("Usage: site_survey.py close <id> [summary]")
            sys.exit(1)
        cmd_close(rest[0], rest[1] if len(rest) > 1 else "")
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
