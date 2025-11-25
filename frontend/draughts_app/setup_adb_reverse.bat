@echo off
echo ========================================
echo  SETUP ADB REVERSE FOR USB TESTING
echo ========================================
echo.
echo This allows your phone to access PC's localhost over USB
echo.
echo Prerequisites:
echo 1. Phone connected via USB
echo 2. USB Debugging enabled
echo.
pause

echo.
echo Step 1: Setting up ADB reverse...
echo.
adb reverse tcp:8080 tcp:8080

echo.
echo Step 2: Verifying reverse is active...
echo.
adb reverse --list

echo.
echo ========================================
echo  SETUP COMPLETE!
echo ========================================
echo.
echo Your phone can now access:
echo http://localhost:8080
echo.
echo This points to your PC's port 8080
echo.
echo Next steps:
echo 1. Make sure app_config.dart uses: http://localhost:8080/api/v1
echo 2. Start backend: python -m uvicorn app.main:app --reload --port 8080
echo 3. Install app: flutter run --release
echo.
pause
