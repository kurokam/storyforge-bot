import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_story(category: str, topic: str = ""):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    topic_part = f"Topic: {topic}" if topic else "Topic: Any"

    prompt = f"""
Write a realistic and viral short horror/mystery story.
Category: {category}
{topic_part}

Rules:
- Suitable for YouTube Shorts
- 60-90 seconds story
- Twist ending

Then generate ONLY CapCut scene prompts in this exact format:
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