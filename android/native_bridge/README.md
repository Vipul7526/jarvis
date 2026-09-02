# Android Native Bridge

The `native_bridge/` folder contains Java code that belongs behind Flutter platform channels. It reports Android capabilities for notifications and Bluetooth pairing without storing provider credentials or long-lived secrets.

## Integration

Register the bridge from a Flutter plugin or `MethodChannel`, request runtime permissions in the Android app layer, and forward only capability results to Dart. Verify behavior on each supported Android API level before enabling a production release.
