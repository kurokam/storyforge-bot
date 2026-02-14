import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_story(category: str, duration: str):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Create a viral YouTube Shorts story.

Category: {category}
Duration: {duration}

Return in this exact format:

TITLE:
<viral short title>

DESCRIPTION:
<short engaging description>

TAGS:
<tag1, tag2, tag3, ...>

STORY:
<story text>

CAPCUT SCENES:
Scene 1 - (visual prompt)
Scene 2 - (visual prompt)
...

Scenes count based on duration:
30s = 5 scenes
60s = 10 scenes
90s = 15 scenes

Each scene must include:
- 9:16 vertical
- cinematic lighting
- photorealistic
- camera movement

No extra commentary.
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a professional viral YouTube scriptwriter."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]