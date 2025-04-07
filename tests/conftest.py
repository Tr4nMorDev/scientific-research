import os
import sys
from pathlib import Path

# Add project root to PYTHONPATH
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from vehicle_detection.config.settings import SQLALCHEMY_CONFIG, APP_CONFIG
from vehicle_detection.config.database import init_db
from vehicle_detection.src.entity import Base

# Mock TrafficDetector before importing app
@pytest.fixture(autouse=True)
def mock_traffic_detector(mocker):
    """Mock traffic detector fixture"""
    class MockDetector:
        def __init__(self):
            pass
            
        def detect(self, frame):
            return {
                'vehicle_count': 5,
                'density': 0.5,
                'vehicles': [
                    {
                        'type': 'car',
                        'confidence': 0.95,
                        'bbox': [100, 100, 200, 200]
                    },
                    {
                        'type': 'truck',
                        'confidence': 0.85,
                        'bbox': [300, 300, 400, 400]
                    }
                ]
            }
    
    mocker.patch('vehicle_detection.src.detection.traffic_detector.TrafficDetector', MockDetector)
    return MockDetector()

# Import app after mocking TrafficDetector
from vehicle_detection.server import app

@pytest.fixture(scope="session")
def test_config():
    """Test configuration fixture"""
    return {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
        **SQLALCHEMY_CONFIG,  # Include other SQLAlchemy configs
        **{k: v for k, v in APP_CONFIG.items() if k != 'port'}  # Include app configs except port
    }

@pytest.fixture(scope="session")
def test_app(test_config):
    """Test Flask application fixture"""
    # Create a new Flask app instance for testing
    app.config.update(test_config)
    
    with app.app_context():
        # Initialize database
        db = init_db(app)
        
        # Create all tables
        db.create_all()
        
        yield app
        
        # Cleanup after all tests
        db.session.remove()
        db.drop_all()
        
        # Remove test database file
        test_db = Path('test.db')
        if test_db.exists():
            test_db.unlink()

@pytest.fixture(scope="function")
def test_client(test_app):
    """Test client fixture"""
    return test_app.test_client()

@pytest.fixture(scope="function")
def db_session(test_app):
    """Database session fixture"""
    from vehicle_detection.config.database import db
    
    with test_app.app_context():
        # Start a new transaction
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Create a new session
        session = db.create_scoped_session(
            options={"bind": connection, "binds": {}}
        )
        
        # Use the session
        db.session = session
        
        yield session
        
        # Cleanup after each test
        session.close()
        transaction.rollback()
        connection.close()

def test_database_operations(db_session):
    from vehicle_detection.src.entity import TrafficData
    
    new_traffic = TrafficData(
        location_name="Test Location",
        density=0.5,
        vehicle_count=5,
        status="Normal",
        lat=10.0,
        lng=106.0
    )
    
    db_session.add(new_traffic)
    db_session.commit()
    
    result = db_session.query(TrafficData).first()
    assert result is not None
    assert result.location_name == "Test Location"
