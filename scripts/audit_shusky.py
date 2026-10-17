#!/usr/bin/env python3
"""Inspect candidate shusky kernel source metadata, read-only."""
import base64
import subprocess
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

BRANCH = "android-gs-shusky-6.1-android16"
BASE = "https://android.googlesource.com/"
def get(url, encoded=False):
    req = urllib.request.Request(url, headers={"User-Agent": "husky-kernel-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    return base64.b64decode(data, validate=True).decode("utf-8") if encoded else data.decode("utf-8")
def resolve_ref(project, revision):
    ref = "refs/heads/" + revision
    url = BASE + project
    proc = subprocess.run(
        ["git", "ls-remote", "--exit-code", url, ref],
        capture_output=True, text=True, timeout=45, check=True,
    )
    rows = [line.split(None, 1) for line in proc.stdout.splitlines() if line.strip()]
    for sha, found_ref in rows:
        if found_ref == ref and len(sha) == 40:
            return sha
    raise ValueError(f"No exact SHA found for {ref}; output: {proc.stdout[:300]!r}")

manifest_url = f"{BASE}kernel/manifest/+/refs/heads/{BRANCH}/default.xml?format=TEXT"
root = ET.fromstring(get(manifest_url, encoded=True))
default = root.find("default")
default_rev = default.get("revision") if default is not None else None
print("Manifest:", BRANCH)
print("Default revision:", default_rev)
projects = root.findall("project")
for p in projects:
    if p.get("name") not in ("kernel/common", "kernel/devices/google/shusky", "kernel/devices/google/zuma", "kernel/build"):
        continue
    name = p.get("name")
    revision = p.get("revision") or default_rev
    print("\nProject:", name, "revision:", revision)
    if not revision:
        print(" No revision declared")
        continue
    try:
        print(" Branch head commit:", resolve_ref(name, revision))
    except Exception as exc:
        print(" Branch lookup unavailable:", type(exc).__name__, str(exc))
print("\nDevice firmware: CP3A.261005.005")
print("Device kernel: 6.1.162-android14-11-g9dd05a3a1de-ab16261587")
print("WARNING: matching branch names or branch heads does NOT verify firmware-specific source commits.")
print("No flashable image produced.")
