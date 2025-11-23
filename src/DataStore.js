const User = require('./models/User');
const DraughtsGame = require('./game/DraughtsGame');
const { v4: uuidv4 } = require('uuid');

class DataStore {
  constructor() {
    this.users = new Map();
    this.games = new Map();
    this.sessions = new Map(); // userId -> sessionToken
  }

  // User operations
  createUser(username, password) {
    // Check if username exists
    for (const user of this.users.values()) {
      if (user.username === username) {
        return { success: false, error: 'Username already exists' };
      }
    }

    const user = new User(username, password);
    user.id = uuidv4();
    this.users.set(user.id, user);
    
    return { success: true, user };
  }

  authenticateUser(username, password) {
    for (const user of this.users.values()) {
      if (user.username === username && user.password === password) {
        const sessionToken = uuidv4();
        this.sessions.set(sessionToken, user.id);
        return { success: true, user, sessionToken };
      }
    }
    return { success: false, error: 'Invalid credentials' };
  }

  getUserBySession(sessionToken) {
    const userId = this.sessions.get(sessionToken);
    if (userId) {
      return this.users.get(userId);
    }
    return null;
  }

  getUser(userId) {
    return this.users.get(userId);
  }

  logout(sessionToken) {
    this.sessions.delete(sessionToken);
  }

  // Game operations
  createGame(player1Id, player2Id, betAmount = 0) {
    const player1 = this.users.get(player1Id);
    const player2 = this.users.get(player2Id);

    if (!player1 || !player2) {
      return { success: false, error: 'Invalid players' };
    }

    // Check if both players can afford the bet
    if (betAmount > 0) {
      if (!player1.canPlaceBet(betAmount)) {
        return { success: false, error: 'Player 1 has insufficient balance' };
      }
      if (!player2.canPlaceBet(betAmount)) {
        return { success: false, error: 'Player 2 has insufficient balance' };
      }

      // Deduct bets from both players
      player1.deductBet(betAmount);
      player2.deductBet(betAmount);
    }

    const game = new DraughtsGame(player1Id, player2Id, betAmount);
    game.id = uuidv4();
    game.startGame();
    this.games.set(game.id, game);

    // Increment games played for both players
    player1.incrementGamesPlayed();
    player2.incrementGamesPlayed();

    return { success: true, game };
  }

  getGame(gameId) {
    return this.games.get(gameId);
  }

  makeMove(gameId, playerId, fromRow, fromCol, toRow, toCol) {
    const game = this.games.get(gameId);
    if (!game) {
      return { success: false, error: 'Game not found' };
    }

    if (!game.isPlayerTurn(playerId)) {
      return { success: false, error: 'Not your turn' };
    }

    const result = game.makeMove(fromRow, fromCol, toRow, toCol);

    // Handle game over and winnings
    if (result.success && game.gameOver && game.winner) {
      const winner = this.users.get(game.winner);
      if (winner && game.betAmount > 0) {
        const winnings = game.betAmount * 2;
        winner.addWinnings(winnings);
      }
    }

    return result;
  }

  getActiveGames() {
    const activeGames = [];
    for (const game of this.games.values()) {
      if (!game.gameOver) {
        activeGames.push(game.getState());
      }
    }
    return activeGames;
  }

  getUserGames(userId) {
    const userGames = [];
    for (const game of this.games.values()) {
      if (game.player1Id === userId || game.player2Id === userId) {
        userGames.push(game.getState());
      }
    }
    return userGames;
  }
}

// Singleton instance
const dataStore = new DataStore();

module.exports = dataStore;
