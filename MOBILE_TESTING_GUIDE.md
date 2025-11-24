# Mobile Testing Setup Guide

## 🎯 Quick Setup for Mobile Testing

### Step 1: Find Your PC's IP Address
Your current PC IP: **10.197.75.27**

To verify or find it again:
```bash
# Windows
ipconfig
# Look for "IPv4 Address" under your WiFi adapter
```

### Step 2: Start Backend API (Accessible from Mobile)

```bash
cd D:\Projects\Draughts_online\backend
.\run.bat
```

The API will now be accessible at:
- ✅ Local PC: `http://localhost:8080`
- ✅ From Phone: `http://10.197.75.27:8080`
- ✅ API Docs: `http://10.197.75.27:8080/docs`

### Step 3: Configure Flutter for Mobile

**Option A: Use the mobile config (RECOMMENDED)**

1. Rename current config:
```bash
cd D:\Projects\Draughts_online\frontend\draughts_app\lib\config
move app_config.dart app_config_web.dart
move app_config_mobile.dart app_config.dart
```

2. The mobile config already has your IP: `10.197.75.27`

**Option B: Edit existing config**

Edit `lib/config/app_config.dart`:
```dart
// Change this line:
static const String baseUrl = 'http://localhost:8080/api/v1';

// To this:
static const String baseUrl = 'http://10.197.75.27:8080/api/v1';
```

### Step 4: Connect Your Phone

**Prerequisites:**
- Phone and PC on same WiFi network
- USB Debugging enabled (Android) or phone trusted (iOS)

**For Android:**
```bash
cd D:\Projects\Draughts_online\frontend\draughts_app

# Connect phone via USB
# Enable USB Debugging in Developer Options

# Check device connected
flutter devices

# Run on phone
flutter run
```

**For iOS:**
```bash
cd D:\Projects\Draughts_online\frontend\draughts_app

# Connect iPhone via USB
# Trust the computer on your phone

# Check device connected
flutter devices

# Run on iPhone
flutter run
```

### Step 5: Test the Connection

**Test 1: API Reachable from Phone**

On your phone's browser, visit:
```
http://10.197.75.27:8080/docs
```

You should see the Swagger API documentation.

**Test 2: Register & Login**

1. Open the app on your phone
2. Register with:
   - Username: `mobiletest`
   - Email: `mobile@test.com`
   - Password: `Test123!`
   - Phone: `+265991234567`

3. You should successfully login

**Test 3: Create Game**

1. Click "Play vs AI"
2. Enter bet amount: MWK 100
3. Select time: Rapid (10+5)
4. See network warning ⚠️
5. Confirm and create game
6. **Game board should load!**

## 🐛 Troubleshooting

### Issue: Cannot connect to API

**Fix 1: Check Firewall**
```bash
# Allow Python through Windows Firewall
# Windows Defender Firewall > Allow an app
# Find Python and enable both Private and Public
```

**Fix 2: Test from PC first**
```bash
# On PC browser, test:
http://10.197.75.27:8080/docs

# If this doesn't work, firewall is blocking
```

**Fix 3: Temporary disable firewall (TESTING ONLY)**
```bash
# Windows Settings > Update & Security > Windows Security
# Firewall & network protection > Private network
# Turn off temporarily
```

### Issue: App shows "Network Error"

**Fix 1: Verify IP in config**
```dart
// lib/config/app_config.dart should have:
static const String baseUrl = 'http://10.197.75.27:8080/api/v1';
```

**Fix 2: Restart app**
```bash
# In Flutter terminal, press:
R  # Full restart
```

**Fix 3: Clear and rebuild**
```bash
flutter clean
flutter pub get
flutter run
```

### Issue: Gameplay not working

**Debug Steps:**

1. **Check API logs** (in backend terminal)
   - Look for POST requests when you click pieces
   - Check for any errors

2. **Check browser console** (F12)
   - Look for network errors
   - Check API responses

3. **Test API directly**
   - Visit `http://10.197.75.27:8080/docs`
   - Try creating game via Swagger UI
   - Copy `game_id` and test moves

## 📱 Device-Specific URLs

### Android Emulator
```dart
static const String baseUrl = 'http://10.0.2.2:8080/api/v1';
```

### iOS Simulator  
```dart
static const String baseUrl = 'http://localhost:8080/api/v1';
```

### Real Android Phone (WiFi)
```dart
static const String baseUrl = 'http://10.197.75.27:8080/api/v1';
```

### Real iPhone (WiFi)
```dart
static const String baseUrl = 'http://10.197.75.27:8080/api/v1';
```

### Chrome/Edge (Web)
```dart
static const String baseUrl = 'http://localhost:8080/api/v1';
```

## ✅ Current Configuration

**Backend:**
- Host: `0.0.0.0` (all interfaces)
- Port: `8080`
- CORS: Enabled for all origins (*)
- Your IP: `10.197.75.27`

**Frontend:**
- Config: `app_config_mobile.dart` (ready to use)
- Base URL: `http://10.197.75.27:8080/api/v1`

## 🚀 Quick Commands

```bash
# Start API for mobile
cd D:\Projects\Draughts_online\backend
.\run.bat

# Run on Android phone
cd D:\Projects\Draughts_online\frontend\draughts_app
flutter run

# Or select device if multiple connected
flutter devices
flutter run -d <device-id>

# Check app logs
flutter logs
```

## 🎮 Testing Gameplay

1. **Register/Login**
2. **Create AI Game:**
   - Bet: MWK 100
   - Time: Rapid (10+5)
   - Difficulty: Expert
3. **Click on piece** to select
4. **Click destination** to move
5. **Timer counts down**
6. **AI responds automatically**

If pieces don't move, check:
- Backend logs for errors
- Network tab in browser dev tools
- Game state in API (`/games/{game_id}`)

