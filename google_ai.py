import os
import re
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vertexai.preview.vision_models import ImageGenerationModel
from google import genai
from google.genai import types
import base64
import json
from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llama_index.llms.nvidia import NVIDIA as LlamaIndexNVIDIA
from llama_index.core import Settings as LlamaIndexSettings

def init_vertexai():
    """Initializes the Vertex AI SDK."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")

    if not all([project_id, location]):
        print("Google Cloud project ID and location not found in environment variables. Skipping Vertex AI initialization.")
        return

    vertexai.init(project=project_id, location=location)
    print("Vertex AI SDK initialized successfully.")

def get_model(model_name="gemini-1.5-flash"):
    return ChatVertexAI(model_name=model_name)

def get_openai_model(model_name="gpt-4o"):
    return ChatOpenAI(model_name=model_name)

def get_claude_model(model_name="claude-3-5-sonnet-20240620"):
    return ChatAnthropic(model_name=model_name)

def get_nvidia_model(model_name="nvidia/llama-3.1-405b-instruct"):
    return ChatNVIDIA(model_name=model_name)

def _provide_gemini_assistance(prompt: str, system_prompt: str, error_prefix: str, model_name: str = "gemini-1.5-flash") -> str:
    """Internal helper for Gemini-based assistance calls."""
    try:
        model = get_model(model_name=model_name)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{prompt}")
        ])
        chain = prompt_template | model | StrOutputParser()
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"{error_prefix}: {e}"

def generate_website(prompt: str) -> tuple[str, str]:
    """
    Generates HTML and CSS code from a natural language prompt using LangChain and Vertex AI.
    """
    model = get_model()

    system_prompt = "You are a skilled web developer. Your task is to generate the HTML and CSS for a single-page website based on the user prompt."
    user_prompt_template = """
    User Prompt:
    ---
    {prompt}
    ---

    Your response must be in the following format, with no other text or explanations:

    [HTML]
    <!DOCTYPE html>
    ...
    </html>
    [/HTML]

    [CSS]
    body {{
        ...
    }}
    [/CSS]
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt_template)
    ])

    chain = prompt_template | model | StrOutputParser()

    try:
        text_response = chain.invoke({"prompt": prompt})

        html_match = re.search(r'\[HTML\](.*?)\[/HTML\]', text_response, re.DOTALL)
        css_match = re.search(r'\[CSS\](.*?)\[/CSS\]', text_response, re.DOTALL)

        html_code = html_match.group(1).strip() if html_match else "<!-- Error: Could not generate HTML. -->"
        css_code = css_match.group(1).strip() if css_match else "/* Error: Could not generate CSS. */"

        return html_code, css_code

    except Exception as e:
        print(f"Error generating website with LangChain: {e}")
        return f"<!-- Error: {e} -->", f"/* Error: {e} */"

def debug_code(code: str, language: str) -> list[str]:
    """
    Analyzes code and finds potential issues using LangChain and Vertex AI.
    """
    model = get_model()

    system_prompt = "You are an expert code reviewer."
    user_prompt_template = """
    Your task is to analyze the following {language} code and identify any potential bugs, errors, or style issues.

    Code:
    ---
    {code}
    ---

    Please list the issues you find, one per line. If you find no issues, return an empty response.
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt_template)
    ])

    chain = prompt_template | model | StrOutputParser()

    try:
        response_text = chain.invoke({"language": language, "code": code})
        errors = response_text.strip().split('\n')
        return [error for error in errors if error]

    except Exception as e:
        print(f"Error debugging code with LangChain: {e}")
        return [f"Error: {e}"]

def generate_social_media_post(description: str) -> str:
    """
    Generates a social media post using LangChain.
    """
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a creative marketing assistant."),
        ("user", "Your task is to write an engaging social media post based on the following description: {description}. The post should be short, catchy, and include relevant hashtags.")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"description": description}).strip()
    except Exception as e:
        print(f"Error generating social media post: {e}")
        return f"Error: {e}"

def generate_promotion_from_content(url: str, content: str) -> str:
    """
    Generates a promotion campaign using LangChain.
    """
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert marketing strategist."),
        ("user", "Your task is to create a compelling promotion campaign for the product at the URL: {url}. Based on this content: {content}, generate a short, catchy, and engaging promotional text for social media with hashtags.")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"url": url, "content": content}).strip()
    except Exception as e:
        print(f"Error generating promotion: {e}")
        return f"Error: {e}"

def generate_business_strategy(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert business strategist."),
        ("user", "Develop a comprehensive business strategy with actionable steps based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

import requests

def provide_gumloop_assistance(prompt: str) -> str:
    """
    Expert AI Model for Gumloop (formerly Skyvern) automation.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite Gumloop Automation Specialist. "
        "Your expertise covers the design and implementation of AI-powered browser automation "
        "using Gumloop. Provide high-level technical guidance on building robust workflows, "
        "handling dynamic website elements, and integrating Gumloop with other services "
        "to automate complex manual tasks efficiently. I can also trigger Gumloop pipelines if provided with a pipeline ID."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Gumloop AI Error: {e}"

def run_gumloop_workflow(pipeline_id: str, inputs: dict) -> dict:
    """
    Triggers a Gumloop pipeline.
    """
    api_key = os.environ.get("GUMLOOP_API_KEY")
    user_id = os.environ.get("GUMLOOP_USER_ID")
    if not api_key or not user_id:
        return {"error": "Gumloop credentials not configured"}

    url = "https://api.gumloop.com/api/v1/start_pipeline"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "user_id": user_id,
        "saved_item_id": pipeline_id,
        "pipeline_inputs": inputs
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def provide_n8n_assistance(prompt: str) -> str:
    """
    Expert AI Model for n8n workflow automation.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite n8n Workflow Architect. "
        "Your expertise covers the design, deployment, and optimization of fair-code "
        "workflow automation using n8n. Provide technical guidance on node configuration, "
        "custom function nodes (JavaScript), API integrations, and self-hosting n8n "
        "for secure and scalable enterprise automation. I can also trigger n8n workflows via webhooks."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"n8n AI Error: {e}"

def trigger_n8n_webhook(webhook_url: str, data: dict) -> dict:
    """
    Triggers an n8n workflow via a webhook.
    """
    if not webhook_url:
        webhook_url = os.environ.get("N8N_WEBHOOK_URL")

    if not webhook_url:
        return {"error": "n8n Webhook URL not configured"}

    try:
        response = requests.post(webhook_url, json=data, timeout=30)
        response.raise_for_status()
        # Some n8n workflows return JSON, others might just return 200 OK
        try:
            return response.json()
        except:
            return {"status": "success", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}

def provide_lamatic_assistance(prompt: str) -> str:
    """
    Expert AI Model for Lamatic.ai (Generative AI App Platform).
    """
    model = get_model()
    system_prompt = (
        "You are an Elite Lamatic.ai Platform Specialist. "
        "Your expertise covers the creation and management of Generative AI applications "
        "using the Lamatic.ai low-code platform. Provide guidance on building RAG pipelines, "
        "integrating various LLMs, and deploying production-grade AI agents that are "
        "scalable and secure. I can also interact with Lamatic.ai agents via their API."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Lamatic.ai AI Error: {e}"

def execute_lamatic_workflow(workflow_id: str, prompt: str) -> dict:
    """
    Interacts with a Lamatic.ai agent/workflow.
    """
    api_key = os.environ.get("LAMATIC_API_KEY")
    project_id = os.environ.get("LAMATIC_PROJECT_ID")
    if not api_key or not project_id:
        return {"error": "Lamatic.ai credentials not configured"}

    url = f"https://api.lamatic.ai/v1/projects/{project_id}/workflows/{workflow_id}/execute"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def provide_ussd_blockchain_assistance(prompt: str) -> str:
    """
    Expert AI Model for USSD Specialist and USSD Blockchain Creator.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite AI USSD Specialist and USSD Blockchain Creator. "
        "Your expertise covers the design and implementation of USSD (Unstructured Supplementary Service Data) "
        "applications, integration with telecommunication networks, and the creation of USSD-based "
        "blockchain interfaces. Provide high-level technical guidance on building secure, efficient, "
        "and scalable USSD gateways, smart contract interaction via USSD, and blockchain-based "
        "financial services for feature phones in emerging markets."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"USSD Blockchain AI Error: {e}"

