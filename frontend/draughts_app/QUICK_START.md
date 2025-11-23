# 🚀 Flutter App - Quick Start Guide

## Getting Started in 5 Minutes

### Prerequisites
- Flutter SDK installed (3.0+)
- Backend API running on `http://localhost:8000`
- Android Studio / Xcode for emulators

---

## 📱 Run the App

### 1. Install Dependencies
```bash
cd D:\Projects\Draughts_online\frontend\draughts_app
flutter pub get
```

### 2. Configure API URL
If your backend is not on `localhost:8000`, update the API URL:

**File**: `lib/config/app_config.dart`
```dart
static const String baseUrl = 'http://YOUR_IP:8000/api/v1';
```

For Android emulator use:
```dart
static const String baseUrl = 'http://10.0.2.2:8000/api/v1';
```

For physical device use your computer's IP:
```dart
static const String baseUrl = 'http://192.168.1.XXX:8000/api/v1';
```

### 3. Run the App
```bash
# List available devices
flutter devices

# Run on connected device
flutter run

# Run in debug mode with hot reload
flutter run --debug

# Run in release mode (faster)
flutter run --release
```

---

## 📖 Usage Guide

### First Time User

#### 1. Register Account
- Open app → Tap "Don't have an account? Register"
- Fill in:
  - Username (unique)
  - Email
  - Password
  - Phone number (+255XXXXXXXXX format)
- Tap "Register"

#### 2. Login
- Enter username and password
- Tap "Login"
- You'll be taken to the Dashboard

### Playing Games

#### VS AI
1. From Dashboard, tap "Play vs AI"
2. Select:
   - Bet Amount (e.g., 100 TZS)
   - AI Difficulty (Easy, Medium, Hard, Expert)
3. Tap "Create"
4. Game board opens automatically
5. Make moves by:
   - Tap a piece to select it
   - Tap a highlighted square to move
6. Win to earn money!

#### VS Player
1. From Dashboard, tap "Challenge Player"
2. Set bet amount
3. Tap "Create"
4. Wait for another player to join
5. Play when matched!

### Managing Money

#### Deposit
1. Go to Wallet tab
2. Tap "Deposit" button
3. Enter:
   - Phone number (without +255)
   - Amount (minimum 1,000 TZS)
4. Complete payment via PayChangu prompt
5. Balance updates automatically

#### Withdraw
1. Go to Wallet tab
2. Tap "Withdraw" button
3. Enter:
   - Phone number (without +255)
   - Amount (less than balance)
4. Request submitted
5. Receive money within 24 hours

### Viewing Stats
1. Go to Profile tab
2. See:
   - Game statistics
   - Win rate
   - Total earnings
3. Tap leaderboard icon to see rankings

---

## 🎮 Game Controls

### Game Board
- **Select Piece**: Tap any of your pieces
- **Move**: Tap a green highlighted square
- **Deselect**: Tap the selected piece again or another piece
- **Forfeit**: Tap flag icon in app bar
- **View Info**: Tap info icon in app bar

### Navigation
- **Bottom Tabs**: Quick access to main sections
- **Back Button**: Return to previous screen
- **Pull to Refresh**: Update data on any list

---

## 🔧 Troubleshooting

### Can't Connect to Backend
**Problem**: "Failed to connect" errors

**Solutions**:
1. Check backend is running: `docker-compose ps`
2. Verify API URL in `app_config.dart`
3. For Android emulator, use `10.0.2.2` instead of `localhost`
4. For physical device, use your computer's local IP
5. Check firewall isn't blocking port 8000

### Login Fails
**Problem**: "Invalid credentials" error

**Solutions**:
1. Verify username and password
2. Try registering a new account
3. Check backend logs for errors

### Deposit/Withdraw Not Working
**Problem**: Payment fails

**Solutions**:
1. Verify phone number format (+255XXXXXXXXX)
2. Ensure backend PayChangu credentials are set
3. Check sufficient balance for withdrawals
4. Try sandbox mode first

