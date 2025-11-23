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

// Register a new user
router.post('/register', (req, res) => {
  const { username, password } = req.body;
  
  if (!username || !password) {
    return res.status(400).json({ error: 'Username and password required' });
  }

  const result = dataStore.createUser(username, password);
  
  if (result.success) {
    res.json({
      success: true,
      user: {
        id: result.user.id,
        username: result.user.username,
        balance: result.user.balance
      }
    });
  } else {
    res.status(400).json(result);
  }
});

// Login
router.post('/login', (req, res) => {
  const { username, password } = req.body;
  
  if (!username || !password) {
    return res.status(400).json({ error: 'Username and password required' });
  }

  const result = dataStore.authenticateUser(username, password);
  
  if (result.success) {
    res.json({
      success: true,
      sessionToken: result.sessionToken,
      user: {
        id: result.user.id,
        username: result.user.username,
        balance: result.user.balance
      }
    });
  } else {
    res.status(401).json(result);
  }
});

// Logout
router.post('/logout', requireAuth, (req, res) => {
  const sessionToken = req.headers['x-session-token'];
  dataStore.logout(sessionToken);
  res.json({ success: true });
});

// Get user profile
router.get('/profile', requireAuth, (req, res) => {
  res.json(req.user.getStats());
});

module.exports = router;
