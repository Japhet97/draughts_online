@echo off
echo ========================================
echo  ADB SETUP - Add to PATH
echo ========================================
echo.
echo ADB is installed but not in PATH
echo This script will set it up for this session
echo.
pause

echo.
echo Setting up ADB path...
echo.

REM Add ADB to PATH for this session
set PATH=%PATH%;C:\Users\Jafe\AppData\Local\Android\Sdk\platform-tools

echo.
echo Testing ADB...
echo.
adb version

echo.
echo ========================================
echo  ADB READY!
echo ========================================
echo.
echo Now setting up reverse port forwarding...
echo.
adb devices
echo.
echo If you see your device listed above, we're ready!
echo.
pause

echo.
echo Setting up ADB reverse...
echo.
adb reverse tcp:8080 tcp:8080

echo.
echo Verifying...
echo.
adb reverse --list

echo.
echo ========================================
echo  COMPLETE!
echo ========================================
echo.
echo Your phone can now access PC at:
echo http://localhost:8080
echo.
echo Next:
echo 1. Start backend (new terminal):
echo    cd D:\Projects\Draughts_online\backend
echo    python -m uvicorn app.main:app --reload --port 8080
echo.
echo 2. Install app (keep THIS window open):
echo    cd D:\Projects\Draughts_online\frontend\draughts_app
echo    flutter run --release
echo.
pause
