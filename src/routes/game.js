const express = require('express');
const router = express.Router();
const dataStore = require('../DataStore');

// Middleware to check authentication
const requireAuth = (req, res, next) => {
  const sessionToken = req.headers['x-session-token'];
  const user = dataStore.getUserBySession(sessionToken);
  
  if (!user) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  req.user = user;
  next();
};

// Create a new game
router.post('/create', requireAuth, (req, res) => {
  const { opponentUsername, betAmount } = req.body;
  
  if (!opponentUsername) {
    return res.status(400).json({ error: 'Opponent username required' });
  }

  const bet = parseInt(betAmount) || 0;
  
  if (bet < 0) {
    return res.status(400).json({ error: 'Bet amount cannot be negative' });
  }

  // Find opponent by username
  let opponentId = null;
  for (const user of dataStore.users.values()) {
    if (user.username === opponentUsername) {
      opponentId = user.id;
      break;
    }
  }

  if (!opponentId) {
    return res.status(404).json({ error: 'Opponent not found' });
  }

  if (opponentId === req.user.id) {
    return res.status(400).json({ error: 'Cannot play against yourself' });
  }

  const result = dataStore.createGame(req.user.id, opponentId, bet);
  
  if (result.success) {
    res.json({
      success: true,
      game: result.game.getState()
    });
  } else {
    res.status(400).json(result);
  }
});

// Get game state
router.get('/:gameId', requireAuth, (req, res) => {
  const game = dataStore.getGame(req.params.gameId);
  
  if (!game) {
    return res.status(404).json({ error: 'Game not found' });
  }

  // Check if user is part of this game
  if (game.player1Id !== req.user.id && game.player2Id !== req.user.id) {
    return res.status(403).json({ error: 'Not authorized to view this game' });
  }

  res.json(game.getState());
});

// Get valid moves for a piece
router.get('/:gameId/moves/:row/:col', requireAuth, (req, res) => {
  const game = dataStore.getGame(req.params.gameId);
  
  if (!game) {
    return res.status(404).json({ error: 'Game not found' });
  }

  if (game.player1Id !== req.user.id && game.player2Id !== req.user.id) {
    return res.status(403).json({ error: 'Not authorized' });
  }

  const row = parseInt(req.params.row);
  const col = parseInt(req.params.col);

  const moves = game.getValidMoves(row, col);
  res.json({ moves });
});

// Make a move
router.post('/:gameId/move', requireAuth, (req, res) => {
  const { fromRow, fromCol, toRow, toCol } = req.body;
  
  if (fromRow === undefined || fromCol === undefined || toRow === undefined || toCol === undefined) {
    return res.status(400).json({ error: 'Move coordinates required' });
  }

  const result = dataStore.makeMove(
    req.params.gameId,
    req.user.id,
    parseInt(fromRow),
    parseInt(fromCol),
    parseInt(toRow),
    parseInt(toCol)
  );

  if (result.success) {
    const game = dataStore.getGame(req.params.gameId);
    res.json({
      success: true,
      ...result,
      gameState: game.getState()
    });
  } else {
    res.status(400).json(result);
  }
});

// Get user's games
router.get('/user/games', requireAuth, (req, res) => {
  const games = dataStore.getUserGames(req.user.id);
  res.json({ games });
});

// Get active games
router.get('/all/active', requireAuth, (req, res) => {
  const games = dataStore.getActiveGames();
  res.json({ games });
});

module.exports = router;
