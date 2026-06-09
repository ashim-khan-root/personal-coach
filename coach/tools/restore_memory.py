"""Restore coach memory from git or ZIP backup.
Usage:
  python tools/restore_memory.py                # git pull + rebuild index
  python tools/restore_memory.py --from-zip     # extract latest ZIP backup
  python tools/restore_memory.py --from-zip <path>  # extract specific ZIP
  python tools/restore_memory.py --list         # list available backups
"""
import sys, zipfile, subprocess, os, shutil, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MEM_DIR = PROJECT_ROOT / "coach" / "memory"
BACKUP_DIR = MEM_DIR / "backups"
INDEX_PY = PROJECT_ROOT / "coach" / "tools" / "index_memory.py"


def rebuild_index():
    print("  Rebuilding TF-IDF vector index...")
    try:
        import sys as _sys
        _sys.path.insert(0, str(PROJECT_ROOT / "coach"))
        from tools.index_memory import build_index
        build_index()
        print("  Vector index rebuilt.")
    except Exception as e:
        print(f"  Index rebuild skipped: {e}")


def list_backups():
    print("=== Available Backups ===")
    archives = sorted(BACKUP_DIR.glob("memory-backup-*.zip"))
    if not archives:
        print("  No ZIP backups found.")
        return
    for a in archives:
        size_kb = a.stat().st_size / 1024
        modified = datetime.datetime.fromtimestamp(a.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"  {a.name}  ({size_kb:.0f} KB)  {modified}")
    print(f"\n  Total: {len(archives)} backup(s)")


def restore_from_git():
    print("=== Restore from Git ===")
    try:
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"  Git pull: {output.split(chr(10))[0]}")
            rebuild_index()
            print("Restore from git complete.")
            return True
        else:
            print(f"  Git pull failed: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("  git not found on this system.")
        return False


def restore_from_zip(zip_path=None):
    print("=== Restore from ZIP ===")
    if zip_path:
        archive = Path(zip_path)
        if not archive.exists():
            print(f"  File not found: {zip_path}")
            return False
    else:
        archives = sorted(BACKUP_DIR.glob("memory-backup-*.zip"))
        if not archives:
            print("  No ZIP backups found in coach/memory/backups/")
            return False
        archive = archives[-1]
        print(f"  Using latest: {archive.name}")

    print(f"  Extracting to {MEM_DIR}...")
    with zipfile.ZipFile(str(archive), "r") as zf:
        zf.extractall(str(MEM_DIR))
    print(f"  Extracted {len(zf.namelist())} files.")

    rebuild_index()
    print("Restore from ZIP complete.")
    return True


def main():
    args = sys.argv[1:]

    if "--list" in args:
        list_backups()
        return

    if "--from-zip" in args:
        idx = args.index("--from-zip")
        zip_path = args[idx + 1] if idx + 1 < len(args) and not args[idx + 1].startswith("--") else None
        restore_from_zip(zip_path)
    else:
        restore_from_git()


if __name__ == "__main__":
    main()
