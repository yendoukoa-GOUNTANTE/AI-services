# Yendoukoa AI: The All-in-One Autonomous AI Ecosystem

Yendoukoa AI has officially transitioned from a demo project into a **Production Startup**. We provide a robust, scalable, and autonomous AI ecosystem designed for developers, entrepreneurs, and government institutions.

## 🚀 Release 1.0.0: Production Launch

We are proud to announce the first major production release of Yendoukoa AI.

### Key Highlights:
- **Official Startup Status:** Transitioned from a project to a full-scale AI service platform.
- **Unified API Ecosystem:** Our own production-ready API (`/api/v1`) powering multiple frontends.
- **Multi-Model Intelligence:** Integrated Gemini 1.5 Pro, GPT-4o, Claude 3.5 Sonnet, and Llama 3.1 405B.
- **Enterprise Security:** Specialized AI roles for Malware Defense, Military Strategy, and Public Security.
- **Global Accessibility:** Browser extensions, PWA support, and cross-platform desktop applications.
- **Monetization Ready:** Fully integrated Stripe subscription system.

## 🌐 Multi-Platform Accessibility

We are excited to announce that Yendoukoa AI is now accessible across all your devices and browsers!

-   **Browsers:** Full support for **Chrome** and **Firefox** via our new browser extension.
-   **Mobile:** Installable as a Progressive Web App (PWA) on **Android** and **iOS**.
-   **Desktop:** Use it as a standalone app on **Windows**, **macOS**, and **Linux** through PWA installation or our browser extension.

Stay productive everywhere with Yendoukoa AI!

## 📊 Market Analysis (TAM, SAM, SOM)

Yendoukoa AI targets a high-growth intersection of Generative AI, Developer Tools, and Financial Inclusion in emerging markets.

