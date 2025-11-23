# API Documentation

## Base URL
```
Development: http://localhost:8000/api/v1
Production: https://your-domain.com/api/v1
```

## Authentication
All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Response Format
All responses follow this format:
```json
{
  "success": true,
  "data": {},
  "message": "Optional message"
}
```

Error responses:
```json
{
  "detail": "Error message"
}
```

---

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe",
  "phone_number": "+255712345678"
}
```

**Response:** (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "rating": 1000,
    "balance": 0.0,
    "total_games": 0,
    "games_won": 0,
    "games_lost": 0,
    "is_online": false,
    "created_at": "2025-11-16T10:00:00Z"
  }
}
```

### Login
**POST** `/auth/login`

Login to existing account.

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Response:** Same as register

### Get Current User
**GET** `/auth/me`

Get authenticated user's profile.

**Headers:** Authorization required

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "rating": 1250,
  "balance": 5000.00,
  "total_games": 45,
  "games_won": 28,
  "games_lost": 15,
  "games_drawn": 2,
  "is_online": true
}
```

### Leaderboard
**GET** `/auth/leaderboard?limit=100`

Get top-rated players.

**Response:**
```json
[
  {
    "username": "ChampionPlayer",
    "rating": 2000,
    "total_games": 150,
    "games_won": 100,
    "games_lost": 45,
    "games_drawn": 5,
    "win_rate": 66.67
  }
]
```

---

## Game Endpoints

### Create Game
**POST** `/games/create`

Create a new game (vs AI or waiting for player).

**Request Body:**
```json
{
  "mode": "vs_ai",
  "bet_amount": 1000.00,
  "ai_difficulty": "expert"
}
```

OR for player vs player:
```json
{
  "mode": "vs_player",
  "bet_amount": 500.00
}
```

**Response:**
```json
{
  "id": 1,
  "mode": "vs_ai",
  "bet_amount": 1000.00,
  "status": "in_progress",
  "player1_id": 1,
  "player2_id": null,
  "current_turn": 1,
  "board_state": {
    "board": [[0, 2, 0, 2, ...], ...],
    "current_player": 1,
    "move_count": 0
  },
  "created_at": "2025-11-16T10:00:00Z"
}
```

### Make Move
**POST** `/games/move`

Make a move in an active game.

**Request Body:**
```json
{
  "game_id": 1,
  "from_position": [5, 0],
  "to_position": [4, 1]
}
```

**Response:**
```json
{
  "success": true,
  "board_state": {
    "board": [[...], ...],
    "current_player": 2,
    "move_count": 1
  },
  "message": "Move made successfully"
}
```

### Get Active Games
**GET** `/games/active`

Get user's active games.

**Response:** Array of game objects

### Get Game History
**GET** `/games/history?limit=50`

Get user's completed games.

**Response:** Array of game objects

### Get Waiting Games
**GET** `/games/waiting`

Get games waiting for opponents.

**Response:** Array of game objects with `status: "waiting"`

### Join Game
**POST** `/games/{game_id}/join`

Join a waiting game.

**Request Body (optional):**
```json
{
  "counter_offer": 750.00
}
```

**Response:**
```json
{
  "message": "Successfully joined game",
  "game": { ... }
}
```

### Forfeit Game
**POST** `/games/{game_id}/forfeit`

Forfeit an active game.

**Response:**
```json
{
  "message": "Game forfeited"
}
```

---

## Payment Endpoints

### Initiate Deposit
**POST** `/payments/deposit`

Deposit money to account.

**Request Body:**
```json
{
  "amount": 10000.00,
  "payment_method": "paychangu"
}
```

**Response:**
```json
{
  "message": "Deposit initiated. Please check your phone for payment prompt.",
  "transaction_id": 123,
  "reference": "DEP_1_A1B2C3D4E5F6",
  "amount": 10000.00
}
```

### Initiate Withdrawal
**POST** `/payments/withdraw`

Withdraw money from account.

**Request Body:**
```json
{
  "amount": 5000.00,
  "withdrawal_method": "mobile_money"
}
```

**Response:**
```json
{
  "message": "Withdrawal initiated. Funds will be sent to your mobile money account.",
  "transaction_id": 124,
  "reference": "WTH_1_F6E5D4C3B2A1",
  "amount": 5000.00
}
```

### Payment Callback (Webhook)
**POST** `/payments/callback`

PayChangu webhook endpoint (internal use).

**Headers:**
```
X-PayChangu-Signature: <signature>
```

**Request Body:**
```json
{
  "transaction_id": "PYC123456789",
  "status": "success",
  "amount": 10000.00,
  "reference": "DEP_1_A1B2C3D4E5F6",
  "metadata": {}
}
```

### Get Transactions
**GET** `/payments/transactions?limit=50`

Get transaction history.

**Response:**
```json
[
  {
    "id": 123,
    "type": "deposit",
    "amount": 10000.00,
    "balance_before": 0.00,
    "balance_after": 10000.00,
    "payment_status": "completed",
    "created_at": "2025-11-16T10:00:00Z",
    "description": "Deposit of 10000.0"
  }
]
```

### Get Balance
**GET** `/payments/balance`

Get current balance.

**Response:**
```json
{
  "balance": 15000.00,
  "total_deposited": 20000.00,
  "total_withdrawn": 5000.00
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 400  | Bad Request - Invalid input |
| 401  | Unauthorized - Invalid or missing token |
| 403  | Forbidden - Insufficient permissions |
| 404  | Not Found - Resource doesn't exist |
| 500  | Internal Server Error |

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per user

## WebSocket (Coming Soon)

Real-time game updates via WebSocket:
```
ws://localhost:8000/ws/game/{game_id}
```

## Game Board Format

The board is represented as an 8x8 array:
- `0` = Empty square
- `1` = Player 1 piece
- `2` = Player 2 piece
- `-1` = Player 1 king
- `-2` = Player 2 king

Example:
```python
[
  [0, 2, 0, 2, 0, 2, 0, 2],
  [2, 0, 2, 0, 2, 0, 2, 0],
  [0, 2, 0, 2, 0, 2, 0, 2],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 1, 0, 1, 0, 1, 0],
  [0, 1, 0, 1, 0, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 1, 0]
]
```

## Testing with cURL

### Register:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123!",
    "phone_number": "+255712345678"
  }'
```

### Login:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test123!"
  }'
```

### Create Game:
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
