// J.A.R.V.I.S. macOS native boundary. Secrets remain in backend or OS-managed storage.
import Foundation

public struct JarvisCapabilityReport: Codable {
    public let platform: String
    public let localModelReady: Bool
    public let deviceControlReady: Bool

    public init(localModelReady: Bool = false, deviceControlReady: Bool = false) {
        self.platform = "macos"
        self.localModelReady = localModelReady
        self.deviceControlReady = deviceControlReady
    }
}

public struct JarvisEnvelope: Codable {
    public let protocolVersion: String
    public let messageId: String
    public let messageType: String
    public let createdAt: String
    public let source: String
    public let target: String?
    public let requiresConfirmation: Bool
    public let payload: [String: String]

    public init(messageType: String, source: String, payload: [String: String], target: String? = nil, requiresConfirmation: Bool = false) {
        self.protocolVersion = "JDP/1.0"
        self.messageId = UUID().uuidString
        self.messageType = messageType
        self.createdAt = ISO8601DateFormatter().string(from: Date())
        self.source = source
        self.target = target
        self.requiresConfirmation = requiresConfirmation
        self.payload = payload
    }
}