### 🌎 TAM (Total Addressable Market) - $500B+
The global AI software and services market is projected to exceed **$500 Billion** by 2030 (Source: [Gartner](https://www.gartner.com), [PwC](https://www.pwc.com)). This includes the entire landscape of generative AI, automated business workflows, and enterprise-grade intelligence across all sectors.

### 🎯 SAM (Serviceable Addressable Market) - $50B
Our serviceable market focuses on the **Specialized AI Agent & Emerging Market FinTech** sectors. The AI Agents market alone is projected to reach **$50B+** by 2030 (Source: [MarketsandMarkets](https://www.marketsandmarkets.com)). This includes developers seeking agentic workflows, SMEs in need of localized ERP/AI tools (Odoo, Sage), and the massive mobile-first populations in Francophone Africa requiring USSD-based financial and AI services.

### 🚀 SOM (Serviceable Obtainable Market) - 500k Active Users
Our immediate target is to capture **500,000 active users** within the first 3 years. We are uniquely positioned to win this share by:
-   Dominating the **Francophone African** USSD-AI niche.
-   Providing the go-to marketplace for specialized **Agentic Workflows** (n8n, Gumloop, Lamatic.ai).
-   Serving the **Developer Community** with elite model access (Llama 3.1 405B, GPT-4o) and GitHub Copilot integrations.

## 💰 Monetization & Business Model

Yendoukoa AI is built on a sustainable business model designed to provide high-quality AI services while ensuring continuous innovation and infrastructure stability. Our monetization strategy is three-fold:

### 1. Subscription-Based Access (SaaS)
We offer tiered subscription plans powered by **Stripe** to cater to different user needs:
-   **Free Tier:** Basic access to standard AI agents with a limited monthly credit allowance.
-   **Premium Plan ($19/mo):** Enhanced access to advanced models (Claude 3.5 Sonnet, GPT-4o), priority support, and a higher credit quota.
-   **Pro Plan ($49/mo):** Full access to elite models (Llama 3.1 405B, Nemotron-4 340B), custom workflow execution (n8n, Gumloop), and API access for developers.

### 2. Pay-Per-User / Credit System
Our platform utilizes a flexible **Credit System** for high-compute tasks. This ensures fair usage and allows users to pay only for what they consume:
-   **Standard Execution:** Standard agent tasks cost a fixed amount of credits (typically 50 credits per use).
-   **On-Demand Top-ups:** Users can purchase additional credit packs if they exceed their plan's monthly allocation.
-   **Transparent Usage:** Real-time credit tracking is available in the user dashboard.

### 3. USSD & Mobile Financial Services
Specializing in emerging markets, Yendoukoa AI provides a unique **USSD & Blockchain Ecosystem**:
-   **USSD Blockchain Integration:** We enable financial services and blockchain interaction via USSD, making advanced tech accessible to feature phone users without internet.
-   **Enterprise USSD Solutions:** Custom USSD gateway design and smart contract interfaces for mobile operators and banks.
-   **Transaction Security:** Specialized AI agents for fraud detection and transaction optimization in mobile money ecosystems.

## GitHub Site Web View & Split Architecture

Yendoukoa AI now uses a split architecture to optimize deployment and performance:

1.  **Frontend (Static):** The React-based marketplace frontend is hosted on **GitHub Pages** (the `docs/` directory). This provides a fast, globally distributed "Web View" of the platform.
2.  **Backend (API):** The Flask-based API is deployed separately (e.g., on Google Cloud Run or AWS).

This split allows for independent scaling and simplifies the deployment of the frontend to GitHub's static hosting.

## Devpost Challenge Submission

This project is a submission for the **[Name of Devpost Challenge]**.

*   **Live Demo (Frontend):** [https://yendoukoa.ai](https://yendoukoa.ai)
*   **API Documentation:** [https://yendoukoa.ai/api/v1](https://yendoukoa.ai/api/v1) (when backend is active)
*   **Video Walkthrough:** [Link to Video Walkthrough]

## Sponsorship

If you find this project useful, please consider sponsoring us!

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/GYFX35)
[![Sponsor](https://img.shields.io/badge/Sponsor-Open%20Collective-7f9bff?style=for-the-badge&logo=open-collective)](https://opencollective.com/yendoukoa)
[![Sponsor](https://img.shields.io/badge/Sponsor-Patreon-f96854?style=for-the-badge&logo=patreon)](https://patreon.com/yendoukoa)
[![Sponsor](https://img.shields.io/badge/Sponsor-Stripe-626cd9?style=for-the-badge&logo=stripe)](https://buy.stripe.com/example)

### How It Works

Our platform connects to multiple AI services to provide a suite of tools for developers and entrepreneurs. The core of the application is a Flask-based backend that serves a user-friendly frontend. The AI functionalities are powered by Google's Vertex AI, enabling features like code generation, debugging, and content creation. The platform is designed to be easily extensible, allowing for the integration of new AI-powered tools in the future.

## Features

- **Software Engineer:** Generates multi-section HTML and CSS for a static website based on a structured text prompt.
- **Debugger:** Lints HTML and CSS code to find basic errors. Can analyze pasted code or fetch a file directly from a GitHub URL.
- **Marketer:** Creates promotional social media posts from a business description.
- **System Analyzer:** Scans a website URL for broken links and suggests search queries to find solutions.
- **Fine-Tuning Specialist:** Provides expert guidance on LLM fine-tuning, dataset preparation, and performance optimization.
- **Router Capacity Architect:** Optimizes AI infrastructure with intelligent routing and automated capacity management.
- **DeepMind Image Gen:** Generates high-fidelity images using Google's DeepMind Imagen 3 technology.
- **DeepMind Video Creator:** Produces cinematic scripts, storyboards, and advanced video creative directions powered by DeepMind's flagship Gemini 1.5 Pro.
- **Open Collective Specialist:** Provides elite guidance on transparent project funding and community-led financial management using Open Collective.
- **Patreon Strategist:** Offers expert advice on creator monetization, membership tiers, and audience engagement strategies for Patreon.

## How to Use

### Software Engineer
The Software Engineer agent uses a simple, indented syntax to define the components of a website. Provide a description in the "Software-Engineer" text box, and the agent will return the HTML and CSS code in the response box below.

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
1.  **Paste Code:** Paste your HTML or CSS code directly into the large text area.
2.  **Use a GitHub URL:** Paste the URL of a public file on GitHub into the smaller URL input field.

The agent will automatically fetch the code from the URL and analyze it.

### System Analyzer
Enter a full website URL (e.g., `https://example.com`) to scan the page for broken links.

## Setup and Installation

### Prerequisites
- Python 3.x
- `pip` for installing Python packages

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

2.  **Set the API URL (Optional for local dev):**
    Create a `.env.local` file:
    ```
    VITE_API_BASE_URL=http://localhost:5001/api/v1
    ```

3.  **Start the development server:**
    ```bash
    npm run dev
    ```

4.  **Open your web browser:**
    Navigate to the URL provided by Vite (usually `http://localhost:5173`).

## Developer Deployment and Integration

This project is configured for easy use across multiple platforms.

### Git and GitLab
- **Git Attributes:** Consistent line endings are managed via `.gitattributes`.
- **GitLab CI/CD:** A `.gitlab-ci.yml` is provided for automated builds, testing with `pytest`, and linting.
  - Simply push to GitLab to trigger the pipeline.
  - Ensure you set your environment variables (from `.env.example`) in GitLab CI/CD settings.

### Firebase and Firebase Studio
- **Hosting and Functions:** Use `firebase.json` and `.firebaserc` for deployment.
- **Firebase Studio:** Compatible with Firebase tools for project management.
- **Deploy command:**
  ```bash
  firebase deploy
  ```

### AWS (Amazon Web Services)
- **Containerized Deployment:** A `Dockerfile` and `docker-compose.yml` are included.
- **AWS SAM (Serverless Application Model):** A `template.yaml` is provided for deploying as an AWS Lambda function with API Gateway.
- **Deploy via SAM:**
  ```bash
  sam build
  sam deploy --guided
  ```

### Google Cloud Platform (GCP)
- **App Engine:** Deploy using `app.yaml`.
  ```bash
  gcloud app deploy
  ```
- **Cloud Run via Cloud Build:** Use `cloudbuild.yaml` for automated container builds and deployment.
  ```bash
  gcloud builds submit --config cloudbuild.yaml
  ```

### Lablab.ai and Devpost
- **Hackathon Ready:** This repository includes all necessary configuration for quick cloning and deployment during hackathons.
- **Project Story:** (Add your project's inspiration and goals here for your submission).
- **One-Click Setup:** Use the provided Docker and Cloud configurations to get your demo live in minutes.

### GitHub Copilot Integration
Yendoukoa AI is optimized for AI-assisted development using GitHub Copilot.
- **Custom Instructions:** We provide tailored Copilot instructions in `.github/copilot-instructions.md` to help Copilot understand our architecture and coding standards.
- **VS Code Support:** Recommended extensions (including Copilot and Copilot Chat) are defined in `.vscode/extensions.json`.
- **Copilot SDK:** We have integrated the GitHub Copilot SDK for programmatic agentic workflows.
  - Install the SDK: `pip install -r requirements-dev.txt`
  - Example helper: `python tools/copilot_helper.py` (Requires `GITHUB_TOKEN`)
- **GitHub Models:** Access top-tier models (GPT-4o, Llama 3.1) directly within the Yendoukoa AI platform via the GitHub Models API.
- **Copilot Chat API:** Integration with the Copilot Chat API for deep codebase intelligence.

---
*© 2024 Yendoukoa AI. Empowering the future of autonomous intelligence.*
