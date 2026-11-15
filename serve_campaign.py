#!/usr/bin/env python3
"""
serve_campaign.py — serve a static site on 0.0.0.0:5990 and open UFW for it.

Typical use (on the host, e.g. zero@192.168.193.196):
    python3 ~/mabkom/serve_campaign.py

Options:
    --dir PATH    directory to serve (default: ~/mabkom/campaign)
    --port N      port (default: 5990)
    --bind ADDR   bind address (default: 0.0.0.0)
    --no-ufw      skip adding the firewall rule
"""

import argparse
import functools
import http.server
import os
import shutil
import socket
import subprocess
import sys

DEFAULT_DIR = os.path.expanduser("~/mabkom/campaign")
DEFAULT_PORT = 5990


def run(cmd):
    """Run a command, return (ok, combined_output)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    except FileNotFoundError:
        return False, f"{cmd[0]}: command not found"


def allow_ufw(port):
    if not shutil.which("ufw"):
        print("[!] ufw not installed; skipping firewall rule.")
        return

    # Non-interactive sudo: works if the user has NOPASSWD or a valid
    # sudo timestamp. Otherwise we fall back to printing the manual command.
    ok, out = run(["sudo", "-n", "ufw", "allow", f"{port}/tcp"])
    if ok:
        print(f"[+] ufw rule ensured: allow {port}/tcp")
        if out:
            print("    " + out.replace("\n", "\n    "))
    else:
        print(f"[!] Could not add ufw rule non-interactively ({out}).")
        print(f"    Run manually:  sudo ufw allow {port}/tcp")


def local_ips():
    ips = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))      # no packets actually sent
        ips.add(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ips.add(info[4][0])
    except socket.gaierror:
        pass
    ips.discard("127.0.0.1")
    return sorted(ips)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=DEFAULT_DIR, help="directory to serve")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--bind", default="0.0.0.0")
    ap.add_argument("--no-ufw", action="store_true", help="skip ufw rule")
    args = ap.parse_args()

    root = os.path.abspath(os.path.expanduser(args.dir))
    if not os.path.isdir(root):
        sys.exit(f"[x] Not a directory: {root}")

    if not args.no_ufw:
        allow_ufw(args.port)

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
    httpd = http.server.ThreadingHTTPServer((args.bind, args.port), handler)

    print(f"[+] Serving {root}")
    print(f"[+] Listening on http://{args.bind}:{args.port}/")
    for ip in local_ips():
        print(f"    http://{ip}:{args.port}/")
    print("[i] Ctrl+C to stop.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[i] Stopped.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
