from pathlib import Path
import os
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]


ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


GROQ_API_KEY = None

import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


ROUTER_MODEL = "openai/gpt-oss-20b"

CODING_MODEL = "openai/gpt-oss-20b"

RAG_MODEL = "openai/gpt-oss-20b"

WEB_SEARCH_MODEL = "openai/gpt-oss-120b"

DOCUMENTS_DIR = (
    BASE_DIR
    / "data"
    / "documents"
)

GENERATED_PROJECTS_DIR = (
    BASE_DIR
    / "generated_projects"
)

MAX_CODING_ATTEMPTS = 3


APP_NAME = "Multi-Agent System"

TEMPERATURE = 0