# Online Draughts Game with Betting 🎯

An online draughts (checkers) game with real-time betting functionality. Players can compete against each other and win money!

## Features

- **Complete Draughts Game**: Full implementation of draughts rules including:
  - Standard 8x8 board setup
  - Forced capture rule
  - King promotion when pieces reach the opposite end
  - Multi-jump captures
  - Win detection (no pieces or no valid moves)

- **Betting System**: 
  - Place bets before starting a game
  - Winner takes the pot (2x bet amount)
  - Free play option (0 bet amount)
  - Automatic balance management

- **User Management**:
  - User registration and authentication
  - Persistent sessions
  - Starting balance of $1000
  - Track statistics (games played, won, win rate, total winnings)

- **Interactive Web Interface**:
  - Beautiful responsive design
  - Real-time game board visualization
  - Click to select and move pieces
  - Turn indicators
  - Balance and stats display

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Japhet97/draughts_online.git
cd draughts_online
```

2. Install dependencies:
```bash
npm install
```

3. Start the server:
```bash
npm start
```

4. Open your browser and navigate to:
```
http://localhost:3000
```

## How to Play

1. **Register/Login**: Create a new account or login with existing credentials
2. **Start a Game**: 
   - Enter opponent's username
   - Set bet amount (0 for free play)
   - Click "Create Game"
3. **Play**: 
   - Black pieces (player 1) move first
   - Click on your piece to select it
   - Click on destination square to move
   - Captures are mandatory when available
   - Pieces are promoted to kings when reaching the opposite end
4. **Win**: Capture all opponent pieces or leave them with no valid moves
5. **Collect Winnings**: Winner automatically receives 2x the bet amount

## Game Rules

- **Movement**: Regular pieces move diagonally forward one square
- **Kings**: Can move diagonally in all directions
- **Captures**: Jump over opponent pieces to capture them (mandatory)
- **Multi-Jumps**: If you can capture more pieces after a jump, you must continue
- **Promotion**: Pieces reaching the opposite end become kings (marked with crown)
- **Win Conditions**: 
  - Opponent has no pieces left
  - Opponent has no valid moves

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/profile` - Get user profile and stats

### Game
- `POST /api/game/create` - Create new game with betting
- `GET /api/game/:gameId` - Get game state
- `POST /api/game/:gameId/move` - Make a move
- `GET /api/game/:gameId/moves/:row/:col` - Get valid moves for a piece
- `GET /api/game/user/games` - Get user's games
- `GET /api/game/all/active` - Get all active games

## Technologies Used

- **Backend**: Node.js, Express
- **Frontend**: Vanilla JavaScript, HTML5 Canvas, CSS3
- **Data Storage**: In-memory (for simplicity)

## Project Structure

```
draughts_online/
├── src/
│   ├── game/
│   │   ├── Board.js          # Game board logic
│   │   └── DraughtsGame.js   # Core game mechanics
│   ├── models/
│   │   └── User.js           # User model with wallet
│   ├── routes/
│   │   ├── auth.js           # Authentication routes
│   │   └── game.js           # Game API routes
│   ├── DataStore.js          # In-memory data storage
│   └── server.js             # Express server setup
├── public/
│   ├── css/
│   │   └── style.css         # Styling
│   ├── js/
│   │   └── app.js            # Frontend logic
│   └── index.html            # Main HTML page
├── package.json
└── README.md
```

## Future Enhancements

- Persistent database storage (MongoDB, PostgreSQL)
- WebSocket support for real-time multiplayer
- Spectator mode
- Game history and replay
- Leaderboards
- Tournament mode
- Password hashing and security improvements
- Mobile app version

## License

ISC

## Author

Created for online draughts gaming with betting functionality.
