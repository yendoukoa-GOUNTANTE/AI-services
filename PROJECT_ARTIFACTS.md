# Yendoukoa AI: Project Artifacts Manifest

This document provides a comprehensive catalog of the artifacts and components within the Yendoukoa AI ecosystem.

## 🏛️ Ecosystem Architecture

The project follows a split architecture designed for scalability, performance, and multi-platform deployment.

### 1. Backend API (Flask)
- **Core:** `app.py`
- **Port:** 5001
- **Technology:** Python, Flask (Asynchronous), SQLAlchemy, SQLite.
- **Key Features:** User authentication, credit-based economy, database-backed agent/design store, Stripe/Meta integrations, and security hardening.
- **Database:** `project.db` (SQLite) containing Users, Agents, Designs, Purchases, and Files.

### 2. AI Intelligence Engine
- **Module:** `google_ai.py`
- **Integration:** Multi-model support including:
    - **Google Vertex AI:** Gemini 1.5 Pro/Flash, Imagen 3, Veo 3.1.
    - **Anthropic:** Claude 3.5 Sonnet.
    - **OpenAI:** GPT-4o.
    - **NVIDIA:** Llama 3.1 405B, Nemotron-4 340B.
    - **GitHub Models:** Access to high-performance open and closed models.

### 3. Marketplace Frontend (React)
- **Directory:** `marketplace-frontend/`
- **Technology:** React, Vite, TypeScript, Tailwind CSS, Lucide Icons.
- **Deployment Build:** Located in `docs/` for GitHub Pages hosting.
- **URL:** [https://yendoukoa.ai](https://yendoukoa.ai) (Local: [http://localhost:5173](http://localhost:5173))

### 4. Local Project Portal
- **Directory:** `yendoukoa-ai-site/`
- **Entry Point:** `yendoukoa-ai-site/index.html`
- **Purpose:** A standalone dashboard for local environment management, service monitoring, and documentation access.

### 5. Multi-Platform Extensions
- **Browser Extension:** `extension/` (Manifest v3, supporting Chrome and Firefox).
- **Mobile/Desktop:** Progressive Web App (PWA) configuration integrated into the frontend build.

---

## 🤖 Specialized AI Agents Catalog

Yendoukoa AI features a diverse array of specialized agents, each accessible via the platform API.

### Software & Development
- **Software Engineer:** Professional static website generation (HTML/CSS).
- **Debugger:** Multi-model code analysis and conflict resolution.
- **System Analyser:** Infrastructure audit and broken link detection.
- **OS Kernel Architect:** Elite Yendoukoa OS kernel design and performance optimization.
- **File System Architect:** Expert in OS file system design and data persistence.
- **Process Controller:** OS process management and task scheduling specialist.
- **Fine-Tuning Specialist:** LLM dataset preparation and training guidance.
- **Antigravity Agent:** Autonomous task execution in secure Linux sandboxes.
- **GitHub Copilot Expert:** Programmatic coding assistance and architectural advice.

### Business & Marketing
- **Elite Marketer Bot:** Campaign management and high-fidelity video generation (Google Veo 3.1).
- **Financial Advisor:** Wealth management and investment trading optimization.
- **Monetization Strategist:** Revenue model design (Sponsorships, Subscriptions).
- **Xero Specialist:** Expert accounting and financial integration (Xero API).
- **Sage/Odoo Experts:** ERP implementation for Francophone markets.

### Security & Strategy
- **Cybersecurity Sentinel:** Elite security audits and penetration testing guidance.
- **Malware Defender:** Threat detection and system hardening specialist.
- **Automotive Security:** Specialized vehicle cybersecurity and CAN bus analysis.
- **Military/Public Security Strategists:** Specialized tactical and operational guidance for national security entities.

### Domain-Specific Experts
- **Togo Public Service Assistant:** Specialized guidance for Togolese administrative procedures.
- **USSD & Blockchain Creator:** Fintech solutions and smart contract interaction for feature phones.
- **Blockchain Sponsoring Expert:** Decentralized funding and global stablecoin strategy.
- **Language Specialist:** Device-agnostic translation and global language learning tracks.

---

## 🛠️ Developer Resources

- **`AGENTS.md`:** Onboarding guide for new AI agents joining the ecosystem.
- **`CHANGELOG.md`:** Detailed version history and feature tracking.
- **`CONTRIBUTING.md`:** Technical standards and contribution workflows.
- **`requirements.txt`:** Master list of backend dependencies.
- **`setup.py`:** Package configuration for the AI Services platform.
- **`langflow_flows/`:** Visual AI workflow definitions for Langflow execution.

---
*© 2026 Yendoukoa AI. Empowering the future of autonomous intelligence.*
