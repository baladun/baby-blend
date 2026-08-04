from pathlib import Path

UPLOAD_DIR = Path(__file__).parent / "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_FILE_SIZE_MB = MAX_FILE_SIZE // (1024 * 1024)
MIN_IMAGE_DIMENSION = 256
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
