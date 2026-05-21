import os
import re
import vertexai
from vertexai.generative_models import GenerativeModel, Part
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
        ("system", "You are an expert Digital Marketing and Bot Management Specialist."),
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
