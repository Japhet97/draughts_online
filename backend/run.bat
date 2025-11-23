@echo off
echo Starting Draughts API Server...
echo.
C:\Users\Jafe\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
echo.
pause
