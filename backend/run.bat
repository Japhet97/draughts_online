@echo off
echo Starting Draughts API Server...
echo.
echo API accessible at:
echo - Local: http://localhost:8080
echo - Network: http://10.197.75.27:8080
echo - Mobile: Use 10.197.75.27:8080 in your phone
echo.
C:\Users\Jafe\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
echo.
pause
