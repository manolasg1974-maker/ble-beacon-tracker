"""Configuration settings for BLE Beacon Tracker application."""

import os
from datetime import timedelta

class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost:5432/ble_tracker'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # BLE Configuration
    BLE_SCAN_INTERVAL = 5  # seconds
    BLE_RSSI_THRESHOLD = -100  # dBm
    BLE_MAC_FILTER = []  # Empty = scan all
    
    # Geofencing
    GEOFENCE_CHECK_INTERVAL = 10  # seconds
    GEOFENCE_RADIUS = 50  # meters
    
    # Signal Processing
    KALMAN_PROCESS_VARIANCE = 0.01
    KALMAN_MEASUREMENT_VARIANCE = 4.0
    RSSI_REFERENCE_POWER = -59  # dBm at 1 meter
    PATH_LOSS_EXPONENT = 2.0
    
    # API
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:8000']
    
    # Pagination
    ITEMS_PER_PAGE = 50
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
