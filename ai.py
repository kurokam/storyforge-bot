import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_story(category: str, lang: str):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    if lang == "en":
        prompt = f"""
Write a realistic and viral short horror/mystery story.
Category: {category}

Rules:
- Suitable for YouTube Shorts
- 60-90 seconds story
- Twist ending

Then generate ONLY CapCut scene prompts in this format:
Scene 1 - (visual prompt)
Scene 2 - (visual prompt)
...
Total 10 scenes.

Each scene must be:
- 9:16 vertical
- cinematic lighting
- photorealistic
- camera movement (slow zoom / handheld / motion blur)
No extra explanation.
"""
    else:
        prompt = f"""
Gercekci ve viral olabilecek kisa korku/gizem hikayesi yaz.
Kategori: {category}

Kurallar:
- YouTube Shorts icin uygun
- 60-90 saniyelik hikaye
- Sonda ters kose

Sonra SADECE su formatta CapCut sahneleri uret:
Sahne 1 - (gorsel prompt)
Sahne 2 - (gorsel prompt)
...
Toplam 10 sahne olacak.

Her sahne:
- 9:16 dikey
- sinematik isiklandirma
- fotogercekci
- kamera hareketi (slow zoom / handheld / motion blur)
Baska aciklama yazma.
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a creative viral short video storyteller."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]