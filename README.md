# Yendoukoa AI: The All-in-One Autonomous AI Ecosystem

Yendoukoa AI is a robust, scalable, and autonomous AI ecosystem designed for developers, entrepreneurs, and government institutions. We provide a unified platform for specialized AI agents across various domains.

## 🚀 Release 1.0.0: Production Launch

We are proud to announce the first major production release of Yendoukoa AI.

### Key Highlights:
- **Unified API Ecosystem:** Our production-ready API (`/api/v1`) powers multiple frontends.
- **Multi-Model Intelligence:** Integrated Gemini 1.5 Pro, GPT-4o, Claude 3.5 Sonnet, and Llama 3.1 405B.
- **Enterprise Security:** Specialized AI roles for Malware Defense, Military Strategy, and Public Security.
- **Global Accessibility:** Browser extensions, PWA support, and cross-platform desktop applications.
- **Monetization Ready:** Fully integrated Stripe subscription system.

## 🌐 Multi-Platform Accessibility

Yendoukoa AI is accessible across your devices and browsers!

-   **Browsers:** Support for **Chrome** and **Firefox** via our browser extension.
-   **Mobile:** Installable as a Progressive Web App (PWA) on **Android** and **iOS**.
-   **Desktop:** Use it as a standalone app on **Windows**, **macOS**, and **Linux** through PWA installation or our browser extension.

## 📊 Market Analysis (TAM, SAM, SOM)

Yendoukoa AI targets a high-growth intersection of Generative AI, Developer Tools, and Financial Inclusion in emerging markets.

### 🌎 TAM (Total Addressable Market) - $500B+
The global AI software and services market is projected to exceed **$500 Billion** by 2030. This includes generative AI, automated business workflows, and enterprise-grade intelligence.

### 🎯 SAM (Serviceable Addressable Market) - $50B
Our serviceable market focuses on the **Specialized AI Agent & Emerging Market FinTech** sectors. This includes developers seeking agentic workflows, SMEs in need of localized ERP/AI tools (Odoo, Sage), and the mobile-first populations in Francophone Africa requiring USSD-based financial and AI services.

### 🚀 SOM (Serviceable Obtainable Market) - 500k Active Users
Our immediate target is to capture **500,000 active users**. We are positioned to win this share by:
-   Focusing on the **Francophone African** USSD-AI niche.
-   Providing a marketplace for specialized **Agentic Workflows** (n8n, Gumloop, Lamatic.ai).
-   Serving the **Developer Community** with elite model access (Llama 3.1 405B, GPT-4o) and GitHub Copilot integrations.

## 💰 Monetization & Business Model

Yendoukoa AI is built on a sustainable business model. Our monetization strategy is three-fold:

### 1. Subscription-Based Access (SaaS)
We offer tiered subscription plans powered by **Stripe**:
-   **Free Tier:** Basic access to standard AI agents with a limited monthly credit allowance.
-   **Premium Plan:** Enhanced access to advanced models (Claude 3.5 Sonnet, GPT-4o), priority support, and a higher credit quota.
-   **Pro Plan:** Full access to elite models (Llama 3.1 405B, Nemotron-4 340B), custom workflow execution (n8n, Gumloop), and API access for developers.

### 2. Pay-Per-Use / Credit System
Our platform utilizes a flexible **Credit System** for high-compute tasks:
-   **Standard Execution:** Tasks cost a fixed amount of credits.
-   **On-Demand Top-ups:** Users can purchase additional credit packs.
-   **Transparent Usage:** Real-time credit tracking is available.

### 3. USSD & Mobile Financial Services
Specializing in emerging markets, Yendoukoa AI provides a unique **USSD & Blockchain Ecosystem**:
-   **USSD Blockchain Integration:** Financial services and blockchain interaction via USSD.
-   **Enterprise USSD Solutions:** Custom USSD gateway design and smart contract interfaces for mobile operators and banks.
-   **Transaction Security:** Specialized AI agents for fraud detection in mobile money ecosystems.

## 🏗️ Split Architecture

Yendoukoa AI uses a split architecture to optimize deployment and performance:

1.  **Frontend (Static):** The React-based marketplace frontend is hosted on **GitHub Pages** (the `docs/` directory).
2.  **Backend (API):** The Flask-based API is deployed separately.

