package com.jarvis.client;

import android.content.Context;
import android.os.Build;

/**
 * Native Android boundary for capabilities that must remain outside Dart.
 * Secrets, pairing tokens, and provider credentials must never be placed here.
 */
public final class JarvisBridge {
    private final Context context;

    public JarvisBridge(Context context) {
        this.context = context.getApplicationContext();
    }

    public String platformDescriptor() {
        return "android:" + Build.VERSION.SDK_INT;
    }

    public boolean canUseNotificationListener() {
        return Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR2;
    }

    public boolean canUseBluetoothPairing() {
        return Build.VERSION.SDK_INT >= Build.VERSION_CODES.S;
    }
}
