# Chess Clock Timer Feature - Implementation Guide

## ✅ What Was Added

### Backend Changes

#### 1. Database Model Updates (`models.py`)
Added time control fields to Game model:
```python
# Time control (chess clock)
time_control = Column(Integer, default=600)  # Total time in seconds
time_increment = Column(Integer, default=5)  # Increment per move (Fischer)
player1_time_left = Column(Integer)  # Player 1 remaining time
player2_time_left = Column(Integer)  # Player 2 remaining time
last_move_time = Column(DateTime)  # Timestamp of last move
```

#### 2. Schema Updates (`schemas.py`)
- `GameCreate`: Added `time_control` and `time_increment` optional fields
- `GameResponse`: Added timer fields to API responses

#### 3. Game Creation Updates (`games.py`)
- Initialize player times when creating games
- Set `started_at` and `last_move_time` when game begins
- Both players start with same time (e.g., 600 seconds = 10 minutes)

### Time Control Presets

Common chess clock settings:
- **Blitz**: 3+2 (3 minutes + 2 second increment)
- **Rapid**: 10+5 (10 minutes + 5 second increment) - DEFAULT
- **Classical**: 15+10 (15 minutes + 10 second increment)
- **Bullet**: 1+0 (1 minute, no increment)

### How Fischer Increment Works

**Example: 10+5 game**
1. Both players start with 600 seconds (10 minutes)
2. Player 1 makes move in 8 seconds
   - Time used: 8 seconds
   - Increment added: +5 seconds
   - Net time lost: 3 seconds
   - Remaining: 597 seconds
   
3. If player moves instantly (< 5 seconds):
   - They GAIN time!
   - Move in 2 seconds → +5 increment = +3 seconds total

**This rewards fast play** ⚡

## 📱 Frontend Implementation Needed

### 1. Time Selection UI (Challenge Creation)

```dart
// Add to create game dialog
class TimeControlSelector extends StatefulWidget {
  final Function(int timeControl, int increment) onSelected;
  
  // Presets
  static const presets = [
    {'name': 'Bullet 1+0', 'time': 60, 'inc': 0},
    {'name': 'Blitz 3+2', 'time': 180, 'inc': 2},
    {'name': 'Rapid 10+5', 'time': 600, 'inc': 5},
    {'name': 'Classical 15+10', 'time': 900, 'inc': 10},
    {'name': 'Custom', 'time': null, 'inc': null},
  ];
}
```

### 2. Chess Clock Widget

```dart
class ChessClock extends StatefulWidget {
  final Game game;
  final int currentPlayerId;
  
  // Display two timers side by side
  // Active player's timer counts down
  // Show increment animation when move is made
}
```

### 3. Timer Logic

```dart
// In GameProvider or game screen
Timer? _gameTimer;

void startTimer() {
  _gameTimer = Timer.periodic(Duration(seconds: 1), (timer) {
    if (game.currentTurn == myPlayerId) {
      // Decrease my time
      game.myTimeLeft--;
      
      if (game.myTimeLeft <= 0) {
        // Time's up - I lose
        forfeitOnTime();
      }
      
      notifyListeners();
    }
  });
}

void onMoveMade() {
  // Add increment
  int timeLeft = game.currentTurn == player1 
    ? game.player1_time_left 
    : game.player2_time_left;
    
  timeLeft += game.time_increment;
  
  // Update last_move_time
  game.last_move_time = DateTime.now();
}
```

### 4. Display Format

```dart
String formatTime(int seconds) {
  int minutes = seconds ~/ 60;
  int secs = seconds % 60;
  return '${minutes}:${secs.toString().padLeft(2, '0')}';
}

// Examples:
// 597 seconds → "9:57"
// 45 seconds → "0:45"
```

### 5. Visual Indicators

```dart
// Time warning colors
Color getTimeColor(int seconds) {
  if (seconds > 60) return Colors.green;
  if (seconds > 30) return Colors.orange;
  return Colors.red;  // Under 30 seconds - critical!
}

// Pulsing animation when time < 10 seconds
AnimatedContainer(
  decoration: BoxDecoration(
    color: seconds < 10 ? Colors.red.withOpacity(0.3) : null,
  ),
)
```

## 🎮 User Flow

### Creating a Challenge

