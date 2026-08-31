# Project Scripts

The `scripts/` folder contains maintenance and release helpers for J.A.R.V.I.S.

## Publish and backup

`publish_and_backup.sh` commits local changes, pushes the current branch to GitHub, creates a source ZIP excluding Git metadata and generated caches, calculates a SHA-256 checksum, and uploads the archive to Google Drive through the configured Workspace account.

Set the Drive destination folder before running it:

```bash
export JARVIS_DRIVE_PARENT_ID="your-google-drive-folder-id"
./scripts/publish_and_backup.sh
```

The script does not contain credentials. It expects GitHub authentication and an active Google Workspace account to already be configured. It also refuses to upload when `JARVIS_DRIVE_PARENT_ID` is missing.

## Safety

Review `git status` and the generated commit before using the script in a production release. Backups are created as new versioned archives; the script never deletes existing Drive files.
