# AI Quotation Coach — Agent Instructions

## Run context

- **Always run commands from `quotation-coach/` root** — all tools resolve paths internally.
- **Deps**: `pip install -r coach/requirements.txt` (requests, pyyaml, openpyxl, scikit-learn, mcp)
- **Python**: Use `python` (not python3) on Windows

## Tool commands (run from `quotation-coach/` root)

| Command | Purpose |
|---|---|
| `python coach/tools/make_quotation.py "<input>"` | AI quotation maker: "8 cameras 2MP", "3 cameras 4MP KPOI", etc. |
| `python coach/tools/make_quotation.py "<input>" --moi` | MOI-compliant quotation (120-day storage, RAID 5, UPS 1hr, AMC) |
| `python coach/tools/make_quotation.py "<input>" --moi --arabic` | MOI-compliant bilingual (EN/AR) quotation |
| `python coach/tools/make_quotation.py --interactive` | Interactive chat mode |
| `python coach/tools/make_quotation.py --list-rates` | Show current rate card |
| `python coach/tools/make_quotation.py --update-rates <file.xlsx>` | Import new prices from Excel |
| `python coach/tools/store_session.py <count> <type> <total> [notes] [--moi]` | Save a quotation session |
| `python coach/tools/read_context.py [N]` | Show checkpoint, goals, recent sessions |
| `python coach/tools/analyze_patterns.py` | Analyze quotation history for insights |
| `python coach/tools/backup_memory.py` | Git commit + ZIP backup |
| `python coach/tools/backup_memory.py --git-only` | Git commit only |
| `python coach/tools/backup_memory.py --zip-only` | ZIP archive only |
| `python coach/tools/update_rates.py <file.xlsx>` | Import new price sheet |
| `python coach/tools/mcp_server.py` | Start MCP server for memory access |
| `python coach/tools/session_hooks.py pre` | Print context before quoting |
| `python coach/tools/session_hooks.py post <count> <type> <total> [notes]` | Save session after quoting |

## Quick Examples

```powershell
# Standard quote
python coach/tools/make_quotation.py "8 cameras 2MP for Al Thani Villa"

# MOI-compliant quote
python coach/tools/make_quotation.py "16 cameras 2MP for Grand Mosque" --moi

# MOI-compliant bilingual (EN/AR) quote
python coach/tools/make_quotation.py "16 cameras 2MP for Grand Mosque" --moi --arabic

# 4MP KPOI system
python coach/tools/make_quotation.py "3 cameras 4MP KPOI" --moi

# ANPR system with discount
python coach/tools/make_quotation.py "2 cameras 4MP ANPR at parking" --customer "Gate 1" --discount 5

# View rates
python coach/tools/make_quotation.py --list-rates

# Interactive mode
python coach/tools/make_quotation.py --interactive
```

## Input Parsing

The quotation maker understands natural language:
- `"8 cameras 2MP"` → 8 cameras, 2MP bullet type
- `"3 cameras 4MP KPOI for mosque"` → 3 KPOI cameras
- `"2 cameras 4MP ANPR at parking entrance"` → 2 ANPR cameras with pole mounts
- `"20 cameras 2MP eyeball"` → 20 eyeball dome cameras
- `"4 cameras 8MP 4K"` → 4K ultra-HD cameras
- `"thermal"` → thermal camera system
- Suffix `--moi` → MOI-compliant mode

## System Configuration Logic

The tool auto-configures complete systems:

| Component | Selection Logic |
|---|---|
| **NVR** | 16ch for ≤13 cams, 32ch for ≤26, 64ch for ≤51 |
| **HDD** | Calculated for 30-day (standard) or 120-day (MOI) retention + RAID 5 overhead |
| **PoE Switch** | 8-port for ≤6 cams, 16-port for ≤14, 24-port for larger |
| **Rack** | 9U wall for ≤4, 18U for ≤16, 27U for ≤32, 42U for larger |
| **UPS** | 1KVA for ≤8 cams, 2KVA for ≤24, 3KVA for larger |
| **Monitor** | 24" for ≤9 cams, 32" for ≤16, dual 32" for larger |
| **Workstation** | Included for systems >8 cameras |

## MOI Compliance Features

When `--moi` flag is set:
- **120-day storage** retention (instead of 30)
- **RAID 5** HDD configuration (extra HDD for parity)
- **DSA/DIA** documentation and approvals included
- **Annual Maintenance Contract (AMC)** mandatory
- **UPS** with minimum 1-hour runtime
- **NVR RAID support** configured
- **MOI-specific terms** in quotation

## Memory Layout (`coach/memory/`)

| File | Format |
|---|---|
| `meta.md` | YAML: agent metadata, version, currency |
| `profile.md` | Company profile and MOI certification |
| `checkpoint.md` | Current focus and active projects |
| `goals.md` | Quotation targets and KPIs |
| `habits.md` | Daily quotation workflow habits |
| `decisions.md` | System design decisions log |
| `rates.json` | Rate card: cameras, NVRs, HDDs, switches, services |
| `moi_specs.json` | MOI technical specifications reference |
| `resources.md` | External links and references |
| `sessions/session-*.md` | Per-quotation YAML logs |
| `quotations/*.xlsx` | Generated quotation files |
| `backups/*.zip` | Timestamped ZIP backups |

## OpenCode Skill

The `.opencode/skills/ai-quotation-maker/SKILL.md` auto-loads when the user mentions quotations, pricing, CCTV, MOI, or security systems. It provides domain expertise on:
- MOI Law No. 9/2011 requirements
- Camera types and specifications
- System sizing rules
- Rate card structure
- Quotation generation workflow
