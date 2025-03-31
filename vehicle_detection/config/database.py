from dotenv import load_dotenv
import os
from pathlib import Path

# Lấy đường dẫn tới thư mục gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file từ thư mục gốc
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Cấu hình Database
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'vehicle_detection'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Tạo connection string
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Debug: In ra đường dẫn để kiểm tra
print(f"Loading .env from: {os.path.join(BASE_DIR, '.env')}")