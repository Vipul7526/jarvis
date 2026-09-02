// J.A.R.V.I.S. client boundary: transport types are explicit and never carry provider secrets.
import 'dart:convert';
import 'package:flutter/foundation.dart';

@immutable
class ReadinessState {
  const ReadinessState({required this.label, required this.state, required this.detail});

  final String label;
  final String state;
  final String detail;

  factory ReadinessState.fromJson(Map<String, dynamic> json) => ReadinessState(
        label: json['label'] as String? ?? 'UNKNOWN',
        state: json['state'] as String? ?? 'PLANNED',
        detail: json['detail'] as String? ?? '',
      );
}

class JarvisTransport {
  JarvisTransport({required this.baseUrl});

  final Uri baseUrl;

  // Network implementation belongs behind this boundary so clients can later
  // add certificate pinning, request timestamps, and session headers centrally.
  Future<ReadinessState> health() async {
    throw UnimplementedError('Connect a vetted HTTP client and backend session before release.');
  }

  Map<String, dynamic> encodeCommand({required String text, required String deviceId}) => {
        'command': text,
        'device_id': deviceId,
        'client': 'flutter',
        'payload_encoding': utf8.name,
      };
}
