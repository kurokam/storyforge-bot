import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_story(kind: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {"role": "system", "content": (
                "You are StoryForge AI. Create a viral 15-second YouTube Shorts script. "
                "Return structured output with: HOOK, SCENE, TWIST, CAPCUT_PROMPT, TAGS. "
                "Language: Turkish. Style based on kind."
            )},
            {"role": "user", "content": f"Create a viral {kind} short story for faceless anime-style video."}
        ],
        "temperature": 0.9,
        "max_tokens": 350
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(GROQ_URL, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ AI hata verdi:\n{e}"
