# Draughts Online - Real Money Gaming Platform

A robust, scalable online draughts (checkers) gaming platform with real money betting, built with Flutter and Python FastAPI.

## 🎮 Features

### Core Gaming Features
- **Player vs AI**: Play against an expert AI opponent with multiple difficulty levels (Easy, Medium, Hard, Expert)
- **Player vs Player**: Challenge other players online with real-time gameplay
- **ELO Rating System**: Players are rated based on their performance
- **Leaderboard**: See top-ranked players
- **Game History**: Track all your previous games

### Financial Features
- **Secure Deposits**: Deposit money via PayChangu mobile money integration
- **Instant Withdrawals**: Withdraw winnings to your mobile money account
- **10% Commission**: Platform takes 10% commission on all game winnings
- **Balance Management**: Real-time balance tracking
- **Transaction History**: Complete audit trail of all transactions

### Betting System
- **Flexible Betting**: Set your own bet amounts (within platform limits)
- **AI Betting**: Bet against AI - win to earn money
- **PvP Betting**: Both players stake money, winner takes pot minus 10% commission
- **Challenge System**: Create open challenges or counter-offer amounts
- **Fair Play**: All bets are locked before game starts

### Technical Features
- **RESTful API**: Clean, documented API built with FastAPI
- **PostgreSQL Database**: Robust data persistence
- **Redis Caching**: Fast session and game state management
- **Docker Support**: Easy deployment with Docker Compose
- **Extensible Architecture**: Ready for additional games (dice roll, etc.)
- **WebSocket Support**: Real-time game updates (to be implemented)

## 🏗️ Architecture

```
┌─────────────────┐
│  Flutter App    │  (Mobile Client)
│  (iOS/Android)  │
└────────┬────────┘
         │ HTTPS/WSS
         ▼
┌─────────────────┐
│   FastAPI       │  (Python Backend)
│   REST API      │
└────────┬────────┘
         │
    ┌────┴─────┬────────────┐
    ▼          ▼            ▼
┌────────┐ ┌───────┐  ┌──────────┐
│PostreSQL│ │ Redis │  │PayChangu │
│         │ │       │  │ Gateway  │
└─────────┘ └───────┘  └──────────┘
```

## 📁 Project Structure

```
Draughts_online/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       ├── auth.py          # Authentication endpoints
│   │   │       ├── games.py         # Game management endpoints
│   │   │       └── payments.py      # Payment endpoints
│   │   ├── core/
│   │   │   ├── config.py           # Application configuration
│   │   │   └── security.py         # Authentication & encryption
│   │   ├── db/
│   │   │   └── database.py         # Database connection
│   │   ├── games/
│   │   │   ├── draughts_engine.py  # Game logic
│   │   │   └── draughts_ai.py      # AI opponent
│   │   ├── models/
│   │   │   └── models.py           # SQLAlchemy models
│   │   ├── schemas/
│   │   │   └── schemas.py          # Pydantic schemas
│   │   ├── services/
│   │   │   ├── game_service.py     # Game business logic
│   │   │   └── payment_service.py  # Payment integration
│   │   └── main.py                 # Application entry point
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── .env.example
├── frontend/                        # Flutter app (to be created)
└── docs/
    └── API.md                       # API documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+ (or use Docker)
- Redis (or use Docker)
- PayChangu API credentials

### Backend Setup

1. **Clone and navigate to backend**:
```bash
cd backend
```

2. **Create environment file**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Update .env with your credentials**:
```env
DATABASE_URL=postgresql://draughts_user:draughts_pass@localhost:5432/draughts_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secret-key-change-this
PAYCHANGU_API_KEY=your_paychangu_api_key
PAYCHANGU_SECRET_KEY=your_paychangu_secret_key
PAYCHANGU_CALLBACK_URL=https://your-domain.com/api/v1/payments/callback
```

4. **Run with Docker (Recommended)**:
```bash
docker-compose up -d
```

5. **Or run locally**:
```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations (if using Alembic)
# alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

6. **Access the API**:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📱 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/leaderboard` - Get top players
- `GET /api/v1/auth/online-players` - Get online players

### Games
- `POST /api/v1/games/create` - Create new game
- `POST /api/v1/games/move` - Make a move
- `GET /api/v1/games/active` - Get active games
- `GET /api/v1/games/history` - Get game history
- `GET /api/v1/games/waiting` - Get waiting games
- `GET /api/v1/games/{game_id}` - Get game details
- `POST /api/v1/games/{game_id}/join` - Join a game
- `POST /api/v1/games/{game_id}/forfeit` - Forfeit game

### Payments
- `POST /api/v1/payments/deposit` - Initiate deposit
- `POST /api/v1/payments/withdraw` - Initiate withdrawal
- `POST /api/v1/payments/callback` - Payment callback (webhook)
- `GET /api/v1/payments/transactions` - Get transaction history
- `GET /api/v1/payments/balance` - Get current balance

## 🎲 Game Rules

### Draughts Rules
- 8x8 board with 12 pieces per player
- Pieces move diagonally forward
- Captures are mandatory when available
- Pieces become kings when reaching opposite end
- Kings can move both forward and backward
- Win by capturing all opponent pieces or blocking all moves

### Betting Rules
1. Players set bet amount when creating game
2. For AI games: Player stakes bet amount
3. For PvP games: Both players stake equal amounts (or counter-offer)
4. Winner receives: `Total Pot - 10% Commission`
5. Draw: Both players get their stakes back
6. Forfeit: Opponent wins by default

### Rating System
- New players start at 1000 ELO
- Ratings adjust based on game results using ELO algorithm
- Beating higher-rated players gains more points
- Minimum 5 games required for leaderboard

## 💰 Payment Integration (PayChangu)

### Setup PayChangu
1. Create account at [PayChangu](https://www.paychangu.com)
2. Get API credentials from dashboard
3. Configure webhook URL for callbacks
4. Update .env file with credentials

### Supported Operations
- Mobile Money Deposits (M-Pesa, Tigo Pesa, Airtel Money, etc.)
- Mobile Money Withdrawals
- Transaction verification
- Webhook callbacks for status updates

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- API signature verification for payments
- SQL injection prevention (SQLAlchemy ORM)
- CORS protection
- Input validation with Pydantic
- Secure transaction handling

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📈 Future Enhancements

### Planned Features
- [ ] WebSocket support for real-time gameplay
- [ ] Dice roll game integration
- [ ] Tournament mode
- [ ] Friend system
- [ ] Chat functionality
- [ ] Push notifications
- [ ] Admin dashboard
- [ ] Analytics and reporting
- [ ] Multiple currency support
- [ ] Referral program

### Technical Improvements
- [ ] Celery for async tasks
- [ ] Rate limiting
- [ ] Caching layer optimization
- [ ] Load balancing
- [ ] Monitoring & logging (Prometheus, Grafana)
- [ ] CI/CD pipeline
- [ ] Automated backups

## 🤝 Contributing

This is a proprietary project. Contact the development team for collaboration opportunities.

## 📄 License

All rights reserved. Proprietary software.

## 🐛 Known Issues

- WebSocket real-time updates not yet implemented
- Need to implement automated testing
- Payment callback needs production webhook URL

## 📞 Support

For support, contact: [your-support-email]

---

**Built with ❤️ for passionate draughts players**
