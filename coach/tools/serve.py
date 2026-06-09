"""Dev server — start a local server and preview sites.
Usage:
  python tools/serve.py                    # Serve current work/ directory
  python tools/serve.py /path/to/site     # Serve specific directory
  python tools/serve.py --port 8080       # Custom port
  python tools/serve.py --open            # Auto-open browser
  python tools/serve.py --watch           # Live reload on file changes
"""
import sys, os, http.server, socketserver, threading, webbrowser, time
from pathlib import Path

PORT = 8000
SERVE_DIR = Path(__file__).resolve().parent.parent / "work"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if "200" not in str(args):
            return  # Only log errors
        print(f"  {self.address_string()} - {args[0]}")


def find_free_port(start=8000):
    port = start
    while port < start + 100:
        try:
            with socketserver.TCPServer(("", port), None) as s:
                pass
            return port
        except OSError:
            port += 1
    return start


def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def start_server(directory, port, open_browser=False):
    directory = Path(directory).resolve()
    if not directory.exists():
        print(f"Error: Directory not found: {directory}")
        sys.exit(1)

    os.chdir(directory)

    handler = QuietHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        local_ip = get_local_ip()

        print(f"=== Dev Server Started ===")
        print(f"  Serving: {directory}")
        print(f"  Local:   http://localhost:{port}")
        print(f"  Network: http://{local_ip}:{port}")
        print(f"  Press Ctrl+C to stop\n")

        if open_browser:
            threading.Timer(0.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


def watch_and_restart(directory, port):
    """Simple file watcher that restarts server on changes."""
    directory = Path(directory).resolve()
    mtimes = {}
    for fp in directory.rglob("*"):
        if fp.is_file() and not fp.name.startswith("."):
            mtimes[fp] = fp.stat().st_mtime

    print("Watching for file changes...")

    while True:
        time.sleep(1)
        changed = False
        for fp in directory.rglob("*"):
            if fp.is_file() and not fp.name.startswith("."):
                try:
                    mtime = fp.stat().st_mtime
                    if fp not in mtimes or mtime != mtimes[fp]:
                        print(f"  Changed: {fp.name}")
                        mtimes[fp] = mtime
                        changed = True
                except OSError:
                    pass

        if changed:
            print("  Reloading...")


def list_work_files():
    work_dir = Path(__file__).resolve().parent.parent / "work"
    if not work_dir.exists():
        print("No work/ directory found.")
        return

    files = []
    for fp in sorted(work_dir.rglob("*")):
        if fp.is_file() and fp.suffix in [".html", ".htm", ".css", ".js", ".md", ".csv", ".json"]:
            rel = fp.relative_to(work_dir)
            size = fp.stat().st_size
            files.append((rel, size))

    if files:
        print(f"=== Files in work/ ===\n")
        for rel, size in files:
            print(f"  {rel} ({size:,} bytes)")
        print(f"\nRun: python tools/serve.py --open")
    else:
        print("No web files found in work/.")


def main():
    directory = str(SERVE_DIR)
    port = PORT
    open_browser = False
    watch = False

    args = sys.argv[1:]

    if not args:
        list_work_files()
        return

    i = 0
    while i < len(args):
        if args[i] == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
            i += 2
        elif args[i] == "--open":
            open_browser = True
            i += 1
        elif args[i] == "--watch":
            watch = True
            i += 1
        elif not args[i].startswith("-"):
            directory = args[i]
            i += 1
        else:
            i += 1

    port = find_free_port(port)

    if watch:
        threading.Thread(target=watch_and_restart, args=(directory, port), daemon=True).start()

    start_server(directory, port, open_browser)


if __name__ == "__main__":
    main()
