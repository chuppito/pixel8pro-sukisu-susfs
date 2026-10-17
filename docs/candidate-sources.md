# Candidate source revisions (not firmware validated)

Target: husky / CP3A.261005.005 / 6.1.162-android14-11-g9dd05a3a1de-ab16261587

Candidate manifest: `android-gs-shusky-6.1-android16`

Observed branch heads:

| Project | Git commit |
| --- | --- |
| kernel/common | 8769cc47188c3bdca2a34d39ba0f39a945b85465 |
| kernel/devices/google/zuma | eb90f2862e78b4c409ff992e116c44e81f836e9e |
| kernel/devices/google/shusky | a88953f657282d6e52c6c0b3669ca3a890907518 |
| kernel/build | 6483b5a6b74251440b266536c2dbc902a4fa3cf2 |

These are branch heads, not verified build-specific pins. The on-device short SHA `9dd05a3a1de` was not resolved. Git history fetch returned HTTP 500; this does not prove incompatibility.

Before building a flashable kernel, establish the matching Google source/tag or build manifest for this exact firmware, the kernel build configuration and required vendor modules, and a rollback image. Do not use Android 17 6.18 kernel branches for this Android 14 6.1 KMI target.

No claim of a functioning SukiSU Ultra/SUSFS kernel is made.