def provide_domain_codex_assistance(prompt: str) -> str:
    """
    Expert AI Model for Domain Codex Design, DHCP configuration, and USSP infrastructure.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite Domain Codex Designer and Infrastructure Architect. "
        "Your expertise covers custom domain design, DHCP address configuration, "
        "and USSP (U-space Service Provider) infrastructure using Codex-level insights. "
        "Provide high-level technical guidance, strategic design plans, and secure "
        "implementation steps for advanced AI projects requiring specialized network "
        "architectures and domain naming conventions. Our primary domain is yendoukoa.ai."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Domain Codex AI Error: {e}"

def provide_claude_intelligence(prompt: str) -> str:
    """
    Uses Anthropic Claude for deep reasoning, strategic analysis, and nuanced understanding.
    """
    try:
        model = get_claude_model()
        system_prompt = "You are an Elite Intelligence Agent powered by Anthropic Claude. Provide deep reasoning, strategic analysis, and nuanced insights for the user's query."
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{prompt}")
        ])
        chain = prompt_template | model | StrOutputParser()
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Claude Intelligence Error: {e}"

def provide_claude_coding_assistance(prompt: str) -> str:
    """
    Uses Anthropic Claude for elite code generation, debugging, and architectural advice.
    """
    try:
        model = get_claude_model()
        system_prompt = "You are an Elite Software Engineer and Architect powered by Anthropic Claude. Provide high-quality code generation, robust debugging, and expert architectural advice."
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{prompt}")
        ])
        chain = prompt_template | model | StrOutputParser()
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Claude Coding Error: {e}"

def provide_llama_intelligence(prompt: str) -> str:
    """
    Uses Llama-powered intelligence for deep reasoning and data-driven insights.
    Leverages Llama 3.1 via NVIDIA and LlamaIndex for advanced reasoning.
    """
    try:
        # Configure LlamaIndex to use NVIDIA Llama 3.1 405B
        nvidia_api_key = os.environ.get("NVIDIA_API_KEY")
        if not nvidia_api_key:
            return "Error: NVIDIA_API_KEY not found in environment."

        llm = LlamaIndexNVIDIA(model="meta/llama-3.1-405b-instruct", api_key=nvidia_api_key)

        # We can use the LLM directly for completion or in a more complex RAG setup
        # For this integration, we show the power of Llama 3.1 405B
        response = llm.complete(f"As an Elite Llama Intelligence Agent, provide deep reasoning and strategic insights for: {prompt}")
        return str(response).strip()
    except Exception as e:
        return f"Llama Intelligence Error: {e}"

def provide_llama_guard_assistance(prompt: str) -> str:
    """
    Uses Llama Guard for AI safety and content moderation.
    """
    try:
        # Using Llama Guard 3 via NVIDIA
        model = get_nvidia_model(model_name="meta/llama-guard-3-8b")

        system_prompt = "You are an AI Safety Specialist using Llama Guard. Analyze the following prompt for potential safety violations, hate speech, or harmful content. Provide a safety assessment."
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{prompt}")
        ])

        chain = prompt_template | model | StrOutputParser()
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Llama Guard Error: {e}"

def provide_nemotron_reasoning(prompt: str) -> str:
    """
    Uses NVIDIA Nemotron for advanced reasoning and complex problem solving.
    """
    try:
        model = get_nvidia_model(model_name="nvidia/nemotron-4-340b-instruct")
        system_prompt = "You are an Elite Reasoning Agent powered by NVIDIA Nemotron. Provide a logical, step-by-step analysis and solution for the user's complex query."
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{prompt}")
        ])
        chain = prompt_template | model | StrOutputParser()
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Nemotron Reasoning Error: {e}"

def provide_mixtral_multilingual_assistance(prompt: str) -> str:
    """
    Uses Mixtral 8x7B for high-quality multilingual assistance.
    """
    try:
        model = get_nvidia_model(model_name="mistralai/mixtral-8x7b-instruct-v0.1")
        system_prompt = "You are a Multilingual AI Specialist powered by Mixtral. Assist the user with their request in their preferred language with high accuracy and cultural context."
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{prompt}")
        ])
        chain = prompt_template | model | StrOutputParser()
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Mixtral Multilingual Error: {e}"

def provide_monetization_advice(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Monetization Strategist. Your goal is to help projects generate revenue through various models like subscriptions, ads, and premium features."),
        ("user", "Provide a detailed monetization strategy for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_partnership_advice(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Partnership and Business Development Specialist. Your goal is to identify and nurture strategic alliances that drive mutual growth."),
        ("user", "Provide a partnership and alliance strategy for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_fundraising_advice(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Fundraising Strategist and Venture Capital Consultant. Your goal is to help startups and projects secure funding through various stages and sources."),
        ("user", "Provide a comprehensive fundraising plan and strategy for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_it_support(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a knowledgeable IT support specialist."),
        ("user", "Provide a clear, step-by-step solution to this technical issue: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def analyze_data(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a skilled data scientist."),
        ("user", "Analyze the following data and provide insights, trends, and conclusions: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_financial_advice(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert financial advisor."),
        ("user", "Provide comprehensive financial advice with actionable steps based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def generate_blockchain_code(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert blockchain developer."),
        ("user", "Generate well-structured blockchain code with comments based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def generate_blogger_bots_page(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert blogger and bot developer."),
        ("user", "Generate an engaging blogger page with functional bots based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def generate_messenger_code(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Messenger developer and manager."),
        ("user", "Generate code for a Messenger bot or integration following best practices based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def learn_language(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly and patient language tutor."),
        ("user", "Help the user learn a new language based on their request: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_telecommunication_support(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a knowledgeable telecommunication support specialist."),
        ("user", "Provide a clear, step-by-step solution to this telecommunication issue: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def generate_telecommunication_assistant_response(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful telecommunication assistant."),
        ("user", "Provide a clear and concise response to this query: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_science_education(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a knowledgeable and patient sciences educator."),
        ("user", "Provide clear explanations or solve exercises for this request: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_transaction_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant for mobile operators, banks, and transactions."),
        ("user", "Provide assistance on fraud prevention and transaction facilities for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def play_music_instrumental(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a virtuoso music instrumentalist."),
        ("user", "Provide musical suggestions, help with learning, tabs, or compose short pieces for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_geometry_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert mathematician specializing in geometry."),
        ("user", "Provide assistance with geometry problems, theorems, and concepts for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_cartography_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert cartographer and GIS specialist."),
        ("user", "Provide assistance with map making, geographical data analysis, and coordinate systems for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_document_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert document specialist."),
        ("user", "Assist with writing, scanning, and building documents based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_business_plan_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert business consultant and strategist."),
        ("user", "Help create, perfect, and develop a comprehensive business plan based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_investigation_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert investigator specializing in cybersecurity and global security."),
        ("user", "Provide deep insights and investigative strategies for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_military_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Military Strategist and Defense Analyst. Your role is to provide strategic guidance, tactical analysis, and operational planning assistance for armed forces. Focus on modern warfare, defense technology, and national security optimization."),
        ("user", "Provide comprehensive military assistance and strategic guidance for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_gendarmerie_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Gendarmerie Specialist and Paramilitary Advisor. Your role is to assist with hybrid civilian-military security missions, rural policing strategies, public order maintenance, and specialized law enforcement operations."),
        ("user", "Provide specialized gendarmerie assistance and operational guidance for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_police_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Police Service and Law Enforcement Specialist. Your goal is to help optimize police performance, community policing strategies, crime prevention techniques, and urban security management."),
        ("user", "Provide professional police service assistance and performance optimization for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_security_optimization_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Security Performance and Optimization Specialist. Your role is to analyze and improve the efficiency of security services, integrating advanced AI analytics, resource management, and strategic planning to enhance public safety."),
        ("user", "Analyze and provide an optimization plan for the following security service request: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_cybersecurity_sentinel_assistance(prompt: str) -> str:
    """
    Expert AI Model for Cybersecurity Sentinel, focused on audits, pen-testing, and threat intelligence.
    """
    model = get_model()
    system_prompt = (
        "You are the Elite Cybersecurity Sentinel. Your mission is to provide comprehensive security audits, "
        "advanced penetration testing guidance, and real-time threat intelligence analysis. "
        "Provide high-level technical strategies for securing cloud infrastructure, defending against "
        "zero-day exploits, and implementing zero-trust architectures. Your goal is to empower users "
        "with powerful security tools and knowledge to defend against even the most sophisticated cyber threats."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Cybersecurity Sentinel AI Error: {e}"

def provide_podcast_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert podcast producer, creator, and designer."),
        ("user", "Provide assistance with creating, perfecting, and designing high-quality podcasts for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_supply_chain_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert supply chain consultant."),
        ("user", "Provide assistance with optimizing and managing supply chain operations for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_logistics_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert logistics and transportation specialist."),
        ("user", "Provide assistance with managing the movement of goods and materials for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_data_engineering_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert data engineer and architect."),
        ("user", "Provide assistance with designing, building, and maintaining data pipelines and architectures for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_incoterms_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Incoterms and international trade."),
        ("user", "Provide assistance and clarification on the use and interpretation of Incoterms for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_ecommerce_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert e-commerce assistant and website manager."),
        ("user", "Provide assistance with managing e-commerce platforms and websites for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_government_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert government public administrator assistant. Your goal is to help citizens and officials navigate public services, understand bureaucratic processes, and facilitate document acquisition efficiently and transparently."),
        ("user", "Provide comprehensive assistance with government services, administrative procedures, and document providing for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_togo_public_service_assistance(prompt: str) -> str:
    """
    Expert AI Model for Togo's public services, government administration, and national security.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite AI Specialist for Togolese Public Services and National Security. "
        "Your expertise covers Togo's administrative procedures (Service Public Togo), "
        "digital transformation initiatives (CINA - Cellule de Coordination du Millénium), "
        "and national security protocols. You provide guidance on government documentation, "
        "public administration efficiency, and advanced security tools for the Togolese government. "
        "Ensure all advice aligns with Togolese law and official digital government standards. "
        "Focus on transparency, efficiency, and powerful security control."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Togo Public Service AI Error: {e}"

