"""Backup coach memory: git push + ZIP archive.
Usage:
  python tools/backup_memory.py               # git commit+push + ZIP
  python tools/backup_memory.py --git-only     # git only
  python tools/backup_memory.py --zip-only     # ZIP only
  python tools/backup_memory.py --quiet        # minimal output
"""
import sys, datetime, shutil, zipfile, subprocess, os
from pathlib import Path
from collections import deque

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MEM_DIR = PROJECT_ROOT / "coach" / "memory"
BACKUP_DIR = MEM_DIR / "backups"
MAX_BACKUPS = 15


def log(msg, quiet=False):
    if not quiet:
        print(msg)


def _ensure_git_config():
    """Set basic git user config if not already set."""
    for key in ("user.name", "user.email"):
        result = subprocess.run(
            ["git", "config", key],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)
        )
        if result.returncode != 0 or not result.stdout.strip():
            default = "Personal Coach Agent" if key == "user.name" else "coach@personal"
            subprocess.run(
                ["git", "config", key, default],
                capture_output=True, cwd=str(PROJECT_ROOT)
            )


def git_commit_and_push(quiet=False):
    """Stage all memory changes, commit, and push to remote."""
    try:
        _ensure_git_config()
        status = subprocess.run(
            ["git", "status", "--porcelain", "--", "coach/memory/"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)
        )
        if not status.stdout.strip():
            log("  No changes to commit.", quiet)
            return True
        changed = status.stdout.strip().splitlines()
        log(f"  Files changed: {len(changed)}", quiet)

        subprocess.run(
            ["git", "add", "-A", "--", "coach/memory/"],
            capture_output=True, cwd=str(PROJECT_ROOT), check=True
        )

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"Backup memory: {timestamp}"
        subprocess.run(
            ["git", "commit", "-m", msg, "--", "coach/memory/"],
            capture_output=True, cwd=str(PROJECT_ROOT)
        )

        push = subprocess.run(
            ["git", "push"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)
        )
        if push.returncode == 0:
            log(f"  Pushed to remote ({len(changed)} files).", quiet)
        else:
            log(f"  Commit OK but push failed: {push.stderr.strip()}", quiet)
        return True
    except subprocess.CalledProcessError as e:
        log(f"  Git error: {e}", quiet)
        return False
    except FileNotFoundError:
        log("  git not found on this system.", quiet)
        return False


def create_zip_archive(quiet=False):
    """Create timestamped ZIP of coach/memory/ in coach/memory/backups/."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_name = f"memory-backup-{timestamp}.zip"
    archive_path = BACKUP_DIR / archive_name

    mem_files = []
    for root, dirs, files in os.walk(str(MEM_DIR)):
        rel_root = os.path.relpath(root, str(MEM_DIR))
        if rel_root.startswith("backups"):
            dirs[:] = []
            continue
        for f in files:
            fpath = os.path.join(root, f)
            arcname = os.path.join(rel_root, f)
            mem_files.append((fpath, arcname))

    with zipfile.ZipFile(str(archive_path), "w", zipfile.ZIP_DEFLATED) as zf:
        for fpath, arcname in mem_files:
            zf.write(fpath, arcname)

    size_mb = archive_path.stat().st_size / (1024 * 1024)
    log(f"  Archive: {archive_name} ({size_mb:.2f} MB, {len(mem_files)} files)", quiet)
    return archive_path.name


def prune_old_backups(quiet=False):
    """Remove oldest backups beyond MAX_BACKUPS."""
    archives = sorted(BACKUP_DIR.glob("memory-backup-*.zip"))
    if len(archives) > MAX_BACKUPS:
        removed = []
        for old in archives[:-MAX_BACKUPS]:
            old.unlink()
            removed.append(old.name)
        log(f"  Pruned {len(removed)} old backup(s).", quiet)


def main():
    args = set(sys.argv[1:])
    quiet = "--quiet" in args
    git_only = "--git-only" in args
    zip_only = "--zip-only" in args

    log("=== Memory Backup ===", quiet)

    git_ok = False
    zip_name = None

    if not zip_only:
        log("[1/2] Git commit + push...", quiet)
        git_ok = git_commit_and_push(quiet)
        if not git_ok:
            log("  (continuing with ZIP anyway)", quiet)

    if not git_only:
        log("[2/2] Creating ZIP archive...", quiet)
        zip_name = create_zip_archive(quiet)
        prune_old_backups(quiet)

    if git_ok and zip_name:
        log(f"Backup complete. git=OK, zip={zip_name}", quiet)
    elif git_ok:
        log("Backup complete (git only).", quiet)
    elif zip_name:
        log("Backup complete (ZIP only).", quiet)
    else:
        log("Backup failed.", quiet)


if __name__ == "__main__":
    main()
