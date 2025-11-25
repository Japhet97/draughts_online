@echo off
echo ========================================
echo  BUILD APK FILE FOR SHARING
echo ========================================
echo.
echo This will create an APK file you can install on any Android phone
echo.
pause

cd /d %~dp0

echo.
echo Building APK (Release mode)...
echo This takes 3-5 minutes...
echo.
flutter build apk --release

echo.
echo ========================================
echo  BUILD COMPLETE!
echo ========================================
echo.
echo APK file location:
echo %cd%\build\app\outputs\flutter-apk\app-release.apk
echo.
echo You can now:
echo 1. Email this APK to yourself
echo 2. Copy to phone via USB
echo 3. Upload to Google Drive and download on phone
echo.
echo To install on phone:
echo 1. Transfer APK to phone
echo 2. Tap the APK file
echo 3. Allow "Install from unknown sources"
echo 4. Install
echo.
pause
