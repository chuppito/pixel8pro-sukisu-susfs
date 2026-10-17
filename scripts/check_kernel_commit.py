#!/usr/bin/env python3
"""Check whether device kernel SHA is present in candidate Google kernel history."""
import subprocess
import tempfile

BRANCH = "android-gs-shusky-6.1-android16"
HEAD = "8769cc47188c3bdca2a34d39ba0f39a945b85465"
DEVICE_SHORT_SHA = "9dd05ae3a1de"
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
    print("Inspecting shallow checkout and Git fetch diagnostics...", flush=True)
    try:
        shallow = run("git", "rev-parse", "--is-shallow-repository", cwd=directory).stdout.strip()
        print("Shallow repository:", shallow, flush=True)
        probe = subprocess.run(
            ["git", "-c", "http.version=HTTP/1.1", "fetch", "--deepen=10",
             "--filter=blob:none", "origin", "refs/heads/" + BRANCH],
            cwd=directory, capture_output=True, text=True, timeout=90,
        )
        print("Small-depth fetch exit:", probe.returncode, flush=True)
        if probe.returncode:
            print("Git stderr:", probe.stderr[-2500:] or "(empty)", flush=True)
            print("RESULT: HISTORY UNAVAILABLE; no ancestry conclusion.", flush=True)
        else:
            history = run("git", "rev-list", "FETCH_HEAD", cwd=directory).stdout.splitlines()
            matches = [sha for sha in history if sha.startswith(DEVICE_SHORT_SHA)]
            print("Commits inspected:", len(history), flush=True)
            print("Device SHA match:", matches[0] if matches else "NOT SEEN IN LIMITED HISTORY", flush=True)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print("Diagnostic interrupted:", type(exc).__name__, flush=True)
        if isinstance(exc, subprocess.CalledProcessError):
            print("Git stderr:", (exc.stderr or "")[-2500:], flush=True)

print("IMPORTANT: a matching commit alone does not establish full firmware or module compatibility.")
print("No build or flashable image produced.")
