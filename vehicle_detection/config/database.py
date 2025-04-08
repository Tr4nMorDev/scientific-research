import logging
logging.basicConfig(level=logging.DEBUG)

from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os
from pathlib import Path
from .settings import DB_CONFIG, get_database_url, SQLALCHEMY_CONFIG

# Khởi tạo SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """
    Initialize Flask-SQLAlchemy
    Args:
        app: Flask application instance
    Returns:
        SQLAlchemy instance
    """

    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url(testing=app.config.get('TESTING', False))
    app.config.update(SQLALCHEMY_CONFIG)
    
    db.init_app(app)
    return db

sample_data = [
    ("Nguyen Van Linh - Quan 7", 0.75, 120),
    ("Xa Lo Ha Noi - Thu Duc", 0.60, 90),
    ("Vo Van Kiet - Quan 5", 0.85, 200),
    ("Pham Van Dong - Go Vap", 0.55, 80),
]

def init_postgres_db():
    """
    Khởi tạo PostgreSQL database và các bảng cần thiết
    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
            (DB_CONFIG['database'],)
        )
        
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
        
        cursor.close()
        conn.close()

        conn = psycopg2.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database']
        )
        
        # Connect to the new database and create tables
        cursor = conn.cursor()
        create_tables(cursor)
        conn.commit()
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

def create_tables(cursor):
    """
    Tạo các bảng và index cần thiết
    """
    # Create tables
    tables = [
        """
        CREATE TABLE IF NOT EXISTS traffic_data (
            id SERIAL PRIMARY KEY,
            location_name VARCHAR(100) NOT NULL,
            density FLOAT NOT NULL,
            vehicle_count INTEGER NOT NULL,
            status VARCHAR(50) NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            lat FLOAT NOT NULL,
            lng FLOAT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS traffic_history (
            id SERIAL PRIMARY KEY,
            location_name VARCHAR(100) NOT NULL,
            density FLOAT NOT NULL,
            vehicle_count INTEGER NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]
    
    # Create indexes
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_traffic_data_location ON traffic_data(location_name)",
        "CREATE INDEX IF NOT EXISTS idx_traffic_data_timestamp ON traffic_data(timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_traffic_history_location ON traffic_history(location_name)",
        "CREATE INDEX IF NOT EXISTS idx_traffic_history_timestamp ON traffic_history(timestamp)"
    ]
    
    for table in tables:
        cursor.execute(table)
    
    for index in indexes:
        cursor.execute(index)

def get_db():
    """
    Lấy instance của database để sử dụng
    
    Returns:
        SQLAlchemy instance
    """
    return db

# Tạo một số helper functions
def create_all():
    """Tạo tất cả các bảng được định nghĩa"""
    db.create_all()

def drop_all():
    """Xóa tất cả các bảng"""
    db.drop_all()

# Lấy thông tin cấu hình
print(DB_CONFIG)

# Lấy database URL
database_url = get_database_url()
print(database_url)