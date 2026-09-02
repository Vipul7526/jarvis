# macOS Swift Layer

The macOS layer contains a Swift Package target for native capability reporting and JDP/1.0 envelope creation. It is designed to sit behind a future Flutter macOS client and must not receive provider secrets directly.

## Build

On macOS with Swift 5.9 or newer, run `swift build` from this folder. A genuine DMG additionally requires an Xcode/macOS runner, app signing, notarization, hardened runtime configuration, and clean-machine installation tests. The current Linux environment can store and review this source but cannot compile or notarize a DMG.
