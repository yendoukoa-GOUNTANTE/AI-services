from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-services-agent",
    version="2.0.0",
    author="Jules",
    author_email="jules@example.com",
    description="A web-based AI agent that can perform several roles to assist with software development and business tasks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GYFX35/AI-services",
    packages=find_packages(),
    py_modules=["app", "google_ai"],
    include_package_data=True,
    install_requires=[
        "Flask[async]",
        "Flask-Babel",
        "Flask-SQLAlchemy",
        "python-dotenv",
        "requests",
        "beautifulsoup4",
        "lxml",
        "httpx",
        "anyio",
        "sniffio",
        "stripe",
        "facebook-business",
        "google-cloud-aiplatform",
        "google-auth",
        "langchain",
        "langchain-google-vertexai",
        "langchain-openai",
        "langchain-anthropic",
        "langchain-nvidia-ai-endpoints",
        "langflow",
        "llama-index",
        "llama-index-llms-nvidia",
        "flask-cors>=5.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
