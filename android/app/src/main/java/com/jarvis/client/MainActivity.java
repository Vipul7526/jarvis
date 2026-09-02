package com.jarvis.client;

import android.Manifest;
import android.os.Bundle;
import androidx.activity.ComponentActivity;
import androidx.core.app.ActivityCompat;

public final class MainActivity extends ComponentActivity {
    private static final int REQUEST_PERMISSIONS = 4101;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        requestPermissionsIfNeeded();
        // Attach JarvisMethodChannel to the FlutterEngine when the Flutter host is added.
        // The native bridge is kept isolated so secrets never cross into the UI layer.
    }

    private void requestPermissionsIfNeeded() {
        if (android.os.Build.VERSION.SDK_INT >= 31) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT}, REQUEST_PERMISSIONS);
        }
        if (android.os.Build.VERSION.SDK_INT >= 33) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.POST_NOTIFICATIONS}, REQUEST_PERMISSIONS + 1);
        }
    }
}
