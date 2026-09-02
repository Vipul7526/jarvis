# Packaging

The `packaging/` folder contains release definitions for verified platform artifacts. It intentionally contains packaging metadata rather than fake binaries.

## Planned targets

| Target | Format | Current state |
|---|---|---|
| Windows | EXE and setup wizard | Native bridge scaffolded; signed release build pending |
| Android | APK | Flutter client scaffolded; signing and platform integration pending |
| Ubuntu/Debian/Kali | `.deb` and AppImage | Packaging definition included; native client pending |
| macOS | `.dmg` | Planned; Apple signing and macOS runner required |

Artifacts must be generated in CI from tagged commits, checked for signatures and checksums, and attached to the matching GitHub release. Never label a source scaffold as an installable release.
