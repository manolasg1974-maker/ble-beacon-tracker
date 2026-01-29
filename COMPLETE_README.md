# BLE Beacon Tracker

## 🚀 Advanced Bluetooth Low Energy Beacon Tracking System

A comprehensive, production-ready BLE beacon tracking solution featuring real-time location heatmaps, intelligent geofencing, advanced signal processing with Kalman filtering, and multi-platform support.

---

## ✨ Key Features

### 1. **Real-Time Location Tracking**
- Continuous BLE beacon scanning and monitoring
- High-precision distance estimation using RSSI (Received Signal Strength Indicator)
- Real-time location updates with minimal latency
- Support for hundreds of simultaneous beacon tracking

### 2. **Advanced Signal Processing**
- **Kalman Filter Implementation**: Reduces RSSI noise and improves accuracy
- **RSSI Path Loss Modeling**: Accurate distance calculation using propagation models
- **Multi-point Averaging**: Smoothing over multiple RSSI measurements
- **Frequency Hopping Analysis**: Handles BLE channel hopping interference

### 3. **Location Heatmaps**
- Real-time visualization of beacon density and movement patterns
- Grid-based heatmap generation with configurable resolution
- Time-range filtering (1h, 24h, 7d, 30d)
- Zone-specific analytics and reporting

### 4. **Intelligent Geofencing**
- Circular geofence zone creation and management
- Enter/Exit event detection with timestamp logging
- Dwell time tracking and movement analytics
- Configurable radius and alert thresholds
- Automatic event triggering and webhook notifications

### 5. **Multi-Platform Support**
- **iOS App**: Native Swift implementation using CoreBluetooth
- **Android App**: Kotlin with Android BLE Manager
- **Web Dashboard**: React.js with real-time WebSocket updates
- **REST API**: Complete HTTP API for third-party integrations

### 6. **Database Integration**
- **PostgreSQL**: Primary data storage with full schema optimization
- **Time-Series Optimization**: Efficient storage of location history
- **Real-Time Analytics**: Built-in queries for heatmaps and patterns
- **Data Retention**: Configurable archival and cleanup policies

### 7. **Security & Authentication**
- JWT token-based API authentication
- Role-based access control (RBAC)
- Encrypted credential storage
- Audit logging for all API calls
- UUID validation for beacon identification

### 8. **Performance Monitoring**
- Battery life prediction for mobile clients
- Signal quality metrics and diagnostics
- API response time tracking
- Resource utilization monitoring

---

## 🏗️ Project Structure

```
ble-beacon-tracker/
├── backend/
│   ├── app.py                 # Flask application factory
│   ├── config.py              # Configuration management
│   ├── signal_processing.py   # Kalman filter & RSSI processing
│   ├── geofencing.py          # Geofence management
│   ├── api/
│   │   ├── routes.py          # REST API endpoints
│   │   ├── models.py          # Database models
│   │   └── auth.py            # Authentication handlers
│   ├── services/
│   │   ├── beacon_service.py  # Beacon management logic
│   │   ├── location_service.py# Location tracking
│   │   └── geofence_service.py# Geofence processing
│   └── utils/
│       ├── logger.py          # Logging configuration
│       └── decorators.py      # Custom decorators
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API service calls
│   │   └── utils/             # Frontend utilities
│   └── package.json
├── mobile/
│   ├── ios/                   # Swift iOS app
│   └── android/               # Kotlin Android app
├── db/
│   ├── schemas.sql            # Database schema
│   ├── migrations/            # Database migrations
│   └── seeds/                 # Initial data
├── docs/
│   ├── API.md                 # API documentation
│   ├── ARCHITECTURE.md        # System architecture
│   └── INSTALLATION.md        # Setup guide
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker orchestration
└── README.md                  # This file
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Node.js 14+ (for frontend)
- Docker & Docker Compose (optional)

### Backend Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ble-beacon-tracker.git
cd ble-beacon-tracker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
flask db upgrade

# Run backend
python backend/app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

### Using Docker

```bash
docker-compose up -d
```

---

## 📡 REST API Endpoints

### Health Check
```
GET /api/health
```

### Beacons
```
GET /api/beacons                    # List all beacons
GET /api/beacons/<id>               # Get beacon details
POST /api/beacons                   # Create new beacon
PUT /api/beacons/<id>               # Update beacon
DELETE /api/beacons/<id>            # Delete beacon
```

### Locations
```
POST /api/locations                 # Update beacon location
GET /api/locations/<beacon_id>      # Get location history
```

### Heatmaps
```
GET /api/heatmap?zone_id=...&time_range=1h
```

### Geofences
```
GET /api/geofences                  # List all geofences
POST /api/geofences                 # Create geofence
DELETE /api/geofences/<id>          # Delete geofence
```

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# BLE Settings
BLE_SCAN_INTERVAL = 5           # Scan interval in seconds
BLE_RSSI_THRESHOLD = -100       # Minimum signal strength

# Signal Processing
KALMAN_PROCESS_VARIANCE = 0.01
KALMAN_MEASUREMENT_VARIANCE = 4.0
RSSI_REFERENCE_POWER = -59      # dBm at 1 meter
PATH_LOSS_EXPONENT = 2.0

# Geofencing
GEOFENCE_RADIUS = 50            # Default radius in meters
GEOFENCE_CHECK_INTERVAL = 10    # Check interval in seconds

# Database
SQLALCHEMY_DATABASE_URI = "postgresql://..."
```

---

## 📊 Signal Processing Details

### Kalman Filter
The Kalman filter reduces noise in RSSI measurements:
```
Prediction: P = P + Q
Update: K = P / (P + R)
        x = x + K * (measurement - x)
        P = (1 - K) * P
```

### Distance Estimation
RSSI-to-distance conversion using path loss model:
```
distance = 10^((RSSI_ref - RSSI) / (10 * n))

where:
RSSI_ref = Reference power at 1m
n = Path loss exponent (typically 2.0)
```

---

## 🔐 Security

- **API Authentication**: JWT tokens with expiration
- **Data Encryption**: HTTPS for all communications
- **Audit Logging**: All API calls are logged with timestamps
- **Role-Based Access**: Admin, User, and Viewer roles
- **Input Validation**: All inputs validated server-side

---

## 📈 Performance Metrics

- **Beacon Scanning**: 100-500ms per scan cycle
- **Location Update Latency**: <1 second
- **RSSI Accuracy**: ±5-10 meters (typical indoor)
- **Database Query Time**: <100ms for 1000 beacons
- **API Response Time**: <200ms average

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 📞 Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

## 🗺️ Roadmap

- [ ] Machine learning for improved location accuracy
- [ ] Advanced analytics dashboard
- [ ] Multi-region support
- [ ] Mobile app optimization for battery life
- [ ] Integration with popular IoT platforms
- [ ] GraphQL API endpoint

---

**Built with ❤️ for indoor positioning and asset tracking**
