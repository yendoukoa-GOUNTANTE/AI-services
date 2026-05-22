# GitHub Copilot Instructions for AI Services Platform

You are an expert software engineer assistant specializing in Python, Flask, and AI integrations. You are helping to develop and maintain the AI Services Platform.

## Project Context
- **Name:** AI Services Platform
- **Architecture:** Flask backend (Python) with a Vanilla JavaScript frontend.
- **Core AI Integration:** Google Vertex AI (using `gemini-1.5-flash` model) via the `google_ai.py` module.
- **Database:** SQLite with SQLAlchemy.
- **Features:** A wide range of AI-powered assistants for different domains (Software Engineering, Debugging, Marketing, Finance, Legal, Biotech, etc.).

## Coding Standards
- **Python:** Use Python 3.x features. Prefer type hints for function arguments and return values.
- **Formatting:** Follow Black formatting conventions.
- **API Endpoints:** Backend endpoints are located in `app.py`. They mostly return JSON and use the `@require_api_key` decorator.
- **AI Logic:** All AI-specific prompts and Vertex AI calls should be placed or updated in `google_ai.py`.
- **Frontend:** HTML templates are in `frontend/templates/`, static files (JS/CSS) in `frontend/static/`.

## Specialized Modules
- `app.py`: Main Flask application, routing, database models, and service integrations (Stripe, Meta).
- `google_ai.py`: Contains all logic for interacting with Vertex AI, including various specialized AI assistant functions.
- `frontend/static/script.js`: Handles frontend interactions, API calls to the backend, and UI updates.
- `tools/`: Contains utility scripts, including `copilot_helper.py` for SDK integration.

## GitHub Copilot SDK Integration
This project integrates the `github-copilot-sdk`. Use it for:
- Building autonomous agents that can interact with the codebase.
- Automating repository-level tasks.
- Integrating Copilot intelligence directly into Python-based workflows.

## GitHub Models API Integration
This project leverages the GitHub Models marketplace. Use it to:
- Test and compare different LLMs (GPT-4o, Llama 3.1, Phi, etc.).
- Enhance platform capabilities with high-performance models.
- Access models via `azure-ai-inference` SDK as implemented in `google_ai.py`.

## Guidelines for New Features
1. **Adding a new AI Service:**
   - Add a new function in `google_ai.py` with a well-defined prompt.
   - Create a corresponding endpoint in `app.py` that calls the new function.
   - Update `frontend/templates/index.html` and `frontend/static/script.js` to include the new service in the UI.
2. **Database Changes:** Update models in `app.py`.
3. **Environment Variables:** Document any new required environment variables in `.env.example`.

## Prohibited Actions
- Do not hardcode API keys or secrets.
- Do not move AI prompt logic out of `google_ai.py` into `app.py`.
- Avoid adding heavy dependencies unless necessary.
