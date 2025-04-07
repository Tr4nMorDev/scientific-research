from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Database settings
DB_CONFIG = {
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'vehicle_detection')
}

def get_database_url(testing=False):
    """
    Get database URL for SQLAlchemy
    Args:
        testing (bool): Whether to use testing database
    Returns:
        str: Database URL
    """
    if testing:
        return 'sqlite:///test.db'
    return f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Create DATABASE_URL
DATABASE_URL = get_database_url()

# Flask-SQLAlchemy settings
SQLALCHEMY_CONFIG = {
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': DATABASE_URL
}

# App settings
APP_CONFIG = {
    'host': os.getenv('APP_HOST', '0.0.0.0'),
    'port': int(os.getenv('APP_PORT', 5000)),
    'debug': os.getenv('DEBUG', 'False').lower() == 'true',
    'videos_folder': os.getenv('VIDEOS_FOLDER', 'videos'),
    'cors_enabled': True
}

# Model settings
YOLO_MODEL_PATH = str(BASE_DIR / 'src' /'models' / 'yolov8n.pt')
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.5'))

__all__ = ['DB_CONFIG', 'SQLALCHEMY_CONFIG', 'APP_CONFIG', 'DATABASE_URL', 'YOLO_MODEL_PATH', 'CONFIDENCE_THRESHOLD'] 