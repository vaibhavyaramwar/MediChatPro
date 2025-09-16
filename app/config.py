import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Self-hosted Model Configuration
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://69.19.137.87:8000/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "not-needed")
OPENAI_EMBEDDING_BASE = os.getenv("OPENAI_EMBEDDING_BASE", "http://69.19.137.107:8000/v1")
OPENAI_EMBEDDING_KEY = os.getenv("OPENAI_EMBEDDING_KEY", "dummy")

# Model Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-20b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")

# Legacy Euri AI Configuration (keeping for backward compatibility)
EURI_API_KEY = os.getenv("EURI_API_KEY", "euri-4e452443eac7f3adca982989e1e152a66c882ba4f9c287cacbc90db914415b63")

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com"),
    'smtp_port': int(os.getenv("EMAIL_SMTP_PORT", "587")),
    'sender_email': os.getenv("EMAIL_SENDER", "genai.project.group@gmail.com"),
    'sender_password': os.getenv("EMAIL_PASSWORD", "chmj tqkn xepk rtbl"),
    'receiver_email': os.getenv("EMAIL_RECEIVER", "vaibhav.yaramwar@gmail.com")
}