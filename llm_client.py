from datetime import datetime
import os
import json
import time

from dotenv import load_dotenv
import litellm

load_dotenv()

ROLE_CONFIG: dict = {
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

def _log(status: str, user_prompt: str, input_tokens: int, model_response: str, output_tokens: int, role: str, model_name: str, latency_time: float, fallback_model_name=None) -> None:
    
    timestamp = datetime.now()

    log_entry: dict = {
        "status": status,
        "input": user_prompt,
        "input_tokens_count": input_tokens,
        "output": model_response,
        "output_tokens_count": output_tokens,
        "role": role, 
        "model_name": model_name,
        "fallback_model": fallback_model_name,
        "timestamp": timestamp.time().strftime("%H:%M:%S"),
        "date": timestamp.date().strftime("%D"),
        "latency": latency_time
    }

    json_string: str = json.dumps(log_entry)

    os.makedirs("logs", exist_ok=True)

    with open("logs/logs.jsonl", "a") as af:
        af.write(json_string)
        af.write("\n")

def chat(messages: list[dict], role: str):
    config = ROLE_CONFIG.get(role)
    call_kwargs = {
        "model": config["model_name"], 
        "messages": messages,
        "api_key": config["api_key"],
    }

    if config["api_base"] is not None:
        call_kwargs["api_base"] = config["api_base"]
    
    print(call_kwargs)

    t0 = time.time()

    try:
        # response = litellm.completion(**call_kwargs)
        t1 = time.time()
        latency = round(t1-t0, 3)
        print(latency)

    except:
        if config["fallback_model_name"] is None:
            latency = round(t1-t0, 3)
            print(latency)
            # _log()
            raise

        call_kwargs["model"] = config.get("fallback_model_name")
        call_kwargs["api_key"] = config.get("fallback_api_key")

        if config["fallback_api_base"] is not None:
            call_kwargs["api_base"] = config.get("fallback_api_base")

        # response = litellm.completion(**call_kwargs)
        t2 = time.time()

        latency = round(t2-t0, 3)
        # _log()
        print(latency)

    # print(response.choices[0].messages.content)

chat([{"hi": "hello"}], "fast")