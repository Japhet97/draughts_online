# 📱 Install App on Your Phone - Complete Guide

## 🎯 Goal
Install the Draughts app on your Android/iOS phone and connect it to the API running on your PC.

## Prerequisites
- ✅ Your PC and Phone on **same WiFi network**
- ✅ USB cable to connect phone to PC
- ✅ Phone with USB debugging enabled (Android) or trusted (iOS)

## 📝 Step-by-Step Instructions

### STEP 1: Update App Configuration for Mobile

**1.1 Edit the config file:**

Open: `D:\Projects\Draughts_online\frontend\draughts_app\lib\config\app_config.dart`

**1.2 Change the baseUrl:**

Find this line:
```dart
static const String baseUrl = 'http://localhost:8080/api/v1';
```

Change it to:
```dart
static const String baseUrl = 'http://10.197.75.27:8080/api/v1';
```

**1.3 Save the file**

---

### STEP 2: Enable USB Debugging on Your Phone

**For Android:**

1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times (enables Developer Options)
3. Go back to **Settings** → **System** → **Developer Options**
4. Enable **USB Debugging**
5. Connect phone to PC via USB
6. On phone, tap **Allow USB Debugging** when prompted

**For iOS:**

1. Connect iPhone to PC via USB
2. Tap **Trust** on your iPhone when prompted
3. Enter your passcode

---

### STEP 3: Verify Phone Connection

**3.1 Open PowerShell/Terminal:**
```bash
cd D:\Projects\Draughts_online\frontend\draughts_app
```

**3.2 Check if phone is detected:**
```bash
flutter devices
```

**Expected output:**
```
2 connected devices:

SM G991B (mobile) • R5CR30XXXXX • android-arm64 • Android 13
Chrome (web)      • chrome      • web-javascript • Google Chrome 120.0
```

If you see your phone listed → ✅ Connected!

If not → Check USB cable, USB debugging, or try different USB port

---

### STEP 4: Start Backend API (Network Mode)

**4.1 Open PowerShell:**
```bash
cd D:\Projects\Draughts_online\backend
```

**4.2 Start API on network (not just localhost):**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8080
```

This means API is accessible from your phone!

**4.3 Test from your PC browser first:**
```
http://10.197.75.27:8080/docs
```

If this loads → ✅ API is accessible on network

---

### STEP 5: Install App on Phone

**5.1 Build and install in one command:**
```bash
cd D:\Projects\Draughts_online\frontend\draughts_app

# For Android
flutter run --release

# Flutter will:
# - Build the APK
# - Install it on your phone
# - Launch the app
```

**5.2 Wait for build (takes 3-5 minutes first time)**

You'll see:
```
Building APK...
Installing APK...
Launching app...
```

**5.3 App should open on your phone automatically!**

---

### STEP 6: Test the App

**6.1 On your phone, you should see the app:**
- Splash screen
- Login/Register screen

**6.2 Register a new user:**
- Username: `phoneuser`
- Email: `phone@test.com`
- Password: `Test123!`
- Phone: `+265991234567`

**6.3 If registration succeeds → ✅ App is talking to API!**

**6.4 Test creating a game:**
1. Click "Play vs AI"
2. Bet: 100 MWK
3. Time: Rapid (10+5)
4. See network warning
5. Create game
6. Game should load!

---

## 🔧 Alternative: Build APK File to Share

If you want to install without USB cable:

**1. Build release APK:**
```bash
cd D:\Projects\Draughts_online\frontend\draughts_app
flutter build apk --release
```

**2. APK will be at:**
```
D:\Projects\Draughts_online\frontend\draughts_app\build\app\outputs\flutter-apk\app-release.apk
```

**3. Transfer to phone:**
- Email it to yourself
- Upload to Google Drive
- Use USB to copy to phone's Downloads folder

**4. Install on phone:**
- Open file manager
- Tap the APK file
- Allow "Install from unknown sources" if prompted
- Install

---

## 🐛 Troubleshooting

### Issue: "flutter devices" shows no phone

**Fix 1: USB Debugging**
- Settings → Developer Options → USB Debugging → ON
- Unplug and replug USB cable
- Tap "Allow" on phone

**Fix 2: USB Drivers (Windows)**
```bash
# Install Android SDK Platform Tools
# Or install your phone manufacturer's USB drivers
```

**Fix 3: Try different USB cable**
- Some cables are charge-only, need data cable

---

### Issue: App can't connect to API

**Fix 1: Check IP address**
```bash
# On PC:
ipconfig