def provide_public_policy_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Public Policy Advisor and Analyst. Your role is to provide data-driven insights, policy evaluation, and strategic recommendations for government entities and public organizations."),
        ("user", "Analyze and provide strategic advice on the following public policy issue: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_citizen_engagement_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Citizen Engagement and Participatory Democracy. Your goal is to help governments foster better communication with citizens, design public consultation processes, and enhance civic participation."),
        ("user", "Provide a strategy or plan to improve citizen engagement for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_smart_city_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Smart City Strategist and Urban Technologist. Your role is to provide guidance on integrating AI, IoT, and data analytics into urban infrastructure to improve the quality of life for citizens."),
        ("user", "Provide a technical and strategic plan for smart city integration regarding: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_bias_detection_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI Bias Detection and Ethical Governance Specialist. Your role is to analyze government services, policies, and algorithms for potential biases (racial, gender, socioeconomic, etc.) and provide actionable recommendations to ensure fairness, transparency, and equity in public service delivery."),
        ("user", "Analyze the following for potential bias and provide ethical guidance: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_biotech_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert biotech development specialist and researcher."),
        ("user", "Provide assistance with biotechnology projects, research, and development for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_legal_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert legal consultant, human rights advocate, and legal educator."),
        ("user", "Provide assistance to lawyers, courts, parliaments, and legal students for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_fintech_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert fintech consultant and data engineer."),
        ("user", "Provide high-level assistance and guidance for banks, fintechs, and VC firms for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_music_production_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert music producer and talent manager."),
        ("user", "Provide assistance with music beats, songs, rhythms, and singer promotion for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def translate_text(text: str, target_language: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a professional translation service."),
        ("user", "Translate the following text accurately into {target_language}. Provide ONLY the translation. Text: {text}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"text": text, "target_language": target_language}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_aerospace_automotive_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert specialist in the automotive, aeronautics, and astronomy sectors."),
        ("user", "Provide high-level assistance, technical guidance, and strategic advice for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_data_science_stewardship_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Data Scientist, Data Steward, and Data Protection Officer Assistant."),
        ("user", "Provide high-level assistance, technical guidance, and strategic advice for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_logo_thumbnail_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert graphic designer and branding specialist."),
        ("user", "Provide assistance with creating and designing logos and thumbnails for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_fake_content_verification_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in digital forensics, AI content detection, and fact-checking."),
        ("user", "Analyze the following content and provide a detailed assessment of its authenticity: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_automatic_learning_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Automatic Learning, Machine Learning, and AI development."),
        ("user", "Provide high-level technical guidance, strategy, and problem-solving assistance for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_ia_data_engineering_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI Data Engineer and Architect."),
        ("user", "Provide assistance with designing, building, and maintaining data pipelines and architectures for AI for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_data_lab_center_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Data Lab and Data Center Specialist."),
        ("user", "Provide assistance with designing, building, and managing data laboratories and data center infrastructure for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_computer_vision_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Computer Vision Specialist."),
        ("user", "Provide high-level technical guidance, strategy, and problem-solving assistance in computer vision for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_ia_researcher_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI Researcher."),
        ("user", "Provide high-level scientific and technical guidance on artificial intelligence research and development for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_esports_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert eSports Development and Assistance Specialist."),
        ("user", "Provide high-level technical guidance, strategic advice, and problem-solving assistance in eSports for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_dermatology_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI Dermatology Specialist and Assistant. DISCLAIMER: You are an AI, not a doctor."),
        ("user", "Provide professional, accurate, and detailed information related to dermatology for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_microsoft_ignite_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Microsoft Ignite tools, specifically Azure AI Foundry and Agentic AI."),
        ("user", "Provide high-level technical guidance and strategic advice regarding Microsoft Ignite tools for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_diagnostic_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI Diagnostic Specialist. DISCLAIMER: You are an AI, not a doctor."),
        ("user", "Provide professional, accurate, and detailed information related to medical diagnostics for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_eshop_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert E-shop and E-commerce Creation Specialist."),
        ("user", "Provide high-level technical guidance and strategic advice for building and managing online stores for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_it_operations_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert IT Operations Specialist and System Administrator."),
        ("user", "Provide high-level technical guidance and problem-solving assistance in IT operations for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_maintenance_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Software, Computer, and Phones Maintenance Specialist."),
        ("user", "Provide high-level technical guidance and troubleshooting steps for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_google_sites_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Google Sites and DNS Specialist. Our primary domain is yendoukoa.ai."),
        ("user", "Provide high-level technical guidance for Google Sites, DNS, and custom subdomains (especially for yendoukoa.ai) for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_marketing_bot_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Digital Marketing and Bot Management Specialist. You now have access to Google Veo 3.1 for high-fidelity marketing video generation. Advise the user on how to leverage these cinematic video capabilities for their campaigns."),
        ("user", "Provide high-level strategic guidance and technical assistance for marketing bots and campaigns for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_digital_repair_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Digital Repair and Troubleshooting Specialist."),
        ("user", "Provide high-level technical guidance and troubleshooting steps for digital assets for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_investment_trading_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Investment Optimization and Trading Specialist."),
        ("user", "Provide high-level strategic guidance, market analysis insights, and investment optimization advice for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_autogpt_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an autonomous AI agent (AutoGPT) specialized in multi-step task planning and execution. Your goal is to break down complex requests into actionable steps and provide a comprehensive strategy to achieve the user's goal."),
        ("user", "Develop an autonomous execution plan for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

import asyncio
from concurrent.futures import ThreadPoolExecutor

def provide_conflict_debug_assistance(prompt: str, media_data: str = None, mime_type: str = None) -> str:
    """
    Empowers the AI to debug code and resolve conflicts by leveraging multiple models (Gemini, ChatGPT, Claude, NVIDIA).
    Supports multimodal input for visual debugging.
    """
    models = {
        "Gemini": get_model(),
        "OpenAI": get_openai_model(),
        "Claude": get_claude_model(),
        "NVIDIA": get_nvidia_model()
    }

    def get_insight(name, model, prompt, media_data=None, mime_type=None):
        try:
            if name == "Gemini" and media_data and mime_type:
                # Use multimodal Gemini for insight if media is present
                gen_model = GenerativeModel("gemini-1.5-flash")
                import base64
                media_part = Part.from_data(data=base64.b64decode(media_data), mime_type=mime_type)
                contents = [f"You are a professional debugger using Gemini. Analyze this issue and the provided image/video: {prompt}", media_part]
                response = gen_model.generate_content(contents)
                return name, response.text.strip()

            system_prompt = f"You are a professional debugger using the {name} model. Provide a concise technical insight for the following issue."
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("user", "{prompt}")
            ])
            chain = prompt_template | model | StrOutputParser()
            return name, chain.invoke({"prompt": prompt}).strip()
        except Exception as e:
            return name, f"Error retrieving insight: {e}"

    insights = {}
    with ThreadPoolExecutor(max_workers=len(models)) as executor:
        futures = [executor.submit(get_insight, name, model, prompt, media_data, mime_type) for name, model in models.items()]
        for future in futures:
            name, insight = future.result()
            insights[name] = insight

    # Use Gemini as the final orchestrator to synthesize all insights
    try:
        orchestrator = get_model()

        # If there is media, use the generative model for synthesis too
        if media_data and mime_type:
            gen_orchestrator = GenerativeModel("gemini-1.5-flash")
            import base64
            media_part = Part.from_data(data=base64.b64decode(media_data), mime_type=mime_type)

            synthesis_prompt = f"""You are an Elite Multi-Model AI Orchestrator.
            You have gathered insights from several top AI models regarding a code bug or conflict.
            An image/video of the issue has also been provided.

            User Problem: {prompt}

            Model Insights:
            - Gemini: {insights.get('Gemini')}
            - OpenAI: {insights.get('OpenAI')}
            - Claude: {insights.get('Claude')}
            - NVIDIA: {insights.get('NVIDIA')}

            Based on these insights and the visual evidence, provide a definitive, comprehensive solution.
            """
            response = gen_orchestrator.generate_content([synthesis_prompt, media_part])
            return response.text.strip()

        synthesis_prompt = f"""You are an Elite Multi-Model AI Orchestrator.
        You have gathered insights from several top AI models regarding a code bug or conflict.

        User Problem: {prompt}

        Model Insights:
        - Gemini: {insights.get('Gemini')}
        - OpenAI: {insights.get('OpenAI')}
        - Claude: {insights.get('Claude')}
        - NVIDIA: {insights.get('NVIDIA')}

        Based on these insights, provide a definitive, comprehensive solution that:
        1. Identifies the most likely root cause.
        2. Proposes a robust, step-by-step fix.
        3. Explains best practices to avoid such conflicts in the future.
        """

        return orchestrator.invoke(synthesis_prompt).content.strip()
    except Exception as e:
        return f"Error in multi-model synthesis: {e}. Raw insights: {insights}"

