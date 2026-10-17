import base64
import json
import re

import httpx

from app.config import GEMINI_API_BASE, GEMMA_MODEL, GOOGLE_AI_API_KEY
from app.schemas.scene import SceneModel


PROMPT = """
You are the image interpretation component of an educational statics tool.
Read one statics problem image and return only JSON matching this shape:
kind, spatial, title, summary, confidence, units, forceUnit, nodes, members,
loads, pointLoads, distributedLoads, warnings, questions, explanation.
Prioritize printed problem data and visible geometry. Do not invent missing
dimensions or answers. Student handwriting is context, not ground truth.
Use relative coordinates and add a warning when dimensions are unclear.
"""


def _json_from_text(text: str) -> dict:
    cleaned = re.sub(r"^```json\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    return json.loads(cleaned)


async def analyze_image(image: bytes, mime_type: str) -> SceneModel:
    if not GOOGLE_AI_API_KEY:
        raise RuntimeError("GOOGLE_AI_API_KEY is not configured.")

    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"text": PROMPT},
                {"inline_data": {"mime_type": mime_type, "data": base64.b64encode(image).decode("ascii")}}
            ]
        }],
        "generationConfig": {"responseMimeType": "application/json", "maxOutputTokens": 4096}
    }
    url = f"{GEMINI_API_BASE.rstrip('/')}/models/{GEMMA_MODEL}:generateContent"
    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post(url, params={"key": GOOGLE_AI_API_KEY}, json=payload)
        response.raise_for_status()
        data = response.json()

    try:
        text = "".join(part.get("text", "") for part in data["candidates"][0]["content"]["parts"])
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Gemma returned no readable analysis content.") from error
    return SceneModel.model_validate(_json_from_text(text))
