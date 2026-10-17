import os


GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY", "")
GEMMA_MODEL = os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it")
GEMINI_API_BASE = os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta")
MAX_IMAGE_BYTES = 12 * 1024 * 1024
