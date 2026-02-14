import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_story(kind: str):
    if not GROQ_API_KEY:
        return "❌ GROQ_API_KEY bulunamadı. Railway > Variables kısmına ekle."

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
                "You are StoryForge AI. Create a viral YouTube Shorts horror story in Turkish. "
                "Return ONLY in this exact format:\n\n"
                "BASLIK: <YouTube Shorts icin merak uyandiran baslik>\n\n"
                "ACIKLAMA: <2-3 cumlelik aciklama + izleyiciyi yoruma cagir>\n\n"
                "SAHNELER:\n"
                "1. (0-3sn): <CapCut icin goruntu promptu>\n"
                "2. (3-6sn): <CapCut icin goruntu promptu>\n"
                "3. (6-9sn): <CapCut icin goruntu promptu>\n"
                "4. (9-12sn): <CapCut icin goruntu promptu>\n"
                "5. (12-15sn): <CapCut icin goruntu promptu>\n\n"
                "ETIKETLER: <virgulle ayrilmis, en populer YouTube Shorts etiketleri>"
            ),
        },
        {
            "role": "user",
            "content": f"Konu: {kind}. Gercekci ve karanlik bir korku hikayesi yaz."
        }
    ],
    "temperature": 0.9,
    "max_tokens": 350
}

    try:
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.post(URL, headers=headers, json=payload)

            if response.status_code != 200:
                return f"❌ Groq API {response.status_code}: {response.text}"

            data = response.json()

            choices = data.get("choices")
            if not choices or not isinstance(choices, list):
                return f"❌ Beklenmeyen cevap formatı:\n{data}"

            message = choices[0].get("message", {})
            content = message.get("content")

            if not content:
                return f"❌ İçerik boş döndü. Ham cevap:\n{data}"

            return content

    except httpx.TimeoutException:
        return "⏱️ AI geç cevap verdi. Tekrar dene."

    except Exception as e:
        return f"❌ HTTP hata: {e}"