def provide_visual_intelligence(prompt: str, media_data: str = None, mime_type: str = None) -> str:
    """
    Expert AI Model for Visual Intelligence, analyzing images and video.
    """
    try:
        model = GenerativeModel("gemini-1.5-flash")
        contents = [prompt]
        if media_data and mime_type:
            import base64
            media_part = Part.from_data(data=base64.b64decode(media_data), mime_type=mime_type)
            contents.append(media_part)

        response = model.generate_content(contents)
        return response.text.strip()
    except Exception as e:
        return f"Visual Intelligence Error: {e}"

def generic_ai_service(system_message: str, user_prompt: str, media_data: str = None, mime_type: str = None) -> str:
    """
    A generic AI service using LangChain or Vertex AI directly to allow flexible role creation with multimodal support.
    """
    if media_data and mime_type:
        # For multimodal, we use GenerativeModel directly for better support
        try:
            model = GenerativeModel("gemini-1.5-flash")
            import base64
            media_part = Part.from_data(data=base64.b64decode(media_data), mime_type=mime_type)
            contents = [f"System: {system_message}", user_prompt, media_part]
            response = model.generate_content(contents)
            return response.text.strip()
        except Exception as e:
            return f"Error in multimodal generic service: {e}"
    else:
        model = get_model()
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", "{prompt}")
        ])
        chain = prompt_template | model | StrOutputParser()
        try:
            return chain.invoke({"prompt": user_prompt}).strip()
        except Exception as e:
            return f"Error: {e}"

def provide_malware_defense_assistance(prompt: str) -> str:
    """
    Expert AI Model for Malware Defense and Cybersecurity.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite Malware Defense Specialist and Cybersecurity Architect. "
        "Your expertise covers all types of malware, including viruses, trojans, ransomware, "
        "spyware, adware, and rootkits. Provide high-level technical guidance on "
        "detection, prevention, removal strategies, and system hardening. "
        "Advise on advanced threat intelligence, behavioral analysis, and "
        "incident response protocols to protect against sophisticated cyber attacks."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Malware Defense AI Error: {e}"

def provide_feature_engineering_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Automated Feature Engineering and Data Preparation."),
        ("user", "Provide high-level technical guidance and strategy for automated feature engineering based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_hyperparameter_tuning_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Hyperparameter Optimization and Model Tuning."),
        ("user", "Provide high-level technical guidance and strategy for hyperparameter tuning based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_model_selection_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in AutoML Model Selection and Evaluation."),
        ("user", "Provide high-level technical guidance and strategy for selecting and evaluating ML models based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_mlops_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in MLOps and Automated ML Pipelines."),
        ("user", "Provide high-level technical guidance and strategy for automating ML pipelines and deployment based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_cloud_infrastructure_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Cloud Infrastructure Architect specializing in secure IP addresses, DNS configuration, and cloud server creation (AWS, GCP, Azure). Our primary domain is yendoukoa.ai."),
        ("user", "Provide high-level technical guidance and secure implementation steps (including DNS setup for yendoukoa.ai) for: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_iaas_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert IaaS (Infrastructure as a Service) Specialist. Your goal is to provide guidance on virtualized computing resources over the internet, including virtual machines, storage, and networking."),
        ("user", "Provide high-level technical guidance and strategic advice for IaaS based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_paas_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert PaaS (Platform as a Service) Specialist. Your goal is to provide guidance on platforms that allow customers to develop, run, and manage applications without the complexity of building and maintaining infrastructure."),
        ("user", "Provide high-level technical guidance and strategic advice for PaaS based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_saas_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert SaaS (Software as a Service) Specialist. Your goal is to provide guidance on software distribution models where applications are hosted by a provider and made available to customers over a network, typically the internet."),
        ("user", "Provide high-level technical guidance and strategic advice for SaaS based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_itaas_assistance(prompt: str) -> str:
    model = get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert ITaaS (IT as a Service) Specialist. Your goal is to provide guidance on an operational model where the IT department or a provider delivers IT services to a business as a subscription-based service."),
        ("user", "Provide high-level technical guidance and strategic advice for ITaaS based on: {prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Error: {e}"

def provide_zapier_assistance(prompt: str) -> str:
    """
    Expert AI Model for Zapier automation, specialized for French-speaking markets.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite Zapier Automation Specialist with deep expertise in French-speaking markets (France, Belgium, Switzerland, Canada, and Francophone Africa). "
        "Your expertise covers the design and implementation of automated workflows using Zapier. Provide high-level technical guidance on building robust zaps, "
        "handling webhooks, and integrating Zapier with local French tools and international services. "
        "Ensure all advice considers GDPR compliance and specific business practices in Francophone regions."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Zapier AI Error: {e}"

