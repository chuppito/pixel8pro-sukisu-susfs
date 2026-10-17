# Build gates — mandatory before enabling compilation

- [ ] Confirm factory build CP3A.261005.005 for husky against official Google release.
- [ ] Identify **exact** Google common-kernel source commit and Pixel device module sources used by that build.
- [ ] Confirm stock kernel release and ABI/KMI, and 4K/16K page size.
- [ ] Pin SukiSU Ultra and SUSFS commits; verify patch applicability and licensing.
- [ ] Validate configuration, ABI, vendor modules, boot image format, AVB and recovery strategy.
- [ ] Run compilation and inspect generated artifact, including kernel release string.
- [ ] Keep the current working boot/init_boot backups off-device.

A generic GKI image with matching android14-6.1 KMI is NOT automatically safe for husky.
Do not flash output from an unverified CI build. Never relock a modified device.
