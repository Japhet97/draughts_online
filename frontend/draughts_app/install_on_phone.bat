@echo off
echo ========================================
echo  INSTALL DRAUGHTS APP ON YOUR PHONE
echo ========================================
echo.
echo Prerequisites:
echo 1. Phone connected via USB
echo 2. USB Debugging enabled on phone
echo 3. Backend API must be running
echo.
echo Your PC IP: 10.197.75.27
echo API URL: http://10.197.75.27:8080
echo.
pause

echo.
echo Step 1: Checking connected devices...
echo.
flutter devices
echo.

echo Step 2: Building and installing app...
echo This will take 3-5 minutes...
echo.
flutter run --release

echo.
echo Installation complete!
echo.
pause
