# Quick Start - Run API Locally (Windows)

## Step 1: Install Python
1. Download Python 3.11+ from: https://www.python.org/downloads/
2. During installation, CHECK "Add Python to PATH"
3. Verify: Open cmd and type `python --version`

## Step 2: Install Dependencies
```bash
cd D:\Projects\Draughts_online\backend
pip install -r requirements.txt
```

## Step 3: Run the API
```bash
cd D:\Projects\Draughts_online\backend
python -m uvicorn app.main:app --reload
```

## Step 4: Test
Open browser: http://localhost:8080/docs

---

## Alternative: Install with Docker (Easier but larger download)

### Step 1: Install Docker Desktop
Download from: https://www.docker.com/products/docker-desktop/

### Step 2: Run with Docker
```bash
cd D:\Projects\Draughts_online\backend
docker compose up -d
```

### Step 3: Test
Open browser: http://localhost:8080/docs

---

## Quick Test Commands

Once API is running, test with:

```bash
# Health check
curl http://localhost:8080/health

# Register user
curl -X POST http://localhost:8080/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"test\",\"email\":\"test@test.com\",\"password\":\"Test123!\",\"phone_number\":\"+255712345678\"}"
```

---

## Troubleshooting

**Python not found?**
- Reinstall Python and check "Add to PATH"
- Restart terminal/cmd

**Port 8080 in use?**
```bash
python -m uvicorn app.main:app --reload --port 8001
```

**Database error?**
- Check .env file exists
- Using SQLite (no database needed)

---

## What You Get

✅ REST API running at http://localhost:8080
✅ Interactive docs at http://localhost:8080/docs
✅ All endpoints ready to use
✅ SQLite database (auto-created)

Now you can test with Swagger UI or connect your Flutter app!
