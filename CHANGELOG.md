# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **AI Automotive Security Specialist:** New specialized AI role for expert guidance on vehicle cybersecurity, CAN bus analysis, and ECU hardening.
- **AI Graphic Designer:** New specialized AI role for expert brand identity, logo design, and high-impact thumbnail creation.
- **Xero Specialist:** New specialized AI role for expert guidance on Xero accounting, invoicing, financial reporting, and API integrations.
- **Cybersecurity Sentinel:** New specialized AI role for comprehensive security audits, penetration testing guidance, and threat intelligence.
- **Enhanced Backend Security:** Implemented HSTS, X-Frame-Options, X-Content-Type-Options, and X-XSS-Protection security headers to harden the API.

## [1.0.0] - 2024-05-20

### Added
- **Production Startup Status:** Officially transitioned from a demo project to a production-ready AI ecosystem.
- **Split Architecture:** Implemented a split architecture with a React frontend hosted on GitHub Pages (`docs/`) and a Flask backend for API services.
- **Specialized AI Agents:**
    - Antigravity Agent: Elite agentic development with secure Linux sandbox execution.
    - Gemini Spark: Autonomous multi-step tasks and workspace intelligence.
    - Router Capacity Architect: Intelligent LLM routing and capacity management.
    - DeepMind Image Gen & Video Creator: High-fidelity image and video synthesis.
    - Fine-Tuning Specialist: Guidance on LLM fine-tuning and dataset preparation.
    - USSD & Blockchain Expert: Fintech solutions for emerging markets.
    - Malware Defender: Specialized security role for threat mitigation.
- **Monetization Engine:**
    - Stripe integration for tiered subscriptions (Free, Premium, Pro).
    - Credit-based pay-per-use system for AI tasks.
    - Open Collective & Patreon sponsorship assistance.
- **Workflow Integrations:** Support for Gumloop, n8n, and Lamatic.ai workflow execution.
- **Multi-Platform Support:** Browser extensions (Chrome/Firefox), PWA (Android/iOS), and Desktop support.
- **Enterprise Security:** Specialized roles for Military Strategy, Gendarmerie, and Police security guidance.
- **Internationalization:** Support for Francophone markets (France, Belgium, Canada, Africa) with GDPR and OHADA compliance.
- **Advanced Document Management:** Comprehensive file storage system with SQLAlchemy backend and authenticated downloads.
- **GitHub Copilot Integration:** Tailored instructions and programmatic SDK integration for elite coding assistance.

### Changed
- Refactored backend to use asynchronous Flask endpoints for non-blocking AI invocations.
- Updated React marketplace UI with Lucide icons and mobile-responsive navigation.
- Optimized RAG context retrieval using SQLAlchemy's `with_entities`.

### Fixed
- Resolved path traversal vulnerabilities in file uploads using `secure_filename`.
- Fixed API key authentication for direct file downloads via query parameters.
- Corrected various backend unit tests for sponsorship and AI integration endpoints.

## [0.1.0] - 2024-03-15
### Added
- Initial demo version with basic Software Engineer, Debugger, and Marketer agents.
- Basic Flask backend and HTML/CSS frontend.
- Integration with Vertex AI for code generation.

[1.0.0]: https://github.com/GYFX35/AI-services/releases/tag/V10.0.0
[0.1.0]: https://github.com/GYFX35/AI-services/commits/main
