#!/usr/bin/env python3
"""Check official source references without guessing a flashable kernel."""
import json
import os
import re
import urllib.parse
import urllib.request

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "husky-source-discovery/1.0"})
    with urllib.request.urlopen(req, timeout=25) as response:
        body = response.read(2_000_000).decode("utf-8")
    if body.startswith(")]}'"):
        body = body.partition("\n")[2]
    return json.loads(body)

def gitiles_refs(project, prefix):
    url = f"https://android.googlesource.com/{project}/+refs?format=JSON"
    data = fetch_json(url)
    if not isinstance(data, dict):
        raise ValueError("Gitiles refs response is not an object")
    return {key: value for key, value in data.items() if key.startswith(prefix)}

target = dict(line.strip().split("=", 1) for line in open("target.env", encoding="utf-8") if "=" in line and not line.startswith("#"))
print("Target:", target["DEVICE"], target["BUILD_ID"], target["KMI"])
print("Kernel release (device):", target["KERNEL_RELEASE"])
print("Note: a branch head is NOT a build-specific source revision.")
projects = [
    ("kernel/common", "refs/heads/android14-6.1"),
    ("kernel/manifest", "refs/heads/"),
]
for project, prefix in projects:
    try:
        refs = gitiles_refs(project, prefix)
        print(f"\n{project}: {len(refs)} refs returned")
        matches = [(k, v) for k, v in refs.items() if ("android14-6.1" in k or "husky" in k or "pixel" in k.lower())]
        for name, value in matches[:30]:
            sha = value.get("value", "") if isinstance(value, dict) else str(value)
            print(f"  {name}: {sha}")
        if len(matches) > 30:
            print(f"  ... {len(matches)-30} additional matching refs")
    except Exception as exc:
        print(f"{project}: discovery failed: {type(exc).__name__}: {exc}")
print("\nSOURCE PIN STATUS: UNVERIFIED")
print("No kernel build or boot image generated.")
