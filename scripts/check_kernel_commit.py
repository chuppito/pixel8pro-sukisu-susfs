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
    print("Searching Git history for device commit (bounded deepening)...", flush=True)
    found = False
    for depth in (1000, 5000, 20000):
        try:
            run("git", "fetch", "--deepen=" + str(depth), "--filter=blob:none", "origin", "refs/heads/" + BRANCH, cwd=directory)
            history = run("git", "rev-list", "FETCH_HEAD", cwd=directory).stdout.splitlines()
            hits = [sha for sha in history if sha.startswith(DEVICE_SHORT_SHA)]
            print("History commits scanned:", len(history), flush=True)
            if hits:
                print("Device commit in candidate branch history:", hits[0], flush=True)
                found = True
                break
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            print("History search interrupted:", type(exc).__name__, str(exc)[:250], flush=True)
            break
    if not found:
        print("Device commit: NOT FOUND in scanned history; this is not proof of incompatibility.", flush=True)

print("IMPORTANT: a matching commit alone does not establish full firmware or module compatibility.")
print("No build or flashable image produced.")
