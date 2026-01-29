# 🚀 BLE Beacon Tracker - Οδηγός Εγκατάστασης και Χρήσης

## Πώς να το χρησιμοποιήσετε - Τρεις επιλογές

---

## ΕΠΙΛΟΓΗ 1: Γρήγορη Εγκατάσταση με Docker (Συνιστώμενη) ⭐

### Προαπαιτούμενα:
- Docker Desktop (https://www.docker.com/products/docker-desktop)
- Git (https://git-scm.com/)

### Βήματα:

```bash
# 1. Κατεβάστε το repository
git clone https://github.com/manolasg1974-maker/ble-beacon-tracker.git
cd ble-beacon-tracker

# 2. Τρέξτε όλα τα services με Docker
docker-compose up -d

# 3. Περιμένετε 2-3 λεπτά για να ξεκινήσουν τα services

# 4. Ανοίξτε τον browser σας
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
# Database: localhost:5432
```

### Επιβεβαίωση ότι όλα δουλεύουν:
```bash
# Ελέγξτε το health status
curl http://localhost:5000/api/health

# Θα πρέπει να δείτε:
# {"status": "healthy", "timestamp": "...", "version": "1.0.0"}
```

---

## ΕΠΙΛΟΓΗ 2: Manual Installation (για Development)

### Προαπαιτούμενα:
- Python 3.8+ (https://www.python.org/)
- PostgreSQL 12+ (https://www.postgresql.org/)
- Node.js 14+ (https://nodejs.org/)
- Git

### Βήμα 1: Εγκατάσταση Backend

```bash
# Κλωνοποιήστε το repository
git clone https://github.com/manolasg1974-maker/ble-beacon-tracker.git
cd ble-beacon-tracker

# Δημιουργήστε virtual environment
python3 -m venv venv

# Ενεργοποιήστε το virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\\Scripts\\activate

# Εγκαταστήστε dependencies
pip install -r requirements.txt

# Δημιουργήστε .env αρχείο
cat > .env << EOF
DATABASE_URL=postgresql://bletracker:changeMe123@localhost:5432/ble_tracker_db
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
EOF
```

### Βήμα 2: Setup PostgreSQL Database

```bash
# Συνδεθείτε στο PostgreSQL
psql -U postgres

# Δημιουργήστε database και user
CREATE USER bletracker WITH PASSWORD 'changeMe123';
CREATE DATABASE ble_tracker_db OWNER bletracker;
GRANT ALL PRIVILEGES ON DATABASE ble_tracker_db TO bletracker;
\\q

# Φορτώστε το schema
psql -U bletracker -d ble_tracker_db -f db/schemas.sql
```

### Βήμα 3: Τρέξτε το Backend

```bash
python backend/app.py
# Θα δείτε: * Running on http://0.0.0.0:5000
```

### Βήμα 4: Εγκατάσταση Frontend

```bash
# Σε νέο terminal
cd frontend
npm install
npm start
# Θα ανοίξει αυτόματα http://localhost:3000
```

---

## ΕΠΙΛΟΓΗ 3: Κατέβασμα ως Mobile App

### Για iOS (Apple):

```bash
# Προαπαιτούμενα:
# - Mac με Xcode (https://developer.apple.com/xcode/)
# - iOS 13+ device ή simulator

# Βήματα:
git clone https://github.com/manolasg1974-maker/ble-beacon-tracker.git
cd ble-beacon-tracker/mobile/ios

# Ανοίξτε στο Xcode
open BLEBeaconTracker.xcodeproj

# Επιλέξτε το device σας ή simulator
# Πατήστε Play (Cmd+R) για να τρέξει
```

### Για Android:

```bash
# Προαπαιτούμενα:
# - Android Studio (https://developer.android.com/studio)
# - Android 10+ device ή emulator

# Βήματα:
git clone https://github.com/manolasg1974-maker/ble-beacon-tracker.git
cd ble-beacon-tracker/mobile/android

# Ανοίξτε στο Android Studio
# File > Open > ble-beacon-tracker/mobile/android

# Επιλέξτε device/emulator
# Κάνε click Build > Run 'app'
```

### Σημαντικό για Mobile Apps:

⚠️ **Δικαιώματα που χρειάζονται:**

**iOS:**
- Bluetooth permissions (NSBluetoothPeripheralUsageDescription)
- Location permissions (NSLocationWhenInUseUsageDescription)

**Android:**
- BLUETOOTH
- BLUETOOTH_ADMIN
- BLUETOOTH_SCAN (Android 12+)
- ACCESS_FINE_LOCATION
- ACCESS_COARSE_LOCATION

Και τα δύο ζητούν άδεια στο runtime όταν ξεκινά η εφαρμογή.

---

## Πώς να Χρησιμοποιήσετε την Εφαρμογή

### Web Dashboard (React)

1. **Ανοίξτε** http://localhost:3000
2. **Δείτε Beacons** - Λίστα όλων των beacon που βρίσκονται κοντά
3. **Real-time Heatmap** - Οπτικοποίηση της θέσης των beacon
4. **Δημιουργία Geofences** - Ορίστε ζώνες για alerts
5. **API Dashboard** - Παρακολουθείστε τα API calls

### Mobile App (iOS/Android)

1. **Ανοίξτε την εφαρμογή** - Ζητά άδεια Bluetooth
2. **Σαρώστε Beacons** - Βρίσκει κοντινά beacons
3. **Δείτε Απόσταση** - Εμφανίζει거리 σε μέτρα (RSSI)
4. **Alerts** - Ειδοποιήσεις όταν εισέρχεστε/εξέρχεστε ζώνες

---

## API Endpoints - Προγραμματιστές

### Health Check
```bash
GET http://localhost:5000/api/health
```

### Λήψη όλων των Beacons
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/beacons
```

### Ενημέρωση Θέσης
```bash
curl -X POST http://localhost:5000/api/locations \
  -H "Content-Type: application/json" \
  -d '{
    "beacon_id": "uuid-here",
    "x": 10.5,
    "y": 20.3,
    "rssi": -75
  }'
```

### Δημιουργία Geofence
```bash
curl -X POST http://localhost:5000/api/geofences \
  -H "Content-Type: application/json" \
  -d '{
    "zone_id": "zone_1",
    "name": "Αποθήκη A",
    "center_x": 100,
    "center_y": 150,
    "radius": 50
  }'
```

### Λήψη Heatmap
```bash
curl http://localhost:5000/api/heatmap?zone_id=zone_1&time_range=1h
```

---

## Troubleshooting

### Πρόβλημα: "Connection refused" σε localhost:5432
**Λύση:** 
```bash
# Ελέγξτε αν το PostgreSQL τρέχει
# Docker:
docker ps | grep postgres

# Manual:
sudo systemctl status postgresql
```

### Πρόβλημα: "Module not found" για requirements
**Λύση:**
```bash
# Βεβαιωθείτε ότι το virtual environment είναι ενεργό
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate    # Windows

# Αποδώστε ξανά τα requirements
pip install -r requirements.txt
```

### Πρόβλημα: Bluetooth δεν δουλεύει στο Mobile
**Λύση:**
- Ενεργοποιήστε το Bluetooth στην συσκευή
- Δώστε άδειες στην εφαρμογή (Settings > App Permissions)
- Επανεκκινήστε την εφαρμογή
- Ελέγξτε ότι τα beacons είναι σε λειτουργία

### Πρόβλημα: CORS errors στο Frontend
**Λύση:**
```bash
# Ελέγξτε ότι το backend τρέχει
curl http://localhost:5000/api/health

# Και ότι το frontend είναι σε σωστό port
# (λογικό να είναι http://localhost:3000)
```

---

## Επόμενα Βήματα

### 1. **Δημιουργία λογαριασμού χρήστη**
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "email": "your@email.com",
    "password": "secure_password"
  }'
```

### 2. **Παραμετροποίηση Beacons**
- Προσθέστε τα UUID των δικών σας beacons
- Ορίστε reference power και path loss exponent

### 3. **Ρύθμιση Geofences**
- Δημιουργήστε ζώνες για τις χώρες σας
- Ενεργοποιήστε alerts

### 4. **Integration με συστήματα τρίτων**
- Χρησιμοποιήστε τα REST API endpoints
- Συνδέστε με CRM, ERP, ή άλλα συστήματα

---

## Άδεια

Αυτό το project είναι licensed κάτω από **MIT License**

---

## Υποστήριξη

Για ερωτήσεις ή προβλήματα:
1. Ελέγξτε το [GitHub Issues](https://github.com/manolasg1974-maker/ble-beacon-tracker/issues)
2. Ανοίξτε νέο Issue με λεπτομέρειες
3. Δείτε την [API Documentation](./COMPLETE_README.md)
