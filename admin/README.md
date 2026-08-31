# Admin Surface

The `admin/` folder is reserved for the J.A.R.V.I.S. administration dashboard. It will manage users, approved identities, pending and revoked access, devices, authentication, OAuth configuration status, email status, security events, system health, logs, support content, legal documents, announcements, and configuration.

## Setup guide

Build the admin client against the protected backend API. Every administrative endpoint must require the `ADMIN` role, an expiring authenticated session, audit logging, and server-side authorization. The client must never receive the complete private allowlist unless a future policy explicitly requires a carefully redacted administrative view.

## Safety

The current backend includes `POST /api/v1/admin/devices/{device_id}/revoke`, which clears device permissions and changes the trust state to `REVOKED`. Admin actions such as approve, revoke, disable, enable, legal-document updates, and configuration changes should require clear confirmation and produce immutable or tamper-evident audit records in production.