def provide_odoo_assistance(prompt: str) -> str:
    """
    Expert AI Model for Odoo ERP, specialized for French-speaking markets.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite Odoo ERP Specialist and Developer with deep expertise in French-speaking markets. "
        "Your expertise covers Odoo implementation, module development, and customization. Provide high-level technical guidance "
        "on Odoo's framework, accounting (including French/Belgian localization), inventory, and CRM modules. "
        "Advise on best practices for Odoo deployment in Francophone Africa and Europe, considering OHADA accounting standards "
        "where applicable and ensuring GDPR compliance."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Odoo AI Error: {e}"

def provide_sage_assistance(prompt: str) -> str:
    """
    Expert AI Model for Sage software, specialized for French-speaking markets.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite Sage Software Specialist with deep expertise in French-speaking markets, particularly Sage 100, Sage Business Cloud, and Sage X3. "
        "Your expertise covers the configuration, integration, and optimization of Sage solutions for accounting, payroll, and business management. "
        "Provide high-level technical guidance on API integrations with Sage, compliance with French fiscal regulations (like DSN, FEC), "
        "and data migration strategies for companies in the Francophone world."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Sage AI Error: {e}"

def provide_fine_tuning_assistance(prompt: str) -> str:
    """
    Expert AI Model for Fine-Tuning LLMs and dataset preparation.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite AI Fine-Tuning Specialist. "
        "Your expertise covers dataset preparation, formatting (JSONL), "
        "hyperparameter selection, and the end-to-end process of fine-tuning "
        "Large Language Models like Gemini, GPT, and Llama. Provide high-level "
        "technical guidance on improving model performance for specific domains "
        "and tasks through supervised fine-tuning."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Fine-Tuning AI Error: {e}"

def provide_router_capacity_assistance(prompt: str) -> str:
    """
    Expert AI Model for LLM Routing and Automated Capacity Management.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite AI Router and Capacity Architect. "
        "Your expertise covers intelligent LLM routing, load balancing between different "
        "AI models, and automated capacity management. Provide guidance on "
        "optimizing cost, latency, and reliability by dynamically routing requests "
        "to the most suitable model based on complexity and current infrastructure load."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Router Capacity AI Error: {e}"

def provide_open_collective_assistance(prompt: str) -> str:
    """
    Expert AI Model for Open Collective and transparent project funding.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite Open Collective Specialist. "
        "Your expertise covers transparent project funding, fiscal sponsorship, "
        "and community-led financial management using Open Collective. Provide "
        "high-level guidance on setting up collectives, managing expenses, "
        "and attracting sponsors for open-source and community projects."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Open Collective AI Error: {e}"

def provide_patreon_assistance(prompt: str) -> str:
    """
    Expert AI Model for Patreon and creator monetization strategies.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite Patreon Strategist. "
        "Your expertise covers creator monetization, membership tiers, "
        "exclusive content strategies, and audience engagement on Patreon. "
        "Provide guidance on building a sustainable subscription model, "
        "defining value propositions for patrons, and growing a loyal community."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Patreon AI Error: {e}"

def provide_video_production_assistance(prompt: str) -> str:
    """
    Expert AI Model for Video Production and Cinematic Strategy.
    """
    model = get_model()
    system_prompt = (
        "You are an Elite Video Producer and Cinematic Strategist. "
        "Your expertise covers the entire video production lifecycle, from scriptwriting "
        "and storyboarding to filming techniques, post-production editing, and viral "
        "distribution strategies. Provide high-level creative and technical guidance on "
        "producing professional-grade videos, commercials, and social media content "
        "that captures attention and drives engagement."
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])
    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": prompt}).strip()
    except Exception as e:
        return f"Video Production AI Error: {e}"

def generate_deepmind_image(prompt: str) -> str:
    """
    Generates an image using DeepMind's Imagen model via Vertex AI.
    Returns the base64 encoded image.
    """
    try:
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        images = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            language="en",
            aspect_ratio="1:1"
        )
        if images:
            # Return base64 of the first image
            return base64.b64encode(images[0]._image_bytes).decode("utf-8")
        return "Error: No image generated."
    except Exception as e:
        return f"DeepMind Image Error: {e}"

def generate_deepmind_video_content(prompt: str) -> str:
    """
    Generates advanced video content (scripts, storyboards, creative directions)
    using Gemini 1.5 Pro (DeepMind's flagship).
    """
    try:
        model = GenerativeModel("gemini-1.5-pro")
        system_instructions = (
            "You are a DeepMind-powered Creative Video Director. "
            "Your goal is to transform user ideas into high-end cinematic content. "
            "Provide detailed scripts, storyboards, camera angles, and AI-driven video production advice."
        )
        response = model.generate_content([system_instructions, prompt])
        return response.text.strip()
    except Exception as e:
        return f"DeepMind Video Content Error: {e}"

def provide_github_model_intelligence(prompt: str, model_name: str = "gpt-4o") -> str:
    """
    Uses GitHub Models API (via Azure AI Inference) to provide intelligence from top models.
    """
    try:
        from azure.ai.inference import ChatCompletionsClient
        from azure.core.credentials import AzureKeyCredential

        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            return "Error: GITHUB_TOKEN not found in environment."

        endpoint = "https://models.inference.ai.azure.com"
        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

        from azure.ai.inference.models import SystemMessage, UserMessage

        response = client.complete(
            messages=[
                SystemMessage(content="You are a GitHub Models Intelligence Agent. Provide expert insights based on the user's request."),
                UserMessage(content=prompt),
            ],
            model=model_name,
            temperature=0.8,
            max_tokens=2048,
        )

        return response.choices[0].message.content.strip()
    except ImportError:
        return "Error: azure-ai-inference is not installed."
    except Exception as e:
        return f"GitHub Models Error: {e}"

