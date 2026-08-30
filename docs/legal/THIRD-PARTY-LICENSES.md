# J.A.R.V.I.S. Third-Party Licenses

**Inventory status:** Initial manifest; regenerate during each release.  
**Effective date:** 30 August 2026

This file is a release artifact, not a substitute for the license files shipped by third-party components. The final Android, Windows, backend, and local-AI distributions must synchronize this inventory with their resolved dependency lockfiles where practical.

| Component | Version | License | Copyright | Source |
|---|---|---|---|---|
| FastAPI | Resolve from backend lockfile | Resolve from package metadata | Resolve from package metadata | https://github.com/fastapi/fastapi |
| Pydantic | Resolve from backend lockfile | Resolve from package metadata | Resolve from package metadata | https://github.com/pydantic/pydantic |
| Uvicorn | Resolve from backend lockfile | Resolve from package metadata | Resolve from package metadata | https://github.com/encode/uvicorn |
| python-dotenv | Resolve from backend lockfile | Resolve from package metadata | Resolve from package metadata | https://github.com/theskumar/python-dotenv |
| Flutter | Resolve from client lockfile | Resolve from upstream | Resolve from upstream | https://github.com/flutter/flutter |
| Dart packages | Resolve from client lockfile | Resolve per package | Resolve per package | https://pub.dev/ |
| llama.cpp | Resolve from bundled/submodule release | Resolve from upstream | Resolve from upstream | https://github.com/ggml-org/llama.cpp |
| GGUF models | Per selected model | Per model license | Per model metadata | Per model source URL |
| Google Fonts | Per selected font | Per font license | Per font metadata | https://fonts.google.com/ |

## Release requirements

Before distributing a build, replace every `Resolve from ...` value with the exact resolved version, license, copyright, and source URL. Include notices for native Android, Windows, Flutter, Python, C++, model, font, icon, and media dependencies actually shipped. Do not list a component as owned by J.A.R.V.I.S. merely because it is bundled by the build.
