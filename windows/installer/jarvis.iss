; J.A.R.V.I.S. Windows installer definition
; Build only after a signed EXE and verified service binaries exist.
#define MyAppName "J.A.R.V.I.S."
#define MyAppVersion "0.1.0"
#define MyAppPublisher "J.A.R.V.I.S. Project"
#define MyAppExeName "jarvis.exe"

[Setup]
AppId={{9E5A8A61-0C1F-4D75-AF28-5F67DF2B6C4F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\JARVIS
OutputBaseFilename=JARVIS-Setup-{#MyAppVersion}
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
Compression=lzma
SolidCompression=yes
; Signing certificate and release binaries are required before production use.

[Files]
; Source: "build\\windows\\x64\\runner\\Release\\jarvis.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Name: "{autoprograms}\\J.A.R.V.I.S."; Filename: "{app}\\{#MyAppExeName}"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
