"""One-command setup for new PC. Run this on a fresh clone to
install deps, restore memory, configure Ollama, and verify.

Usage:
  py -3 coach/tools/setup_new_pc.py
"""
import sys, subprocess, os, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS = ROOT / "coach" / "tools"
PY = "py -3" if sys.platform == "win32" else "python3"


def run(cmd, desc, check=True):
    print(f"\n=== {desc} ===")
    r = subprocess.run(cmd, shell=True, cwd=str(ROOT))
    if check and r.returncode != 0:
        print(f"[FAIL] {desc}")
        sys.exit(1)
    print(f"[OK] {desc}")
    return r


def main():
    print(f"=== Personal Coach Setup ===")
    print(f"Platform: {sys.platform}")
    print(f"Root:     {ROOT}")

    run(f"{PY} -m pip install -r coach/requirements.txt", "Installing Python dependencies")

    mem_dir = ROOT / "coach" / "memory"

    backups = sorted((mem_dir / "backups").glob("memory-backup-*.zip"))
    if backups:
        latest = str(backups[-1])
        run(f"{PY} {TOOLS / 'restore_memory.py'} --from-zip \"{latest}\"", "Restoring latest ZIP backup")
    else:
        print("\nNo ZIP backup found. Skipping memory restore.")
        print("  (Run backup_memory.py on old PC first, then copy the ZIP)")

    ollama_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe"),
        shutil.which("ollama") or "",
    ]
    ollama_exe = next((p for p in ollama_paths if p and os.path.isfile(p)), None)

    if ollama_exe:
        print(f"\n=== Ollama found at: {ollama_exe} ===")
        r = subprocess.run(f'\"{ollama_exe}\" pull bge-m3', shell=True, check=False)
        if r.returncode == 0:
            print("[OK] bge-m3 pulled")
        else:
            print("[WARN] Could not pull bge-m3. Run 'ollama pull bge-m3' manually.")
    else:
        print("\n=== Ollama not found ===")
        print("  Install from https://ollama.com/download")
        print("  Then: ollama pull bge-m3")

    run(f"{PY} {TOOLS / 'index_memory.py'}", "Rebuilding memory vector index", check=False)

    r = run(f"{PY} {TOOLS / 'session_analytics.py'}", "Verifying pipeline", check=False)
    if r.returncode == 0:
        print("\n=== All good! Ready to work. ===")
    else:
        print("\nSetup completed with warnings.")


if __name__ == "__main__":
    main()