### App Crashes
**Problem**: App closes unexpectedly

**Solutions**:
1. Check Flutter version: `flutter doctor`
2. Clear app data and restart
3. Rebuild app: `flutter clean && flutter pub get && flutter run`
4. Check logs: `flutter logs`

---

## 📚 App Structure

### Main Screens

```
├── Splash Screen (Auto)
├── Login / Register
└── Home (Bottom Navigation)
    ├── Dashboard
    │   ├── User stats
    │   ├── Balance
    │   └── Quick actions
    ├── Games
    │   ├── Active games
    │   ├── Waiting games
    │   └── Game history
    ├── Wallet
    │   ├── Balance card
    │   ├── Deposit/Withdraw
    │   └── Transactions
    └── Profile
        ├── User info
        ├── Statistics
        └── Leaderboard
```

### Features by Screen

| Screen | Features |
|--------|----------|
| Dashboard | Stats, Balance, Quick Play |
| Games | Game List, Game Board, Forfeit |
| Wallet | Deposit, Withdraw, Transactions |
| Profile | Stats, Leaderboard, Logout |

---

## 🎨 UI Guide

### Color Scheme
- **Primary**: Blue (#1E88E5) - Main actions
- **Accent**: Orange (#FF6F00) - Highlights
- **Success**: Green - Wins, deposits
- **Error**: Red - Losses, errors
- **Player 1**: Red pieces
- **Player 2**: Blue pieces

### Icons
- 🎮 Game / Play
- 💰 Money / Wallet
- 👤 Profile / User
- 🏆 Win / Achievement
- 📊 Stats / Leaderboard
- ⚙️ Settings
- 🔄 Refresh
- 🚪 Logout

---

## 🧪 Test Accounts

Create test accounts to try the app:

```bash
# User 1
Username: test_player1
Email: player1@test.com
Password: Test123!
Phone: +255712345678

# User 2
Username: test_player2
Email: player2@test.com
Password: Test123!
Phone: +255723456789
```

---

## 📦 Build for Production

### Android APK
```bash
# Build release APK
flutter build apk --release

# Output location
build/app/outputs/flutter-apk/app-release.apk
```

### Android App Bundle (for Play Store)
```bash
flutter build appbundle --release
```

### iOS
```bash
flutter build ios --release
```

---

## 🔍 Debugging

### Enable Debug Mode
```bash
flutter run --debug
```

### View Logs
```bash
flutter logs
```

### Hot Reload
Press `r` in terminal while app is running

### Hot Restart
Press `R` in terminal while app is running

---

## 📝 Common Tasks

### Update Dependencies
```bash
flutter pub upgrade
```

### Clear Cache
```bash
flutter clean
flutter pub get
```

### Check for Issues
```bash
flutter doctor
flutter analyze
```

### Format Code
```bash
flutter format lib/
```

---

## 🆘 Getting Help

### Documentation
- Flutter docs: https://flutter.dev/docs
- Dart docs: https://dart.dev/guides
- Material Design: https://m3.material.io

### Project Files
- `FLUTTER_PROGRESS.md` - Detailed implementation guide
- `FRONTEND_COMPLETE.md` - Completion summary
- Backend `API.md` - API documentation

---

## ✅ Pre-Launch Checklist

Before releasing to users:

- [ ] Test all screens and features
- [ ] Verify API endpoints work
- [ ] Test on multiple devices
- [ ] Test deposit/withdraw flow
- [ ] Check game logic works correctly
- [ ] Verify balance calculations
- [ ] Test error scenarios
- [ ] Enable production API URL
- [ ] Build release APK/IPA
- [ ] Test release build
- [ ] Prepare app store listing

---

**Ready to Play! 🎮**

Open the app, create an account, and start playing draughts for real money!

---

**Last Updated**: November 19, 2025
**Version**: 1.0.0
