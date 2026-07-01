from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = [
    ".pdf",
    ".docx"
]