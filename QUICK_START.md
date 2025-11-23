# Quick Start Guide - Testing the Backend

This guide will help you quickly test the Draughts Online backend API.

## Prerequisites
- Python 3.11+ installed
- PostgreSQL installed (or use Docker)
- Git installed

## Option 1: Using Docker (Recommended)

### Step 1: Start the Services
```bash
cd backend
docker-compose up -d
```

This starts:
- PostgreSQL database on port 5432
- Redis on port 6379
- API server on port 8000

### Step 2: Check Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

## Option 2: Manual Setup

### Step 1: Install Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and update:
```env
DATABASE_URL=postgresql://draughts_user:draughts_pass@localhost:5432/draughts_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
```

### Step 3: Create Database
```bash
# Using PostgreSQL
createdb draughts_db

# Or using Docker for just the database
docker run -d \
  --name draughts-db \
  -e POSTGRES_DB=draughts_db \
  -e POSTGRES_USER=draughts_user \
  -e POSTGRES_PASSWORD=draughts_pass \
  -p 5432:5432 \
  postgres:15-alpine
```

### Step 4: Start Server
```bash
uvicorn app.main:app --reload
```

## Testing the API

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testplayer",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "full_name": "Test Player",
    "phone_number": "+255712345678"
  }'
```

**Save the `access_token` from the response!**

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testplayer",
    "password": "SecurePass123!"
  }'
```

### 3. Get User Profile

```bash
# Replace YOUR_TOKEN with the token from login/register
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Check Balance

```bash
curl -X GET http://localhost:8000/api/v1/payments/balance \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. Create a Game vs AI

```bash
curl -X POST http://localhost:8000/api/v1/games/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "mode": "vs_ai",
    "bet_amount": 100,
    "ai_difficulty": "expert"
  }'
```

**Note**: This will fail if user has insufficient balance. You need to deposit money first.

### 6. Simulate Deposit (Testing)

For testing without actual payment integration, you can manually update the database:

```sql
-- Connect to database
psql -U draughts_user -d draughts_db

-- Add balance to user (user_id = 1)
UPDATE users SET balance = 10000 WHERE id = 1;
```

Or use this Python script:

```python
# add_balance.py
from app.db.database import SessionLocal
from app.models.models import User

db = SessionLocal()
user = db.query(User).filter(User.username == "testplayer").first()
if user:
    user.balance = 10000
    db.commit()
    print(f"Added balance to {user.username}. New balance: {user.balance}")
else:
    print("User not found")
db.close()
```

Run it:
```bash
python add_balance.py
```

### 7. Create Game After Adding Balance

```bash
curl -X POST http://localhost:8000/api/v1/games/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "mode": "vs_ai",
    "bet_amount": 100,
    "ai_difficulty": "expert"
  }'
```

**Save the `game_id` from response!**

### 8. Make a Move

```bash
curl -X POST http://localhost:8000/api/v1/games/move \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "game_id": 1,
    "from_position": [5, 0],
    "to_position": [4, 1]
  }'
```

Valid starting moves for Player 1 (bottom):
- From [5,0] to [4,1]
- From [5,2] to [4,1] or [4,3]
- From [5,4] to [4,3] or [4,5]
- From [5,6] to [4,5] or [4,7]

### 9. Get Active Games

```bash
curl -X GET http://localhost:8000/api/v1/games/active \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 10. Get Leaderboard

```bash
curl -X GET http://localhost:8000/api/v1/auth/leaderboard
```

## Using API Documentation (Swagger UI)

The easiest way to test is using the built-in Swagger UI:

1. Open browser: http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

For authenticated endpoints:
1. Click "Authorize" button (top right)
2. Enter: `Bearer YOUR_TOKEN`
3. Click "Authorize"
4. Now you can test authenticated endpoints

## Complete Test Flow

Here's a complete test sequence:

```bash
# 1. Register
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"player1","email":"p1@test.com","password":"Pass123!","phone_number":"+255712345678"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"

# 2. Add balance manually (see above)

# 3. Create game
GAME=$(curl -X POST http://localhost:8000/api/v1/games/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"mode":"vs_ai","bet_amount":100,"ai_difficulty":"easy"}')

echo "Game: $GAME"

GAME_ID=$(echo $GAME | jq -r '.id')

# 4. Make moves until game ends
curl -X POST http://localhost:8000/api/v1/games/move \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"game_id\":$GAME_ID,\"from_position\":[5,0],\"to_position\":[4,1]}"

# 5. Check balance after game
curl -X GET http://localhost:8000/api/v1/payments/balance \
  -H "Authorization: Bearer $TOKEN"
```

## Testing Player vs Player

You need two accounts:

```bash
# Terminal 1: Player 1
TOKEN1=$(curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"player1","email":"p1@test.com","password":"Pass123!","phone_number":"+255712345678"}' \
  | jq -r '.access_token')

# Add balance to player1 (see manual method above)

# Create a game waiting for opponent
curl -X POST http://localhost:8000/api/v1/games/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN1" \
  -d '{"mode":"vs_player","bet_amount":100}'

# Terminal 2: Player 2
TOKEN2=$(curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"player2","email":"p2@test.com","password":"Pass123!","phone_number":"+255712345679"}' \
  | jq -r '.access_token')

# Add balance to player2

# Get waiting games
curl -X GET http://localhost:8000/api/v1/games/waiting \
  -H "Authorization: Bearer $TOKEN2"

# Join game (use game_id from above)
curl -X POST http://localhost:8000/api/v1/games/1/join \
  -H "Authorization: Bearer $TOKEN2"

# Now both players can make moves alternately
```

## Troubleshooting

### Database Connection Error
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Solution**: Make sure PostgreSQL is running and credentials in `.env` are correct.

### Port Already in Use
```
ERROR: [Errno 48] Address already in use
```
**Solution**: Stop other services using port 8000 or change port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Module Not Found Error
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution**: Activate virtual environment and install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Token Expired
```
{"detail": "Invalid authentication credentials"}
```
**Solution**: Login again to get a new token.

## Next Steps

1. ✅ Test all API endpoints
2. ✅ Verify game logic works correctly
3. ✅ Test payment integration (with PayChangu sandbox)
4. ⏭️ Build Flutter mobile app
5. ⏭️ Deploy to production

## Useful Commands

```bash
# View logs (Docker)
docker-compose logs -f api

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Connect to database
docker-compose exec db psql -U draughts_user -d draughts_db

# View all users
docker-compose exec db psql -U draughts_user -d draughts_db -c "SELECT * FROM users;"

# View all games
docker-compose exec db psql -U draughts_user -d draughts_db -c "SELECT * FROM games;"
```

## API Endpoints Reference

- **Auth**: `/api/v1/auth/*`
- **Games**: `/api/v1/games/*`
- **Payments**: `/api/v1/payments/*`
- **Docs**: `/docs`
- **Health**: `/health`

Enjoy testing! 🎮
