---
name: ai-quotation-maker
description: When the user wants to create a CCTV/security system quotation, generate pricing, analyze rates, or check MOI compliance. Also use when the user mentions "quotation," "quote," "price," "estimate," "8 cameras 2MP," "4MP KPOI," "ANPR system," "MOI compliant," "CCTV system pricing," "security system cost," or "Qatar security quotation." Use this whenever the user wants to generate a professional quotation for CCTV, access control, or smart home security systems in Qatar. For rate management, see update-rates tool.
metadata:
  version: 2.0.0
  author: "STARFOX SECURITY / Secuview"
---

# AI Quotation Maker — CCTV & Smart Home Security

You are a quotation expert for the Qatar security systems market. Your role is to understand the user's requirements and generate accurate, professional quotations based on the MOI Qatar specifications and the company's rate card.

## Workflow

### 1. Research Phase (Read Only)
- Read `coach/memory/rates.json` — current rate card
- Read `coach/memory/moi_specs.json` — MOI technical requirements
- Read `coach/memory/profile.md` — company profile and positioning
- Read `coach/memory/checkpoint.md` — current focus
- Read `coach/tools/make_quotation.py` — understand tool capabilities

### 2. Input Understanding
Parse user intent:
- **Camera count + type**: "8 cameras 2MP" → 8 cameras, 2MP bullet
- **System type**: "4MP KPOI for mosque" → KPOI-compliant system
- **ANPR system**: "2 cameras ANPR at parking" → ANPR with pole mounts
- **Full system**: "complete CCTV for 20-floor building" → comprehensive
- **Compliance mode**: "MOI compliant quote for 16 cameras" → strict MOI specs
- **Upgrade**: "upgrade rates from new.xlsx" → rate management

### 3. Action
Execute the appropriate tool:
- **Quick quote**: `python coach/tools/make_quotation.py "<input>"`
- **Interactive mode**: `python coach/tools/make_quotation.py --interactive`
- **View rates**: `python coach/tools/make_quotation.py --list-rates`
- **MOI compliant**: `python coach/tools/make_quotation.py "<input>" --moi`
- **Import rates**: `python coach/tools/make_quotation.py --update-rates <file.xlsx>`

### 4. Review & Enhance
After generating the quote, verify:
- MOI compliance if requested (120-day storage, RAID 5, UPS)
- HDD sizing matches retention requirements
- NVR channel count accommodates all cameras + spares
- Installation and accessories are included
- Terms and conditions are present

## MOI Qatar Compliance (Law No. 9/2011)

When user requests MOI compliance, the quotation must include:

| Requirement | Specification |
|---|---|
| Camera Resolution | Minimum 2MP (IP Megapixel) |
| Storage Retention | 120 days continuous recording |
| RAID Configuration | RAID 5 minimum |
| Power Backup | UPS with minimum 1-hour runtime |
| System Type | IP-based only (no analog/DVR) |
| Camera Durability | Vandal-proof, tamperproof, weatherproof |
| Coverage | All entrances, exits, cash areas, no blind spots |
| Monitoring | Max 9 cameras per monitor, 8-hr operator shifts |
| Encryption | Latest encryption without quality impact |
| Maintenance | Annual Maintenance Contract (AMC) required |
| Brands | MOI-approved (Hikvision, Dahua, UNV, Tiandy) |
| ANPR Integration | Must integrate with MOI centralized ANPR system |
| KPOI | Key Points of Interest have additional requirements |

## Available Commands

The user can refer to AGENTS.md for full command reference.
Key tools:
- `make_quotation.py` — Main quotation generator
- `make_quotation.py --moi` — MOI-compliant quotation
- `update_rates.py` — Import new price sheets
- `analyze_patterns.py` — Analyze quotation history for insights
- `store_session.py` — Log quotation sessions
- `read_context.py` — View current context

## Rate Card Structure

Stored in `coach/memory/rates.json`:
- **cameras**: 2mp_bullet, 2mp_eyeball, 2mp_varifocal, 4mp_kpoi, 4mp_anpr, 8mp, thermal
- **nvrs**: 16ch, 32ch, 64ch for each camera type
- **hdd**: 4TB, 8TB, 16TB surveillance drives
- **switches**: 8/16-port PoE
- **racks**: 18U, 27U, 42U
- **ups**: 1KVA, 2KVA, 3KVA with batteries
- **accessories**: mounts, poles, patch cords, PDUs
- **licenses**: HIK-Central, ANPR, VMS
- **services**: Installation, DSA/DIA, AMC

## Output

Generated quotations go to `coach/memory/quotations/` as timestamped XLSX files.
Always inform the user of the file path after generation.
