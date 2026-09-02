package com.jarvis.client;

import android.app.Activity;
import io.flutter.plugin.common.MethodCall;
import io.flutter.plugin.common.MethodChannel;

/** Registers the minimal native capability surface exposed to Dart. */
public final class JarvisMethodChannel implements MethodChannel.MethodCallHandler {
    private final JarvisBridge bridge;

    public JarvisMethodChannel(Activity activity) {
        bridge = new JarvisBridge(activity);
    }

    @Override
    public void onMethodCall(MethodCall call, MethodChannel.Result result) {
        switch (call.method) {
            case "platformDescriptor":
                result.success(bridge.platformDescriptor());
                break;
            case "canUseNotificationListener":
                result.success(bridge.canUseNotificationListener());
                break;
            case "canUseBluetoothPairing":
                result.success(bridge.canUseBluetoothPairing());
                break;
            default:
                result.notImplemented();
        }
    }
}
