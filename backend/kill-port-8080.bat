@echo off
echo Stopping service on port 8080...
echo.

REM Find and kill process on port 8080
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    echo Killing process ID: %%a
    taskkill /F /PID %%a
)

echo.
echo Port 8080 is now free!
echo.
echo Now run run.bat to start the API
pause
