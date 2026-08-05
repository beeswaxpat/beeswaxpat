<p align="center">
  <img src="banner.svg?v=2" alt="BEESWAX PAT: agentic, privacy-first, honey-powered" width="750">
</p>

I build and ship agentic software: a production image-provenance API, MCP servers on the official registry, encrypted apps on Google Play and the App Store, and anything else I fancy at the moment.

Before this, many years of defense contracting. US Army veteran. 

**Open to agentic engineering roles.** [beeswaxpat@gmail.com](mailto:beeswaxpat@gmail.com)

---

#### Agent tools and APIs

- **[ChronoVerify](https://chronoverify.com/)**: Image capture-time and provenance verification, live in production. A **C2PA Conformant Validator**, listed on the [C2PA Conforming Products List](https://chronoverify.com/c2pa-conformance). Section 1 signatory to the EU Code of Practice on Transparency of AI-Generated Content, alongside Meta, OpenAI, and Google. Member of the Content Authenticity Initiative. Validates C2PA Content Credentials cryptographically against the official trust lists, layers on EXIF/XMP analysis and conservative pixel forensics, and returns one typed verdict plus a signed, independently verifiable report. Verifies provenance; deliberately does not claim AI detection. Free public verifier, keyless API, [MCP server](https://github.com/beeswaxpat/chronoverify-mcp), and [agent recipes](https://github.com/beeswaxpat/chronoverify-agent-recipes) for OpenAI, Claude, LangChain, LlamaIndex, CrewAI, and n8n. ([verify a photo](https://chronoverify.com/) · [API](https://chronoverify.com/method#api) · [conformance record](https://chronoverify.com/c2pa-conformance))

- **[chronoverify-mcp](https://github.com/beeswaxpat/chronoverify-mcp)**: MCP server on the official registry, npm, Glama, and Smithery. Typed `structuredContent`, honest tool descriptions, works keyless. `npx chronoverify-mcp`

- **[ffmpeg-render-pro](https://www.npmjs.com/package/ffmpeg-render-pro)**: Parallel video renderer for Node.js + FFmpeg. Worker threads split the frame range, GPU encoders auto-detected (NVENC, VideoToolbox, AMF), stream-copy concat with no re-encode. Ships a live dashboard, checkpoints, color grading, audio merge, and an MCP server exposing 7 typed tools.

#### Privacy-first apps

- **[Scrib](https://scrib.blog/)**: Encrypted notes for Android. AES-256, PIN lock, Private Vault, zero data collected. ([Google Play](https://play.google.com/store/apps/details?id=com.beeswaxpat.jot))
- **[Scrib Desktop](https://github.com/beeswaxpat/scrib-desktop)**: Open-source encrypted editor for Windows. AES-256, rich text, multi-tab, fully offline.
- **[Lumara Live](https://lumara-space.app)**: Sun and Moon dashboard. 12 NASA SDO wavelengths, moon phases, ISS feed, space weather. ([web](https://lumara-space.app) · [Google Play](https://play.google.com/store/apps/details?id=com.beeswaxpat.lumara) · [App Store](https://apps.apple.com/us/app/lumara-sun-moon-live-viewer/id6763933502))
- **[NEXUS-7](https://github.com/beeswaxpat/nexus-7)**: Cyberpunk markets dashboard for Windows. Public APIs only, no accounts, no keys, no telemetry.
- **[Ambient Pleasures](https://www.youtube.com/@ambientpleasures)**: Cinematic ambient YouTube channel, rendered end to end with local ffmpeg pipelines.

---

#### How I work

I research, plan, build, test, deploy, distribute, maintain it, I do not stop at a demo. Lean into GEO, AI-discoverability.

**Contact:** [beeswaxpat@gmail.com](mailto:beeswaxpat@gmail.com)