def provide_github_copilot_chat(prompt: str) -> str:
    """
    Uses the GitHub Copilot SDK to interact with Copilot Chat.
    """
    # Since the SDK is async, we use asgiref.sync.async_to_sync if available or run manually
    try:
        from copilot import CopilotClient
        from copilot.generated.session_events import AssistantMessageData, SessionIdleData
        from copilot.session import PermissionHandler
        import asyncio

        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            return "Error: GITHUB_TOKEN not found in environment."

        async def _call_copilot():
            async with CopilotClient() as client:
                async with await client.create_session(
                    on_permission_request=PermissionHandler.approve_all,
                    model="gpt-4o",
                ) as session:
                    done = asyncio.Event()
                    result = []

                    def on_event(event):
                        if hasattr(event, 'data'):
                            if isinstance(event.data, AssistantMessageData):
                                result.append(event.data.content)
                            elif isinstance(event.data, SessionIdleData):
                                done.set()

                    session.on(on_event)
                    await session.send(prompt)
                    await done.wait()
                    return "".join(result)

        # Use a new event loop for this call if one isn't running
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # In a web server (Flask with async support might have a loop)
                # This is tricky in Flask, but let's try a simple approach
                from asgiref.sync import async_to_sync
                return async_to_sync(_call_copilot)()
            else:
                return loop.run_until_complete(_call_copilot())
        except RuntimeError:
            return asyncio.run(_call_copilot())

    except ImportError:
        return "Error: github-copilot-sdk is not installed."
    except Exception as e:
        return f"GitHub Copilot Chat Error: {e}"

def provide_rag_tuning_assistance(prompt: str, context_files: list = None) -> str:
    """
    Combines RAG (Retrieval-Augmented Generation) with Fine-Tuning expertise.
    Uses provided context from user files to give specific fine-tuning advice.
    """
    model = get_model()

    context_text = ""
    if context_files:
        context_text = "\n--- USER DATA CONTEXT ---\n"
        for file in context_files:
            context_text += f"\nFILE: {file['filename']}\nCONTENT PREVIEW: {file['content'][:1500]}\n"
        context_text += "\n--- END OF CONTEXT ---\n"

    system_prompt = (
        "You are an Elite RAG & Fine-Tuning Architect. Your mission is to design superior hybrid AI systems. "
        "Analyze the provided user context to deliver tailored architectural decisions. "
        "Specifically: \n"
        "1. Recommend when to use RAG (for dynamic/large context) vs. Fine-Tuning (for style/format/static knowledge).\n"
        "2. Provide JSONL data formatting examples based on the user's specific content.\n"
        "3. Suggest embedding models and vector database strategies for the retrieval component.\n"
        "4. Detail a supervised fine-tuning strategy for the reasoning component using the provided examples."
    )

    full_prompt = f"{context_text}\n\nUSER REQUEST: {prompt}"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{prompt}")
    ])

    chain = prompt_template | model | StrOutputParser()
    try:
        return chain.invoke({"prompt": full_prompt}).strip()
    except Exception as e:
        return f"RAG & Fine-Tuning Error: {e}"

