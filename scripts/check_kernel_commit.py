#!/usr/bin/env python3
"""Check whether device kernel SHA is present in candidate Google kernel history."""
import os
import subprocess
import sys
import tempfile

BRANCH = "android-gs-shusky-6.1-android16"
HEAD = "8769cc47188c3bdca2a34d39ba0f39a945b85465"
DEVICE_SHORT_SHA = "9dd05a3a1de"
URL = "https://android.googlesource.com/kernel/common"

def run(*args, cwd=None, check=True):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=180, check=check)
    return result

print("Candidate branch:", BRANCH, flush=True)
print("Previously observed branch head:", HEAD, flush=True)
print("Device kernel short SHA:", DEVICE_SHORT_SHA, flush=True)
with tempfile.TemporaryDirectory() as directory:
    run("git", "init", "-q", directory)
    run("git", "remote", "add", "origin", URL, cwd=directory)
    run("git", "fetch", "--depth=1", "--filter=blob:none", "origin", "refs/heads/" + BRANCH, cwd=directory)
    actual_head = run("git", "rev-parse", "FETCH_HEAD", cwd=directory).stdout.strip()
    print("Fetched branch head:", actual_head, flush=True)
    if actual_head != HEAD:
        print("WARNING: branch moved since previous audit; results are not based on the recorded SHA.", flush=True)
    try:
        result = run("git", "fetch", "--depth=1", "--filter=blob:none", "origin", DEVICE_SHORT_SHA, cwd=directory)
        resolved = run("git", "rev-parse", "FETCH_HEAD", cwd=directory).stdout.strip()
        print("Device commit fetch: FOUND", resolved, flush=True)
        if resolved == actual_head:
            print("Exact branch head match: YES", flush=True)
        else:
            print("Exact branch head match: NO; ancestry not established.", flush=True)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print("Device commit fetch: NOT VERIFIED (server may reject abbreviated SHA fetch)", flush=True)
        print("Details:", str(exc)[:300], flush=True)
print("IMPORTANT: a matching commit alone does not establish full firmware or module compatibility.")
print("No build or flashable image produced.")
