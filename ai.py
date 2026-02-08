import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_story(kind: str):
    if not GROQ_API_KEY:
        return "❌ GROQ_API_KEY bulunamadı."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are StoryForge AI. Create a viral 15-second YouTube Shorts script in Turkish. "
                    "Return structured output with: HOOK, SCENE, TWIST, CAPCUT_PROMPT, TAGS."
                ),
            },
            {
                "role": "user",
                "content": f"Theme: {kind}. Create a faceless anime-style short story."
            }
        ],
        "temperature": 0.8,
        "max_tokens": 250
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(URL, headers=headers, json=payload)
            if r.status_code != 200:
                return f"❌ Groq {r.status_code}: {r.text}"

            data = r.json()

            # Güvenli parse (Groq/OpenAI uyumlu format)
            choices = data.get("choices")
            if not choices:
                return f"❌ Beklenmeyen cevap formatı:\n{data}"

            message = choices[0].get("message", {})
            content = message.get("content")

            if not content:
                return f"❌ İçerik bulunamadı. Ham cevap:\n{data}"

            return content

    except Exception as e:
        return f"❌ HTTP hata: {e}"    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(URL, headers=headers, json=payload)
            if r.status_code != 200:
                return f"❌ Groq {r.status_code}: {r.text}"
            data = r.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ HTTP hata: {e}"
