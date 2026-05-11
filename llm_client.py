from datetime import datetime
import os
import json
import time

from dotenv import load_dotenv
from litellm import completion

load_dotenv()

ROLE_CONFIG = {
    "fast": {
        "model_name": os.getenv("MODEL_FAST", "gemini/gemini-3.0-flash-preview"),
        "api_key": os.getenv("GEMINI_API_KEY"),
        "api_base": None,
        "fallback_model_name": os.getenv("MODEL_STABLE", "openai/gpt-4o-mini"),
        "fallback_api_key": os.getenv("GITHUB_PAT_TOKEN"),
        "fallback_api_base": "https://models.inference.ai.azure.com"
    },
    "smart": {
        "model_name": os.getenv("MODEL_SMART", "gemini/gemini-2.5-flash"),
        "api_key": os.getenv("GEMINI_API_KEY"),
        "api_base": None,
        "fallback_model_name": os.getenv("MODEL_STABLE", "openai/gpt-4o-mini"),
        "fallback_api_key": os.getenv("GITHUB_PAT_TOKEN"),
        "fallback_api_base": "https://models.inference.ai.azure.com"
    },
    "stable": {
        "model_name": os.getenv("MODEL_STABLE", "openai/gpt-4o-mini"),
        "api_key": os.getenv("GITHUB_PAT_TOKEN"),
        "api_base": "https://models.inference.ai.azure.com",
        "fallback_model_name": os.getenv("MODEL_GENEROUS", "groq/llama-3.3-70b-versatile"),
        "fallback_api_key": os.getenv("GROQ_API_KEY")
    },
    "generous": {
        "model_name": os.getenv("MODEL_GENEROUS", "groq/llama-3.3-70b-versatile"),
        "api_key": os.getenv("GROQ_API_KEY"),
        "api_base": None,
        "fallback_model_name": os.getenv("MODEL_LOCAL", "groq/llama-3.1-8b-instant"),
        "fallback_api_key": os.getenv("GROQ_API_KEY"),
    },
    "local": {
        "model_name": os.getenv("MODEL_LOCAL", "groq/llama-3.1-8b-instant"),
        "api_key": os.getenv("GROQ_API_KEY"),
        "api_base": None,
        "fallback_model_name": None,
        "fallback_api_key": None
    }
}
