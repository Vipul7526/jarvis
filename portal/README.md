# J.A.R.V.I.S. Public Portal

The `portal/` folder contains the public React portal for J.A.R.V.I.S. It presents the product overview, readiness board, release surfaces, Legal Center, Help Center, platform roadmap, and API setup guidance.

## Local development

Install Node.js 22 and pnpm 10, then run `pnpm install`, `pnpm run check`, `pnpm run build`, and `pnpm run dev`. The portal uses the generated artwork reserved for the managed web project and is also kept here as source-level UI documentation.

## Release truth

The portal intentionally distinguishes `verified`, `scaffolded`, and `planned`. Download buttons must never point to a binary that has not passed its platform build, signing, checksum, and clean-machine validation.
