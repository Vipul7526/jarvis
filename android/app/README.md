# Android Application Module

This module is the native Android entry point for J.A.R.V.I.S. It declares the application identity, SDK compatibility, runtime permissions, and release shrinker settings. Flutter embedding and platform-channel registration should be connected here when the Flutter SDK is available.

The module intentionally does not include API keys, OAuth secrets, or device trust material.
