-- BLE Beacon Tracker Database Schema
-- PostgreSQL Database Setup

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Beacons table
CREATE TABLE IF NOT EXISTS beacons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    beacon_uuid VARCHAR(36) NOT NULL UNIQUE,
    major_id INTEGER NOT NULL,
    minor_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    location_name VARCHAR(255),
    rssi_reference INTEGER DEFAULT -59,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_beacon_ids UNIQUE(major_id, minor_id)
);

CREATE INDEX idx_beacon_uuid ON beacons(beacon_uuid);
CREATE INDEX idx_beacon_active ON beacons(is_active);

-- Locations table (time-series)
CREATE TABLE IF NOT EXISTS locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    beacon_id UUID NOT NULL REFERENCES beacons(id) ON DELETE CASCADE,
    x FLOAT NOT NULL,
    y FLOAT NOT NULL,
    distance FLOAT NOT NULL,
    rssi INTEGER NOT NULL,
    accuracy FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT location_valid_coords CHECK (x >= 0 AND y >= 0)
);

CREATE INDEX idx_location_beacon_time ON locations(beacon_id, timestamp DESC);
CREATE INDEX idx_location_timestamp ON locations(timestamp DESC);

-- Geofences table
CREATE TABLE IF NOT EXISTS geofences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_id VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    center_x FLOAT NOT NULL,
    center_y FLOAT NOT NULL,
    radius FLOAT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT geofence_valid_radius CHECK (radius > 0)
);

CREATE INDEX idx_geofence_active ON geofences(is_active);

-- Geofence Events table
CREATE TABLE IF NOT EXISTS geofence_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    beacon_id UUID NOT NULL REFERENCES beacons(id) ON DELETE CASCADE,
    geofence_id UUID NOT NULL REFERENCES geofences(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('enter', 'exit', 'dwell', 'movement')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_geofence_event_beacon_time ON geofence_events(beacon_id, timestamp DESC);
CREATE INDEX idx_geofence_event_geofence_time ON geofence_events(geofence_id, timestamp DESC);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('admin', 'user', 'viewer')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_username ON users(username);
CREATE INDEX idx_user_email ON users(email);

-- API Keys table
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE INDEX idx_api_key_user ON api_keys(user_id);

-- Audit Log table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(100),
    details JSONB,
    ip_address INET,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_user_time ON audit_logs(user_id, timestamp DESC);
CREATE INDEX idx_audit_log_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_log_action ON audit_logs(action);

-- Create views for analytics
CREATE OR REPLACE VIEW beacon_latest_location AS
SELECT DISTINCT ON (beacon_id)
    beacon_id,
    x,
    y,
    distance,
    rssi,
    timestamp
FROM locations
ORDER BY beacon_id, timestamp DESC;

CREATE OR REPLACE VIEW geofence_beacon_count AS
SELECT
    g.id,
    g.zone_id,
    g.name,
    COUNT(DISTINCT ge.beacon_id) as beacon_count,
    COUNT(ge.id) as total_events
FROM geofences g
LEFT JOIN geofence_events ge ON g.id = ge.geofence_id
GROUP BY g.id, g.zone_id, g.name;
