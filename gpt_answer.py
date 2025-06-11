# gpt_answer.py (local AI using Ollama)
import requests

def get_answer_from_gpt(prompt_text):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt_text,
                "stream": False
            }
        )
        result = response.json()
        return result['response'].strip()
    except Exception as e:
        return f"❌ Local Model Error: {e}"