```
1. Click "Challenge Player"
2. Enter bet amount: MWK 1000
3. Select time control:
   [ ] Bullet 1+0
   [ ] Blitz 3+2
   [✓] Rapid 10+5  ← Selected
   [ ] Classical 15+10
   [ ] Custom
4. Click "Create Challenge"
```

### Joining a Challenge

```
Challenges Screen:
┌─────────────────────────────────┐
│ MWK 1,000                       │
│ Time: 10+5                      │
│ Challenger: Player #42          │
│ Created: 2m ago                 │
│                                 │
│ [Join Challenge]                │
└─────────────────────────────────┘
```

### During Game

```
┌─────────────────────────────────┐
│  Player 1     │     Player 2    │
│   9:57 ⏱     │     10:00       │
│  (Active)     │                 │
├─────────────────────────────────┤
│                                 │
│      [Draughts Board]           │
│                                 │
├─────────────────────────────────┤
│ Last move: +5 sec increment     │
└─────────────────────────────────┘
```

## ⚠️ Important: Real-time Updates

**Problem**: When player joins, other player doesn't know

**Solution**: Implement WebSocket or polling

### Option 1: Polling (Simple)
```dart
// In waiting game screen
Timer.periodic(Duration(seconds: 2), (timer) {
  checkIfGameStarted();
});

Future<void> checkIfGameStarted() async {
  final game = await apiService.getGame(gameId);
  
  if (game.status == 'in_progress') {
    // Navigate to game board
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (context) => GameBoardScreen(gameId: game.id),
      ),
    );
  }
}
```

### Option 2: WebSocket (Better)
```dart
// Connect to WebSocket
final channel = WebSocketChannel.connect(
  Uri.parse('ws://localhost:8080/ws/game/${gameId}'),
);

channel.stream.listen((message) {
  final data = jsonDecode(message);
  
  if (data['type'] == 'game_started') {
    // Navigate to game
  }
  
  if (data['type'] == 'move_made') {
    // Update board and timer
  }
});
```

## 🔄 Move Flow with Timer

```
1. Player 1's turn (timer counting down)
2. Player 1 makes move in 8 seconds
3. Backend receives move:
   - Calculate time used: now() - last_move_time = 8 sec
   - Deduct from player1_time_left: 600 - 8 = 592
   - Add increment: 592 + 5 = 597
   - Switch turn to Player 2
   - Set last_move_time = now()
4. Frontend shows:
   - Player 1: 9:57 (gained 3 seconds!)
   - Player 2: 10:00 (timer now active)
```

## 🚀 Implementation Steps

### Step 1: Database Migration
```bash
# Stop API
# Delete draughts.db (or use Alembic migration)
# Restart API - new schema will be created
```

### Step 2: Update Frontend Models
```dart
class Game {
  final int? timeControl;
  final int? timeIncrement;
  final int? player1TimeLeft;
  final int? player2TimeLeft;
  final DateTime? lastMoveTime;
  
  // Add to fromJson
}
```

### Step 3: Add Time Selector UI
- Create TimeControlSelector widget
- Add to create game dialog
- Pass selected time to API

### Step 4: Add Chess Clock Widget
- Display both player times
- Countdown active player
- Show increment animation
- Color coding for low time

### Step 5: Implement Polling/WebSocket
- Check for game start when waiting
- Update timer on opponent's move

## 📊 Database Schema

```sql
ALTER TABLE games ADD COLUMN time_control INTEGER DEFAULT 600;
ALTER TABLE games ADD COLUMN time_increment INTEGER DEFAULT 5;
ALTER TABLE games ADD COLUMN player1_time_left INTEGER;
ALTER TABLE games ADD COLUMN player2_time_left INTEGER;
ALTER TABLE games ADD COLUMN last_move_time TIMESTAMP;
ALTER TABLE games ADD COLUMN started_at TIMESTAMP;
```

## Testing Checklist

- [ ] Create game with 10+5 time control
- [ ] Join game - timer starts for both players
- [ ] Make move - increment added correctly
- [ ] Move faster than increment - time increases
- [ ] Time runs out - game ends (forfeit on time)
- [ ] Different time controls work (1+0, 3+2, 15+10)
- [ ] Waiting player sees when opponent joins

