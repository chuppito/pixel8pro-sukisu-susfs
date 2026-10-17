#!/usr/bin/env python3
"""Inspect candidate Google kernel manifests without selecting a flashable source."""
import base64
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

BRANCHES = [
    "common-android14-6.1-2026-09",
    "android14-gs-pixel-6.1",
    "android-gs-shusky-6.1-android16",
]
BASE = "https://android.googlesource.com/kernel/manifest/+/refs/heads/"
def read_manifest(branch):
    url = BASE + branch + "/default.xml?format=TEXT"
    req = urllib.request.Request(url, headers={"User-Agent": "husky-manifest-inspector/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return base64.b64decode(response.read(), validate=True).decode("utf-8")

for branch in BRANCHES:
    print("\n=== ", branch, " ===", sep="")
    try:
        xml = read_manifest(branch)
        root = ET.fromstring(xml)
        defaults = root.find("default")
        print("default revision:", defaults.get("revision", "(none)") if defaults is not None else "(none)")
        projects = root.findall("project")
        print("direct projects:", len(projects))
        for item in projects:
            name = item.get("name", "")
            path = item.get("path", "")
            revision = item.get("revision", "(inherited)")
            print(" project:", name, "path:", path, "revision:", revision)
        includes = root.findall("include")
        for item in includes:
            print(" include:", item.get("name", ""))
        print("NOTICE: included XML files and inherited revisions require further resolution.")
    except (urllib.error.URLError, ValueError, ET.ParseError) as exc:
        print("FAILED:", type(exc).__name__, str(exc))
print("\nFIRMWARE-SPECIFIC SOURCE PIN: UNVERIFIED")
print("No compilation or flashable image generated.")
