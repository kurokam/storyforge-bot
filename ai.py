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
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You create viral 15-second YouTube Shorts scripts in Turkish. Return: HOOK, SCENE, TWIST, CAPCUT_PROMPT, TAGS."},
            {"role": "user", "content": f"Create a viral {kind} short story for faceless anime-style video."}
        ],
        "temperature": 0.9,
        "max_tokens": 300
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(GROQ_URL, headers=headers, json=payload)
        # Debug için status ve body’yi döndür
        if r.status_code != 200:
            return f"❌ Groq status={r.status_code}\n{r.text}"
        data = r.json()
        return data["choices"][0]["message"]["content"]
