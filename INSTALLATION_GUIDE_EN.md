# 🚀 BLE Beacon Tracker - Installation & Usage Guide

## How to Use It - Three Options

---

## OPTION 1: Quick Installation with Docker (Recommended) ⭐

### Prerequisites:
- Docker Desktop (https://www.docker.com/products/docker-desktop)
- Git (https://git-scm.com/)

### Steps:

```bash
# 1. Clone the repository
git clone https://github.com/manolasg1974-maker/ble-beacon-tracker.git
cd ble-beacon-tracker

# 2. Run all services with Docker
docker-compose up -d

# 3. Wait 2-3 minutes for services to start

# 4. Open your browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
# Database: localhost:5432
```

### Verify Everything Works:
```bash
# Check health status
curl http://localhost:5000/api/health

# You should see:
# {"status": "healthy", "timestamp": "...", "version": "1.0.0"}
```

---

## OPTION 2: Manual Installation (For Development)

### Prerequisites:
- Python 3.8+ (https://www.python.org/)
- PostgreSQL 12+ (https://www.postgresql.org/)
- Node.js 14+ (https://nodejs.org/)
- Git

### Step 1: Install Backend

```bash
# Clone the repository
git clone https://github.com/manolasg1974-maker/ble-beacon-tracker.git
cd ble-beacon-tracker

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://bletracker:changeMe123@localhost:5432/ble_tracker_db
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
EOF
```

### Step 2: Setup PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE USER bletracker WITH PASSWORD 'changeMe123';
CREATE DATABASE ble_tracker_db OWNER bletracker;
GRANT ALL PRIVILEGES ON DATABASE ble_tracker_db TO bletracker;
\\q

# Load the schema
psql -U bletracker -d ble_tracker_db -f db/schemas.sql
```

### Step 3: Run the Backend

```bash
python backend/app.py
# You should see: * Running on http://0.0.0.0:5000
```

### Step 4: Install Frontend

```bash
# In a new terminal
cd frontend
npm install
npm start
# Will automatically open http://localhost:3000
```

---

## OPTION 3: Download as Mobile App

### For iOS (Apple):

```bash
# Prerequisites:
# - Mac with Xcode (https://developer.apple.com/xcode/)
# - iOS 13+ device or simulator

# Steps:
git clone https://github.com/manolasg1974-maker/ble-beacon-tracker.git
cd ble-beacon-tracker/mobile/ios

# Open in Xcode
open BLEBeaconTracker.xcodeproj

# Select your device or simulator
# Press Play (Cmd+R) to run
```

### For Android:

```bash
# Prerequisites:
# - Android Studio (https://developer.android.com/studio)
# - Android 10+ device or emulator

# Steps:
git clone https://github.com/manolasg1974-maker/ble-beacon-tracker.git
cd ble-beacon-tracker/mobile/android

# Open in Android Studio
# File > Open > ble-beacon-tracker/mobile/android

# Select device/emulator
# Click Build > Run 'app'
```

### Important for Mobile Apps:

⚠️ **Required Permissions:**

**iOS:**
- Bluetooth (NSBluetoothPeripheralUsageDescription)
- Location (NSLocationWhenInUseUsageDescription)

**Android:**
- BLUETOOTH
- BLUETOOTH_ADMIN
- BLUETOOTH_SCAN (Android 12+)
- ACCESS_FINE_LOCATION
- ACCESS_COARSE_LOCATION

Both will request runtime permissions when the app starts.

---

## How to Use the Application

### Web Dashboard (React)

1. **Open** http://localhost:3000
2. **View Beacons** - List of all nearby beacons
3. **Real-time Heatmap** - Visualize beacon locations
4. **Create Geofences** - Define zones for alerts
5. **API Dashboard** - Monitor API calls

### Mobile App (iOS/Android)

1. **Open the app** - Requests Bluetooth permission
2. **Scan Beacons** - Finds nearby beacons
3. **View Distance** - Shows distance in meters (RSSI)
4. **Alerts** - Notifications when entering/leaving zones

---

## API Endpoints for Developers

### Health Check
```bash
GET http://localhost:5000/api/health
```

### Get All Beacons
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \\
  http://localhost:5000/api/beacons
```

### Update Location
```bash
curl -X POST http://localhost:5000/api/locations \\
  -H "Content-Type: application/json" \\
  -d '{
    "beacon_id": "uuid-here",
    "x": 10.5,
    "y": 20.3,
    "rssi": -75
  }'
```

### Create Geofence
```bash
curl -X POST http://localhost:5000/api/geofences \\
  -H "Content-Type: application/json" \\
  -d '{
    "zone_id": "zone_1",
    "name": "Warehouse A",
    "center_x": 100,
    "center_y": 150,
    "radius": 50
  }'
```

### Get Heatmap
```bash
curl http://localhost:5000/api/heatmap?zone_id=zone_1&time_range=1h
```

---

## Troubleshooting

### Problem: "Connection refused" at localhost:5432
**Solution:**
```bash
# Check if PostgreSQL is running
# Docker:
docker ps | grep postgres

# Manual:
sudo systemctl status postgresql
```

### Problem: "Module not found" for requirements
**Solution:**
```bash
# Make sure virtual environment is active
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate    # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Problem: Bluetooth not working on mobile
**Solution:**
- Enable Bluetooth on your device
- Grant permissions to the app (Settings > App Permissions)
- Restart the app
- Check that beacons are powered on

### Problem: CORS errors in frontend
**Solution:**
```bash
# Check backend is running
curl http://localhost:5000/api/health

# Verify frontend is on correct port
# (should be http://localhost:3000)
```

---

## Next Steps

### 1. **Create User Account**
```bash
curl -X POST http://localhost:5000/api/auth/signup \\
  -H "Content-Type: application/json" \\
  -d '{
    "username": "your_username",
    "email": "your@email.com",
    "password": "secure_password"
  }'
```

### 2. **Configure Beacons**
- Add your beacon UUIDs
- Set reference power and path loss exponent

### 3. **Setup Geofences**
- Create zones for your locations
- Enable alerts for events

### 4. **Integrate with Third-Party Systems**
- Use REST API endpoints
- Connect with CRM, ERP, or other systems

---

## Features Included

| Feature | Description |
|---------|-------------|
| **Real-Time Tracking** | Continuous BLE beacon scanning |
| **Signal Processing** | Kalman filter for noise reduction |
| **Location Heatmaps** | Visualize beacon density patterns |
| **Geofencing** | Zone-based alerts and events |
| **Multi-Platform** | iOS, Android, Web support |
| **REST API** | Complete API for integrations |
| **PostgreSQL** | Time-series optimized database |
| **Security** | JWT authentication & RBAC |
| **Docker Support** | Full containerization |

---

## License

This project is licensed under **MIT License**

---

## Support

For questions or issues:
1. Check [GitHub Issues](https://github.com/manolasg1974-maker/ble-beacon-tracker/issues)
2. Open a new issue with details
3. See [API Documentation](./COMPLETE_README.md)

---

## Quick Start Comparison

| Method | Time | Requirements | Best For |
|--------|------|--------------|----------|
| **Docker** | 5 min | Docker + Git | Everyone (simplest) |
| **Manual** | 20 min | Python, PostgreSQL, Node.js | Developers |
| **Mobile** | 30 min | Xcode/Android Studio | App users |

**Recommendation: Start with Docker!** 🐳

All code and resources are available in the GitHub repository with complete implementations for all platforms.