# Find "IPv4 Address" under WiFi adapter
# Should be something like: 192.168.x.x or 10.x.x.x
```

**Fix 2: Update app_config.dart with correct IP**
```dart
static const String baseUrl = 'http://YOUR_PC_IP:8080/api/v1';
```

**Fix 3: Test API from phone browser**
- On phone, open Chrome
- Visit: `http://10.197.75.27:8080/docs`
- If it loads → API is reachable
- If not → Firewall blocking (see below)

---

### Issue: Windows Firewall blocking

**Fix: Allow Python through firewall**

1. Windows Search → "Firewall"
2. Click "Allow an app through Windows Firewall"
3. Click "Change settings"
4. Click "Allow another app"
5. Browse to Python: `C:\Users\Jafe\AppData\Local\Microsoft\WindowsApps\python.exe`
6. Check both "Private" and "Public"
7. OK

**Or temporarily disable firewall (testing only):**
- Windows Settings → Update & Security → Windows Security
- Firewall & network protection
- Turn off for Private network (temporarily)

---

### Issue: Build fails

**Fix 1: Clean and retry**
```bash
flutter clean
flutter pub get
flutter build apk --release
```

**Fix 2: Check Dart SDK**
```bash
flutter doctor
# Fix any issues shown
```

---

## 📱 Quick Commands Reference

```bash
# Check connected devices
flutter devices

# Run on specific device
flutter run -d <device-id>

# Build APK (takes 3-5 min)
flutter build apk --release

# Install and run in release mode
flutter run --release

# View logs from phone
flutter logs

# Hot reload changes
# Press 'r' in terminal while app running

# Full restart
# Press 'R' in terminal
```

---

## ✅ Success Checklist

After successful install, you should be able to:

- [ ] App opens on phone
- [ ] Register new user
- [ ] Login successfully
- [ ] See balance (starting at 0 or 1000 MWK)
- [ ] Create AI game
- [ ] See network warning
- [ ] Select time control
- [ ] Play game (move pieces)
- [ ] Join challenges
- [ ] Make deposits (test mode)

---

## 🎯 Your Setup

**PC IP:** `10.197.75.27`  
**API Port:** `8080`  
**API URL:** `http://10.197.75.27:8080`  
**Docs:** `http://10.197.75.27:8080/docs`

**Required changes:**
1. ✅ `app_config.dart` → baseUrl: `http://10.197.75.27:8080/api/v1`
2. ✅ Backend → `--host 0.0.0.0` (already configured in run.bat)
3. ✅ CORS → `allow_origins=["*"]` (already configured)

**Everything is ready! Just follow the steps above.** 🚀

---

## 💡 Pro Tips

**Tip 1: Keep PC connected to power**
- API needs to keep running while you test

**Tip 2: Keep phone on same WiFi**
- If you switch networks, app won't connect

**Tip 3: Use `flutter run` for development**
- Hot reload lets you test changes instantly
- Press 'r' to reload, 'R' to restart

**Tip 4: Use `--release` for testing performance**
- Runs faster
- Closer to production build

**Tip 5: Check backend logs**
- Watch API terminal for errors
- Every request shows up in logs

---

## 🚀 Next: Testing Multiplayer

Once app works on your phone:

1. Open app on your phone (Player 1)
2. Open app on Chrome (Player 2)
3. Player 1: Create challenge (MWK 1000)
4. Player 2: Join challenge
5. Play against each other!

Or test with 2 phones on same WiFi! 📱📱

