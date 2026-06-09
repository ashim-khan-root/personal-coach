"""Git backup + ZIP archive of quotation memory. Usage: python backup_memory.py"""
import shutil, datetime, zipfile, os, subprocess
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
BACKUP_DIR = MEM_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def git_commit_and_push(quiet=False):
    try:
        subprocess.run(["git", "add", "-A"], cwd=MEM_DIR.parent.parent, capture_output=True, timeout=30)
        subprocess.run(["git", "commit", "-m", f"quotation auto-backup {datetime.date.today()}"], cwd=MEM_DIR.parent.parent, capture_output=True, timeout=30)
        subprocess.run(["git", "push"], cwd=MEM_DIR.parent.parent, capture_output=True, timeout=60)
        if not quiet:
            print("[backup] Git backup complete")
    except Exception as e:
        if not quiet:
            print(f"[backup] Git backup skipped: {e}")

def zip_backup():
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    name = BACKUP_DIR / f"quotation-backup-{ts}.zip"
    with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as z:
        for f in MEM_DIR.rglob("*"):
            if f.is_file() and "backups" not in f.parts:
                z.write(f, f.relative_to(MEM_DIR.parent))
    print(f"[backup] ZIP saved: {name}")
    return name

def main():
    git_only = "--git-only" in sys.argv
    zip_only = "--zip-only" in sys.argv
    if zip_only:
        zip_backup()
    elif git_only:
        git_commit_and_push()
    else:
        git_commit_and_push()
        zip_backup()

if __name__ == "__main__":
    import sys
    main()