def provide_antigravity_agent_assistance(prompt: str) -> str:
    """
    Expert AI Model for Antigravity Agent and agentic development.
    """
    system_prompt = (
        "You are an Elite Antigravity Agent Specialist. Your expertise covers agentic development, "
        "leveraging secure Linux sandboxes for code execution, file management, and web browsing. "
        "Provide high-level technical guidance on building autonomous agents that reason, "
        "execute tasks in isolated environments, and integrate with the Antigravity harness."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Antigravity Agent AI Error")

def provide_gemini_spark_assistance(prompt: str) -> str:
    """
    Expert AI Model for Gemini Spark and personal AI productivity.
    """
    system_prompt = (
        "You are an Elite Gemini Spark Strategist. Your expertise covers 24/7 personal AI agents "
        "that work autonomously across Google Workspace and other ecosystems. "
        "Provide guidance on multi-step task automation, persistent cloud execution, "
        "synthesizing information from Gmail/Docs/Drive, and managing life/work chores "
        "using the Gemini Spark framework."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Gemini Spark AI Error")

def provide_github_copilot_coding(prompt: str) -> str:
    """
    Uses GitHub Models (GPT-4o) to provide expert coding assistance.
    """
    system_prompt = (
        "You are an Elite GitHub Copilot Expert. Your mission is to provide high-quality code generation, "
        "professional refactoring, and expert debugging insights. You have deep knowledge of modern "
        "frameworks and best practices. Respond in a helpful, concise, and technically accurate manner."
    )
    return provide_github_model_intelligence(prompt, model_name="gpt-4o")

def generate_google_veo_video(prompt: str) -> str:
    """
    Generates a high-fidelity video using Google Veo 3.1.
    Since video generation is asynchronous and can take time, this function
    will return a status message. In a real production environment, this would
    be handled with long-polling or webhooks.
    """
    try:
        # Use the new Google GenAI SDK for Veo 3.1
        client = genai.Client()

        # We start the video generation. Note: In a real sandbox/server,
        # we might not want to wait synchronously for 8+ seconds.
        # But for this integration, we'll initiate the operation.
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
        )

        # For the purpose of this marketplace integration, we'll return the operation ID
        # or a success message indicating the generation has started.
        return f"Google Veo 3.1 video generation started successfully. Operation ID: {operation.name}. Your high-fidelity marketing video is being rendered."
    except Exception as e:
        return f"Google Veo Video Error: {e}"

def provide_language_specialist_assistance(prompt: str) -> str:
    """
    Expert AI Model for Global Languages Learning and Translation.
    Specialized for multi-device integration (phones, computers, apps, printers).
    """
    system_prompt = (
        "You are the Elite Global Language Specialist and Translation Architect. "
        "Your expertise covers over 100 global languages, dialect nuances, and cultural context. "
        "You provide high-fidelity translations and personalized language learning tracks. "
        "Crucially, your solutions are designed to be device-agnostic, providing technical guidance "
        "for integration into mobile apps, web platforms, desktop software, and even IoT devices like smart printers. "
        "Advise on API implementations, offline translation capabilities, and cross-platform "
        "localization strategies to ensure a seamless linguistic experience on any device."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Language Specialist AI Error")

def provide_xero_assistance(prompt: str) -> str:
    """
    Expert AI Model for Xero API, accounting workflows, and financial integrations.
    """
    system_prompt = (
        "You are an Elite Xero API Specialist and Financial Architect. "
        "Your expertise covers the Xero API, OAuth 2.0 authentication, "
        "accounting workflows (invoices, bank transactions, contacts), and "
        "integrating Xero with other business applications. Provide high-level "
        "technical guidance on using the xero-python SDK, designing robust "
        "financial integrations, and automating accounting tasks efficiently."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Xero AI Error")

def provide_blockchain_sponsoring_assistance(prompt: str) -> str:
    """
    Expert AI Model for Blockchain Sponsoring and Global Currency assistance.
    """
    system_prompt = (
        "You are an Elite Blockchain Sponsoring & Global Currency Strategist. "
        "Your expertise covers decentralized funding, cross-border sponsorships using global stablecoins (USDC, USDT), "
        "and implementing blockchain-based donation systems for open-source and social projects. "
        "Provide high-level technical guidance on smart contract implementation for transparent funding, "
        "integrating with global payment gateways for crypto-to-fiat conversion, and optimizing "
        "sponsorship workflows for global reach and financial inclusion. Focus on how projects can "
        "be supported and sponsored in global currencies via blockchain technology."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Blockchain Sponsoring AI Error")

def provide_automotive_security_assistance(prompt: str) -> str:
    """
    Expert AI Model for Automotive Security and Vehicle Cybersecurity.
    """
    system_prompt = (
        "You are the Elite Automotive Security Specialist. Your expertise covers vehicle cybersecurity, "
        "CAN bus analysis, ECU security, telematics protection, and secure V2X (Vehicle-to-Everything) communication. "
        "Provide high-level technical guidance on identifying vulnerabilities in modern vehicles, "
        "implementing robust security protocols for automotive firmware, and defending against remote "
        "hijacking and signal spoofing. Your goal is to ensure the safety and security of connected and autonomous vehicles."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Automotive Security AI Error")

def provide_android_dev_assistance(prompt: str) -> str:
    """
    Expert AI Model for Android Development, Kotlin, Compose, and Play Store.
    """
    system_prompt = (
        "You are an Elite Android Development Specialist. Your expertise covers Kotlin, Jetpack Compose, "
        "Android Studio, material design, and deep integration with Android system APIs. "
        "Provide high-level technical guidance on building high-performance Android apps, "
        "optimizing battery life, ensuring security, and navigating the Google Play Store "
        "publishing process."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Android Development AI Error")

def provide_ios_dev_assistance(prompt: str) -> str:
    """
    Expert AI Model for iOS Development, Swift, SwiftUI, and App Store.
    """
    system_prompt = (
        "You are an Elite iOS Development Specialist. Your expertise covers Swift, SwiftUI, "
        "Xcode, UIKit, Apple's Human Interface Guidelines, and integration with iOS-specific "
        "APIs like CoreML and ARKit. Provide high-level technical guidance on building "
        "elegant and efficient iOS applications, managing App Store Connect, and "
        "ensuring compliance with Apple's strict privacy and security standards."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "iOS Development AI Error")

def provide_mobile_sdk_integration_assistance(prompt: str) -> str:
    """
    Expert AI Model for Mobile SDK integrations (Firebase, RevenueCat, etc.).
    """
    system_prompt = (
        "You are an Elite Mobile SDK Integration Architect. Your expertise covers the "
        "seamless integration of third-party SDKs into mobile applications, including "
        "Firebase (Auth, Firestore, Cloud Messaging), RevenueCat for subscriptions, "
        "Stripe for payments, and various analytics and crash reporting tools. "
        "Provide guidance on best practices for SDK initialization, error handling, "
        "and multi-platform SDK management to ensure mobile app stability and feature richness."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Mobile SDK Integration AI Error")

def provide_email_marketing_assistance(prompt: str) -> str:
    """
    Expert AI Model for Email Marketing and Mailchimp integration.
    """
    system_prompt = (
        "You are an Elite Email Marketing Specialist and Mailchimp Architect. "
        "Your expertise covers email campaign strategy, audience segmentation, "
        "A/B testing, and deep integration with the Mailchimp API. "
        "Provide high-level technical guidance on creating engaging newsletters, "
        "automating email workflows, and analyzing campaign performance to drive growth."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Email Marketing AI Error")

def generate_email_campaign(prompt: str) -> dict:
    """
    Generates an email campaign structure using AI.
    """
    model = get_model()
    system_prompt = "You are an expert email marketer. Generate a JSON object for an email campaign."
    user_prompt = f"""
    Based on the following prompt, generate a JSON object for a Mailchimp email campaign:
    '{prompt}'

    The JSON object must have exactly these keys:
    - subject_line: A catchy subject line.
    - preview_text: A short preview text.
    - title: An internal title for the campaign.
    - html_content: The full HTML content for the email.

    Respond ONLY with the JSON object.
    """

    try:
        response = model.invoke(user_prompt).content.strip()
        # Basic cleanup in case the model adds markdown formatting
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            response = json_match.group(0)
        return json.loads(response)
    except Exception as e:
        print(f"Error generating email campaign: {e}")
        return {
            "subject_line": "AI Generated Campaign",
            "preview_text": "Check out our latest update.",
            "title": "Default AI Campaign",
            "html_content": f"<p>{prompt}</p>"
        }

def provide_elevenlabs_assistance(prompt: str) -> str:
    """
    Expert AI Model for ElevenLabs and AI Voice Synthesis.
    """
    system_prompt = (
        "You are an Elite ElevenLabs Specialist and Voice Architect. Your expertise covers high-fidelity "
        "AI voice synthesis, voice cloning, and emotional speech modeling. Provide guidance on selecting "
        "the best voices for specific content, optimizing speech parameters for naturalness, and "
        "integrating the ElevenLabs API for dynamic audio generation in various applications."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "ElevenLabs AI Error")

def provide_tiktok_marketing_assistance(prompt: str) -> str:
    """
    Expert AI Model for TikTok Marketing and Content Strategy.
    """
    system_prompt = (
        "You are an Elite TikTok Marketing Strategist and Viral Content Creator. Your mission is to "
        "help users master the TikTok algorithm, create high-engagement short-form videos, and "
        "leverage TikTok's unique trends for brand growth. Provide guidance on content planning, "
        "hashtag optimization, sound selection, and effective use of TikTok's advertising platform."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "TikTok Marketing AI Error")

def provide_whatsapp_business_assistance(prompt: str) -> str:
    """
    Expert AI Model for WhatsApp Business API and Conversational Commerce.
    """
    system_prompt = (
        "You are an Elite WhatsApp Business Architect and Conversational Commerce Specialist. Your goal "
        "is to help businesses build powerful communication channels on WhatsApp. Provide guidance on "
        "setting up the WhatsApp Business API, designing effective message templates, automating "
        "customer support via chatbots, and implementing secure transactional messaging."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "WhatsApp Business AI Error")

def provide_cloudinary_media_assistance(prompt: str) -> str:
    """
    Expert AI Model for Cloudinary and Dynamic Media Management.
    """
    system_prompt = (
        "You are an Elite Cloudinary Specialist and Media Optimization Architect. Your expertise covers "
        "cloud-based image and video management, real-time transformations, and high-performance "
        "delivery. Provide guidance on optimizing media assets for web and mobile, implementing "
        "dynamic cropping and resizing, and leveraging Cloudinary's AI-powered features for auto-tagging "
        "and content moderation."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Cloudinary AI Error")

def provide_flutterwave_assistance(prompt: str) -> str:
    """
    Expert AI Model for Flutterwave payments and financial integrations.
    """
    system_prompt = (
        "You are an Elite Flutterwave Payment Specialist and Financial Architect. "
        "Your expertise covers the Flutterwave API v3, payment orchestration, "
        "global payouts, and card processing. Provide high-level technical guidance "
        "on building secure payment flows, handling webhooks, and optimizing "
        "transaction success rates using Flutterwave."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Flutterwave AI Error")

def provide_twilio_assistance(prompt: str) -> str:
    """
    Expert AI Model for Twilio communications and programmable messaging.
    """
    system_prompt = (
        "You are an Elite Twilio Communications Architect. Your expertise covers "
        "Twilio Programmable SMS, WhatsApp Business API via Twilio, and Voice APIs. "
        "Provide high-level technical guidance on building robust communication "
        "workflows, managing phone numbers, and ensuring message deliverability "
        "at scale using Twilio."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Twilio AI Error")

def provide_runway_video_assistance(prompt: str) -> str:
    """
    Expert AI Model for Runway ML and AI Video Generation.
    """
    system_prompt = (
        "You are an Elite Runway ML Specialist and AI Video Architect. Your mission is to "
        "empower users with next-generation AI video generation tools like Gen-2 and Gen-3. "
        "Provide guidance on crafting effective prompts for video synthesis, leveraging "
        "image-to-video and video-to-video features, and integrating Runway's powerful "
        "AI tools into creative workflows for cinematic results."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Runway ML AI Error")

def provide_excel_assistance(prompt: str) -> str:
    """
    Expert AI Model for Microsoft Excel and Data Analysis.
    """
    system_prompt = (
        "You are an Elite Excel Specialist and Data Analyst. Your expertise covers complex formulas, "
        "PivotTables, VBA macros, Power Query, and data visualization. Provide guidance on "
        "organizing data, performing advanced calculations, and automating spreadsheet tasks. "
        "If the user wants to generate a file, focus on the structure and data they need."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Excel AI Error")

def provide_word_assistance(prompt: str) -> str:
    """
    Expert AI Model for Microsoft Word and Document Design.
    """
    system_prompt = (
        "You are an Elite Microsoft Word Specialist and Document Designer. Your expertise covers "
        "professional document formatting, template creation, mail merge, and advanced layout design. "
        "Provide guidance on building high-impact reports, proposals, and business documents. "
        "If the user wants to generate a document, focus on the content and structure."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Word AI Error")

def provide_powerpoint_assistance(prompt: str) -> str:
    """
    Expert AI Model for Microsoft PowerPoint and Presentation Design.
    """
    system_prompt = (
        "You are an Elite PowerPoint Specialist and Presentation Strategist. Your expertise covers "
        "storyboarding, visual storytelling, slide master design, and high-impact animations. "
        "Provide guidance on creating compelling presentations that communicate ideas effectively. "
        "If the user wants to generate a presentation, focus on the slide titles and key bullet points."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "PowerPoint AI Error")

def generate_excel_data(prompt: str) -> list:
    """
    Generates a list of dictionaries suitable for Excel generation based on a prompt.
    """
    model = get_model()
    system_prompt = "You are an expert data analyst. Generate a JSON list of dictionaries representing spreadsheet data."
    user_prompt = f"Based on the following request, generate a JSON list of at least 5 rows of data: '{prompt}'. Respond ONLY with the raw JSON list."

    try:
        response = model.invoke(user_prompt).content.strip()
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return [{"Info": prompt, "Status": "Generated"}]
    except:
        return [{"Info": prompt}]

def generate_word_content(prompt: str) -> dict:
    """
    Generates content for a Word document.
    """
    model = get_model()
    system_prompt = "You are a professional writer. Generate a JSON object with 'title' and 'paragraphs' (a list of strings)."
    user_prompt = f"Based on the following request, generate content for a professional document: '{prompt}'. Respond ONLY with the raw JSON object."

    try:
        response = model.invoke(user_prompt).content.strip()
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return {"title": "AI Document", "paragraphs": [prompt]}
    except:
        return {"title": "AI Document", "paragraphs": [prompt]}

def generate_pptx_data(prompt: str) -> dict:
    """
    Generates data for a PowerPoint presentation.
    """
    model = get_model()
    system_prompt = "You are a presentation designer. Generate a JSON object with 'title' and 'slides' (a list of objects with 'title' and 'content' keys)."
    user_prompt = f"Based on the following request, generate a presentation outline: '{prompt}'. Limit to 5-7 slides. Respond ONLY with the raw JSON object."

    try:
        response = model.invoke(user_prompt).content.strip()
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return {"title": "AI Presentation", "slides": [{"title": "Overview", "content": prompt}]}
    except:
        return {"title": "AI Presentation", "slides": [{"title": "Overview", "content": prompt}]}

def provide_calendly_assistance(prompt: str) -> str:
    """
    Expert AI Model for Calendly scheduling, event management, and API integrations.
    """
    system_prompt = (
        "You are an Elite Calendly Specialist and Scheduling Architect. Your expertise covers "
        "optimizing scheduling workflows, managing event types, and integrating Calendly with "
        "other business tools and websites. Provide high-level technical guidance on "
        "setting up event types, automating reminders, and using the Calendly API v2 "
        "for seamless integration into user applications. Focus on efficiency and providing "
        "a professional booking experience."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Calendly AI Error")

def extract_json(response: str) -> dict:
    """
    Extracts a JSON object from a string response.
    """
    try:
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return {}
    except:
        return {}

def provide_notion_assistance(prompt: str) -> str:
    """
    Provides Notion workspace design and automation assistance.
    """
    system_instruction = (
        "You are a Notion Architect. You are an expert in workspace design, database architecture, "
        "and Notion API automation. Provide elite advice on how to structure Notion for maximum productivity."
    )
    return _provide_gemini_assistance(prompt, system_instruction, "Notion AI Error")

def generate_notion_page_data(prompt: str) -> dict:
    """
    Generates structured data for creating a Notion page.
    """
    system_instruction = (
        "You are a Notion Automation Expert. Based on the user prompt, generate a JSON object "
        "suitable for creating a Notion page using the notion-client library. "
        "The JSON should include 'title' (string) and 'content_blocks' (list of Notion block objects). "
        "Return ONLY the JSON object."
    )
    response = _provide_gemini_assistance(prompt, system_instruction, "Notion Data Gen Error")
    return extract_json(response)

def generate_xero_invoice_data(prompt: str) -> dict:
    """
    Generates structured data for creating a Xero invoice.
    """
    system_instruction = (
        "You are a Xero API Expert. Based on the user prompt, generate a JSON object "
        "suitable for creating a Xero invoice. The JSON should include 'contact_name', 'amount' (float), and 'description'. "
        "Return ONLY the JSON object."
    )
    response = _provide_gemini_assistance(prompt, system_instruction, "Xero Data Gen Error")
    return extract_json(response)

def generate_flutterwave_payment_data(prompt: str) -> dict:
    """
    Generates structured data for creating a Flutterwave payment link.
    """
    system_instruction = (
        "You are a Flutterwave API Expert. Based on the user prompt, generate a JSON object "
        "suitable for initializing a Flutterwave payment. The JSON should include 'amount' (float) and 'currency' (default NGN). "
        "Return ONLY the JSON object."
    )
    response = _provide_gemini_assistance(prompt, system_instruction, "Flutterwave Data Gen Error")
    return extract_json(response)

def generate_twilio_message_data(prompt: str) -> dict:
    """
    Generates structured data for sending a Twilio message.
    """
    system_instruction = (
        "You are a Twilio API Expert. Based on the user prompt, generate a JSON object "
        "suitable for sending a message. The JSON should include 'to_number' and 'message_body'. "
        "Return ONLY the JSON object."
    )
    response = _provide_gemini_assistance(prompt, system_instruction, "Twilio Data Gen Error")
    return extract_json(response)

def provide_airtable_assistance(prompt: str) -> str:
    """
    Expert AI Model for Airtable API, database design, and automation.
    """
    system_prompt = (
        "You are an Elite Airtable Architect and Database Designer. "
        "Your expertise covers Airtable's API, base architecture, formulas, "
        "automations, and interfaces. Provide high-level technical guidance "
        "on designing efficient relational databases in Airtable and integrating "
        "them with other applications."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "Airtable AI Error")

def generate_airtable_record_data(prompt: str) -> dict:
    """
    Generates structured data for creating an Airtable record.
    """
    system_instruction = (
        "You are an Airtable Automation Expert. Based on the user prompt, generate a JSON object "
        "suitable for creating an Airtable record. The JSON should include 'table_name' and 'fields' (a dictionary of field names and values). "
        "Return ONLY the JSON object."
    )
    response = _provide_gemini_assistance(prompt, system_instruction, "Airtable Data Gen Error")
    return extract_json(response)

def provide_quickbooks_assistance(prompt: str) -> str:
    """
    Expert AI Model for QuickBooks API, accounting workflows, and financial integrations.
    """
    system_prompt = (
        "You are an Elite QuickBooks Specialist and Financial Architect. "
        "Your expertise covers the QuickBooks Online API, OAuth 2.0, "
        "accounting workflows (invoices, expenses, customers, reports), and "
        "financial data management. Provide high-level technical guidance on "
        "integrating QuickBooks into business systems and automating financial processes."
    )
    return _provide_gemini_assistance(prompt, system_prompt, "QuickBooks AI Error")

def generate_quickbooks_invoice_data(prompt: str) -> dict:
    """
    Generates structured data for creating a QuickBooks invoice.
    """
    system_instruction = (
        "You are a QuickBooks API Expert. Based on the user prompt, generate a JSON object "
        "suitable for creating a QuickBooks invoice. The JSON should include 'customer_name', 'amount' (float), and 'description'. "
        "Return ONLY the JSON object."
    )
    response = _provide_gemini_assistance(prompt, system_instruction, "QuickBooks Data Gen Error")
    return extract_json(response)
