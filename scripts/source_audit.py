#!/usr/bin/env python3
"""Read-only discovery. Never infer firmware compatibility from KMI alone."""
import json
import urllib.request

URLS = {
    "google_common_6_1": "https://android.googlesource.com/kernel/common/+/refs/heads/android14-6.1/?format=JSON",
    "google_pixel_kernel": "https://android.googlesource.com/kernel/google-modules/",
    "sukisu": "https://api.github.com/repos/SukiSU-Ultra/SukiSU-Ultra",
    "susfs": "https://gitlab.com/simonpunk/susfs4ksu",
}
print("Target: husky / CP3A.261005.005 / android14-6.1")
print("WARNING: these are upstream discovery URLs, NOT exact firmware source pins.")
for name, url in URLS.items():
    req = urllib.request.Request(url, headers={"User-Agent": "husky-source-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read(400_000).decode("utf-8", errors="replace")
            print(f"{name}: HTTP {resp.status} ({resp.geturl()})")
            if name == "sukisu":
                obj = json.loads(body)
                print("  default_branch:", obj.get("default_branch"))
            elif name == "google_common_6_1":
                obj = json.loads(body.removeprefix(")]}'\\n"))
                print("  gitiles commit:", obj.get("commit"))
    except Exception as exc:
        print(f"{name}: unavailable: {type(exc).__name__}: {exc}")
print("RESULT: exact husky firmware source commit is UNVERIFIED.")
print("BUILD DISABLED: no flashable image produced.")
