# AI Agent: Software Engineer, Debugger, Marketer, and System Analyzer

This project is a web-based AI agent that can perform several roles to assist with software development and business tasks.

## 🚀 News Update: Multi-Platform Accessibility

We are excited to announce that Yendoukoa AI is now accessible across all your devices and browsers!

-   **Browsers:** Full support for **Chrome** and **Firefox** via our new browser extension.
-   **Mobile:** Installable as a Progressive Web App (PWA) on **Android** and **iOS**.
-   **Desktop:** Use it as a standalone app on **Windows**, **macOS**, and **Linux** through PWA installation or our browser extension.

Stay productive everywhere with Yendoukoa AI!

## Production Ready

Yendoukoa AI is now in full production. We have moved beyond the demo phase to provide a robust, scalable platform for professional AI services.

*   **Official Website:** [https://yendoukoa.ai](https://yendoukoa.ai)
*   **Enterprise Solutions:** Contact us for custom AI integrations.

## Subscription & Monetization

We offer professional-grade AI services via a flexible subscription model. Support our growth and unlock premium features.

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/GYFX35)
[![Sponsor](https://img.shields.io/badge/Sponsor-Stripe-626cd9?style=for-the-badge&logo=stripe)](https://buy.stripe.com/example)

### How It Works

Our platform connects to multiple state-of-the-art AI services to provide a suite of tools for developers and entrepreneurs. The core of the application is a Flask-based backend that serves a high-performance React frontend. The AI functionalities are powered by industry leaders including Google Vertex AI, OpenAI, Anthropic, and NVIDIA, enabling elite features like code generation, debugging, and strategic analysis. The platform is designed for enterprise-grade extensibility.

## Features

- **Software Engineer:** Generates multi-section HTML and CSS for a static website based on a structured text prompt.
- **Debugger:** Lints HTML and CSS code to find basic errors. Can analyze pasted code or fetch a file directly from a GitHub URL.
- **Marketer:** Creates promotional social media posts from a business description.
- **System Analyzer:** Scans a website URL for broken links and suggests search queries to find solutions.

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

1. **Initialize the database:**
   ```bash
   flask init-db
   ```

2. **Start the server:**
   ```bash
   flask run
   ```

3. **Open your web browser:**
   Navigate to `http://127.0.0.1:5000` to access the application.

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

### Enterprise Deployment
- **Production Ready:** This repository includes all necessary configuration for professional deployment.
- **Scalable Architecture:** Built to handle production workloads with high availability.
- **One-Click Setup:** Use the provided Docker and Cloud configurations to get your production environment live in minutes.

---
*Developed for [Hackathon Name]*
