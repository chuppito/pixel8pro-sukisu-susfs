#!/usr/bin/env python3
"""Inspect candidate shusky kernel source metadata, read-only."""
import base64
import json
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
def gitiles_json(url):
    text = get(url)
    return json.loads(text.partition("\n")[2] if text.startswith(")]}'") else text)

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
    url = f"{BASE}{name}/+refs/heads/{revision}?format=JSON"
    try:
        obj = gitiles_json(url)
        print(" Branch head commit:", obj.get("value") or obj.get("commit") or obj.get("id") or "(not provided)")
    except Exception as exc:
        print(" Branch lookup unavailable:", type(exc).__name__, str(exc))
print("\nDevice firmware: CP3A.261005.005")
print("Device kernel: 6.1.162-android14-11-g9dd05a3a1de-ab16261587")
print("WARNING: matching branch names or branch heads does NOT verify firmware-specific source commits.")
print("No flashable image produced.")
