// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "JarvisNativeBridge",
    platforms: [.macOS(.v13)],
    products: [.library(name: "JarvisNativeBridge", targets: ["JarvisNativeBridge"])],
    targets: [.target(name: "JarvisNativeBridge", path: "NativeBridge")]
)
