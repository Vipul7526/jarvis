import XCTest
@testable import JarvisNativeBridge

final class JarvisBridgeTests: XCTestCase {
    func testEnvelopeUsesJdpProtocol() {
        let envelope = JarvisEnvelope(messageType: "health", source: "macos")
        XCTAssertEqual(envelope.protocolVersion, "JDP/1.0")
        XCTAssertEqual(envelope.source, "macos")
    }

    func testDefaultCapabilitiesAreNotClaimedReady() {
        let report = JarvisCapabilityReport()
        XCTAssertFalse(report.localModelReady)
        XCTAssertFalse(report.deviceControlReady)
    }
}
