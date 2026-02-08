import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_story(kind: str):
    system = (
        "You are StoryForge AI. You create viral 15-second YouTube Shorts scripts. "
        "Return structured output with: HOOK, SCENE, TWIST, CAPCUT_PROMPT, TAGS. "
        "Language: Turkish. Style: anime horror / mystery / scam awareness depending on kind."
    )

    user = f"Create a viral {kind} short story for faceless anime-style video."

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0.9,
    )

    return resp.choices[0].message.content