## Sponsorship

If you find this project useful, please consider sponsoring us!

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/GYFX35)
[![Sponsor](https://img.shields.io/badge/Sponsor-Open%20Collective-7f9bff?style=for-the-badge&logo=open-collective)](https://opencollective.com/yendoukoa)
[![Sponsor](https://img.shields.io/badge/Sponsor-Patreon-f96854?style=for-the-badge&logo=patreon)](https://patreon.com/yendoukoa)

## Features

- **Software Engineer:** Generates multi-section HTML and CSS for a static website.
- **Debugger:** Lints HTML and CSS code to find errors, supports pasting code or fetching from GitHub.
- **Marketer:** Creates promotional social media posts and high-fidelity videos using Google Veo 3.1.
- **System Analyzer:** Scans a website URL for broken links.
- **Fine-Tuning Specialist:** Expert guidance on LLM fine-tuning and dataset preparation.
- **Router Capacity Architect:** Optimizes AI infrastructure with intelligent routing.
- **DeepMind Image Gen:** Generates high-fidelity images using Imagen 3.
- **DeepMind Video Creator:** Produces cinematic scripts and storyboards powered by Gemini 1.5 Pro.
- **Open Collective Specialist:** Guidance on transparent project funding.
- **Patreon Strategist:** Expert advice on creator monetization and audience engagement.
- **Cybersecurity Sentinel:** Security audits, penetration testing guidance, and threat intelligence.
- **Blockchain Sponsoring:** Expert AI for implementing decentralized funding, global stablecoin support (USDC/USDT), and cross-border sponsorship systems.

## How to Use

### Software Engineer
The Software Engineer agent uses a simple, indented syntax to define the components of a website.

**Example Prompt:**
```
title: My Photography Portfolio
header: Jane Doe | Photographer
section: About Me
  text: I am a professional photographer specializing in landscapes.
section: Gallery
  images: 4
footer: Copyright © 2024 Jane Doe
```

### Debugger
The Debugger agent can analyze code in two ways:
1.  **Paste Code:** Paste your HTML or CSS code directly into the text area.
2.  **Use a GitHub URL:** Paste the URL of a public file on GitHub into the URL input field.

### System Analyzer
Enter a full website URL (e.g., `https://example.com`) to scan the page for broken links.

## Setup and Installation

### Prerequisites
- Python 3.x
- `pip` for installing Python packages
- `node` and `npm` for the frontend

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GYFX35/AI-services.git
   cd AI-services
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file:**
   - Copy the `.env.example` to `.env` and fill in your API keys.
   ```bash
   cp .env.example .env
   ```

### Running the Application

#### 1. Backend (Flask API)

1.  **Initialize the database:**
    ```bash
    flask init-db
    ```

2.  **Start the server:**
    ```bash
    flask run --port 5001
    ```

#### 2. Frontend (React Marketplace)

1.  **Navigate to the frontend directory:**
    ```bash
    cd marketplace-frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npm run dev
    ```

## GitHub Copilot Integration
Yendoukoa AI is optimized for AI-assisted development.
- **Custom Instructions:** Provided in `.github/copilot-instructions.md`.
- **Copilot SDK:** Integrated for programmatic agentic workflows.
- **GitHub Models:** Access top-tier models (GPT-4o, Llama 3.1) via the GitHub Models API.

## 🏠 Local Project Portal

We've created a dedicated **Local Project Portal** to help you manage and explore the Yendoukoa AI ecosystem in your development environment.

- **Access the Portal:** Open `yendoukoa-ai-site/index.html` in your browser.
- **Features:**
    - **One-Click Service Launch:** Quick links to your local Flask API (Port 5001) and React Marketplace (Port 5173).
    - **Ecosystem Overview:** Visual guide to core specialists and market strategy.
    - **Developer Shortcuts:** Easy access to local documentation and GitHub resources.

## 📂 Project Manifest

For a detailed catalog of the Yendoukoa AI ecosystem, including architecture, specialized agents, and developer resources, please refer to our **[Project Artifacts Manifest](PROJECT_ARTIFACTS.md)**.

---
*© 2024 Yendoukoa AI. Empowering the future of autonomous intelligence.*
