@echo off
echo ========================================
echo  INSTALL APP ON YOUR PHONE
echo  (Using ADB Reverse - Works with Hotspot!)
echo ========================================
echo.
echo Your device: R8YX2058QQE
echo Connection: USB with ADB Reverse
echo API: http://localhost:8080 (on phone)
echo.
pause

cd /d D:\Projects\Draughts_online\frontend\draughts_app

echo.
echo Step 1: Setting up ADB reverse...
echo.
C:\Users\Jafe\AppData\Local\Android\Sdk\platform-tools\adb.exe -s R8YX2058QQE reverse tcp:8080 tcp:8080

echo.
echo Step 2: Verifying connection...
echo.
C:\Users\Jafe\AppData\Local\Android\Sdk\platform-tools\adb.exe -s R8YX2058QQE reverse --list

echo.
echo Step 3: Building and installing app...
echo This takes 3-5 minutes...
echo.
flutter run -d R8YX2058QQE --release

echo.
echo ========================================
echo  INSTALLATION COMPLETE!
echo ========================================
echo.
pause
