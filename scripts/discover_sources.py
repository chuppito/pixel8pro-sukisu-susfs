#!/usr/bin/env python3
"""Read-only source discovery; no assumptions about firmware pinning."""
import json
import urllib.request

BASE = "https://android.googlesource.com/"
def fetch_json(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "husky-source-discovery/2.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read().decode("utf-8")
    if raw.startswith(")]}'"):
        raw = raw.partition("\n")[2]
    return json.loads(raw)

target = dict(line.strip().split("=", 1) for line in open("target.env", encoding="utf-8") if "=" in line and not line.startswith("#"))
print("Target:", target["DEVICE"], target["BUILD_ID"], target["KMI"])
print("Kernel release (device):", target["KERNEL_RELEASE"])
print("Note: branch heads are NOT build-specific source revisions.")

try:
    obj = fetch_json("kernel/common/+/refs/heads/android14-6.1/?format=JSON")
    print("\nkernel/common branch head:", obj.get("commit") or obj.get("id") or "unknown")
except Exception as exc:
    print("\nkernel/common lookup failed:", type(exc).__name__, str(exc))

try:
    refs = fetch_json("kernel/manifest/+refs?format=JSON")
    if not isinstance(refs, dict):
        raise ValueError("Unexpected manifest refs payload")
    print("\nkernel/manifest: total refs:", len(refs))
    matches = [(k, v) for k, v in refs.items() if any(s in k.lower() for s in ("shusky", "android17", "android14-gs-pixel-6.1", "common-android14-6.1"))]
    print("Relevant refs:", len(matches))
    for key, val in matches[:80]:
        sha = val.get("value", "") if isinstance(val, dict) else str(val)
        print(" ", key, sha)
    if len(matches) > 80:
        print(" ...", len(matches)-80, "additional matches")
except Exception as exc:
    print("\nkernel/manifest lookup failed:", type(exc).__name__, str(exc))

print("\nSOURCE PIN STATUS: UNVERIFIED")
print("No kernel build or boot image generated.")
