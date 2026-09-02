# Windows Installer

This folder contains the Inno Setup definition for a future J.A.R.V.I.S. Windows setup wizard. It reserves service registration, shortcuts, installation location, and safe uninstall behavior.

## Release requirements

A production wizard requires a real signed EXE, tested service lifecycle, code-signing certificate, upgrade behavior, rollback behavior, and validation on clean Windows machines. Until those checks pass, the `.iss` file is a packaging definition only.
