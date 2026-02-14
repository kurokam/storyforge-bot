import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_story(category: str):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Gercekci ve viral olabilecek kisa korku/gizem hikayesi yaz.
Kategori: {category}

Kurallar:
- YouTube Shorts icin uygun
- 60-90 saniyelik hikaye metni
- Sonda ters kose bitis

Sonra SADECE asagidaki formatta CapCut icin sahneler uret:
Sahne 1 - (gorsel prompt)
Sahne 2 - (gorsel prompt)
...
Toplam 10 sahne olacak.
Baska hicbir aciklama yazma.
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a creative horror storyteller."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]