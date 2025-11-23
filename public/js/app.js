// Global state
let sessionToken = null;
let currentUser = null;
let currentGame = null;
let selectedPiece = null;
let canvas = null;
let ctx = null;

// Constants
const SQUARE_SIZE = 80;
const PIECE_RADIUS = 30;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  canvas = document.getElementById('game-board');
  ctx = canvas.getContext('2d');

  // Event listeners
  document.getElementById('login-form').addEventListener('submit', handleLogin);
  document.getElementById('register-form').addEventListener('submit', handleRegister);
  document.getElementById('logout-btn').addEventListener('click', handleLogout);
  document.getElementById('create-game-form').addEventListener('submit', handleCreateGame);
  document.getElementById('back-to-lobby').addEventListener('click', backToLobby);
  document.getElementById('new-game-btn').addEventListener('click', backToLobby);
  canvas.addEventListener('click', handleBoardClick);

  // Check for existing session
  const savedToken = localStorage.getItem('sessionToken');
  if (savedToken) {
    sessionToken = savedToken;
    loadUserProfile();
  }
});

// Auth functions
function showTab(tab, buttonElement) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
  
  if (buttonElement) {
    buttonElement.classList.add('active');
  }
  document.getElementById(`${tab}-tab`).classList.add('active');
}

async function handleLogin(e) {
  e.preventDefault();
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  const response = await apiCall('/api/auth/login', 'POST', { username, password });
  
  if (response.success) {
    sessionToken = response.sessionToken;
    currentUser = response.user;
    localStorage.setItem('sessionToken', sessionToken);
    showMessage('Login successful!', 'success');
    showProfileSection();
  } else {
    showMessage(response.error || 'Login failed', 'error');
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const username = document.getElementById('register-username').value;
  const password = document.getElementById('register-password').value;

  const response = await apiCall('/api/auth/register', 'POST', { username, password });
  
  if (response.success) {
    showMessage('Registration successful! Please login.', 'success');
    showTab('login');
    document.getElementById('login-username').value = username;
  } else {
    showMessage(response.error || 'Registration failed', 'error');
  }
}

async function handleLogout() {
  await apiCall('/api/auth/logout', 'POST', {});
  sessionToken = null;
  currentUser = null;
  localStorage.removeItem('sessionToken');
  showAuthSection();
  showMessage('Logged out successfully', 'info');
}

async function loadUserProfile(showUI = true) {
  const response = await apiCall('/api/auth/profile', 'GET');
  
  if (response.username) {
    currentUser = response;
    if (showUI) {
      showProfileSection();
    }
  } else {
    sessionToken = null;
    localStorage.removeItem('sessionToken');
    showAuthSection();
  }
}

// Game functions
async function handleCreateGame(e) {
  e.preventDefault();
  const opponentUsername = document.getElementById('opponent-username').value;
  const betAmount = parseInt(document.getElementById('bet-amount').value) || 0;

  const response = await apiCall('/api/game/create', 'POST', { opponentUsername, betAmount });
  
  if (response.success) {
    showMessage('Game created successfully!', 'success');
    currentGame = response.game;
    await loadUserProfile(false); // Refresh balance without showing UI
    showGameSection(); // Then show game
  } else {
    showMessage(response.error || 'Failed to create game', 'error');
  }
}

async function loadGame(gameId) {
  const response = await apiCall(`/api/game/${gameId}`, 'GET');
  
  if (response.id) {
    currentGame = response;
    showGameSection();
  } else {
    showMessage('Failed to load game', 'error');
  }
}

async function makeMove(fromRow, fromCol, toRow, toCol) {
  const response = await apiCall(`/api/game/${currentGame.id}/move`, 'POST', {
    fromRow, fromCol, toRow, toCol
  });

  if (response.success) {
    currentGame = response.gameState;
    selectedPiece = null;
    drawBoard();
    
    if (response.gameOver) {
      showGameOver();
      loadUserProfile(); // Refresh balance
    } else if (response.hasMoreCaptures) {
      showMessage('You can capture more pieces!', 'info');
      selectedPiece = { row: toRow, col: toCol };
      drawBoard();
    }
  } else {
    showMessage(response.error || 'Invalid move', 'error');
  }
}

function handleBoardClick(e) {
  if (!currentGame || currentGame.gameOver) return;

  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  
  const col = Math.floor(x / SQUARE_SIZE);
  const row = Math.floor(y / SQUARE_SIZE);

  if (row < 0 || row >= 8 || col < 0 || col >= 8) return;

  const piece = currentGame.board[row][col];
  const isMyTurn = currentGame.currentPlayer === currentUser.id;

  if (!isMyTurn) {
    showMessage("It's not your turn!", 'error');
    return;
  }

  // Determine player's color
  const myColor = currentGame.player1Id === currentUser.id ? 'black' : 'white';
  
  if (selectedPiece) {
    // Try to move
    makeMove(selectedPiece.row, selectedPiece.col, row, col);
  } else {
    // Select piece
    const isBlack = piece === 1 || piece === 2;
    const isWhite = piece === 3 || piece === 4;
    const isMyPiece = (myColor === 'black' && isBlack) || (myColor === 'white' && isWhite);
    
    if (piece > 0 && isMyPiece) {
      selectedPiece = { row, col };
      drawBoard();
    }
  }
}

function drawBoard() {
  if (!currentGame) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw squares
  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const isLight = (row + col) % 2 === 0;
      ctx.fillStyle = isLight ? '#f0d9b5' : '#b58863';
      ctx.fillRect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE);
    }
  }

  // Highlight selected piece
  if (selectedPiece) {
    ctx.fillStyle = 'rgba(0, 255, 0, 0.3)';
    ctx.fillRect(
      selectedPiece.col * SQUARE_SIZE,
      selectedPiece.row * SQUARE_SIZE,
      SQUARE_SIZE,
      SQUARE_SIZE
    );
  }

  // Draw pieces
  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const piece = currentGame.board[row][col];
      if (piece > 0) {
        drawPiece(row, col, piece);
      }
    }
  }

  // Update turn indicator
  updateTurnIndicator();
}

function drawPiece(row, col, piece) {
  const x = col * SQUARE_SIZE + SQUARE_SIZE / 2;
  const y = row * SQUARE_SIZE + SQUARE_SIZE / 2;

  // Piece color
  const isBlack = piece === 1 || piece === 2;
  const isKing = piece === 2 || piece === 4;

  // Draw outer circle
  ctx.beginPath();
  ctx.arc(x, y, PIECE_RADIUS, 0, Math.PI * 2);
  ctx.fillStyle = isBlack ? '#333' : '#eee';
  ctx.fill();
  ctx.strokeStyle = isBlack ? '#000' : '#ccc';
  ctx.lineWidth = 2;
  ctx.stroke();

  // Draw king crown
  if (isKing) {
    ctx.fillStyle = isBlack ? '#FFD700' : '#DAA520';
    ctx.font = 'bold 24px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('♔', x, y);
  }
}

function updateTurnIndicator() {
  const turnIndicator = document.getElementById('turn-indicator');
  const gameMessage = document.getElementById('game-message');
  const isMyTurn = currentGame.currentPlayer === currentUser.id;

  if (isMyTurn) {
    turnIndicator.textContent = '✓ Your Turn';
    turnIndicator.className = 'turn-indicator your-turn';
    gameMessage.textContent = 'Click on your piece to select it, then click where you want to move';
  } else {
    turnIndicator.textContent = '⏳ Opponent\'s Turn';
    turnIndicator.className = 'turn-indicator opponent-turn';
    gameMessage.textContent = 'Waiting for opponent to make a move...';
  }
}

function showGameOver() {
  const gameOverSection = document.getElementById('game-over-section');
  const gameResult = document.getElementById('game-result');
  const winningsInfo = document.getElementById('winnings-info');

  const isWinner = currentGame.winner === currentUser.id;
  
  if (isWinner) {
    gameResult.textContent = '🎉 You Won!';
    if (currentGame.betAmount > 0) {
      const winnings = currentGame.betAmount * 2;
      winningsInfo.textContent = `You won $${winnings}!`;
    } else {
      winningsInfo.textContent = 'Great game!';
    }
  } else {
    gameResult.textContent = '😔 You Lost';
    if (currentGame.betAmount > 0) {
      winningsInfo.textContent = `You lost $${currentGame.betAmount}`;
    } else {
      winningsInfo.textContent = 'Better luck next time!';
    }
  }

  gameOverSection.classList.remove('hidden');
}

// UI navigation
function showAuthSection() {
  document.getElementById('auth-section').classList.remove('hidden');
  document.getElementById('profile-section').classList.add('hidden');
  document.getElementById('game-setup-section').classList.add('hidden');
  document.getElementById('game-section').classList.add('hidden');
}

function showProfileSection() {
  document.getElementById('auth-section').classList.add('hidden');
  document.getElementById('profile-section').classList.remove('hidden');
  document.getElementById('game-setup-section').classList.remove('hidden');
  document.getElementById('game-section').classList.add('hidden');

  // Update profile info
  document.getElementById('user-name').textContent = currentUser.username;
  document.getElementById('user-balance').textContent = currentUser.balance;
  document.getElementById('games-played').textContent = currentUser.gamesPlayed || 0;
  document.getElementById('games-won').textContent = currentUser.gamesWon || 0;
  document.getElementById('win-rate').textContent = currentUser.winRate || '0%';
  document.getElementById('total-winnings').textContent = currentUser.totalWinnings || 0;
}

function showGameSection() {
  document.getElementById('auth-section').classList.add('hidden');
  document.getElementById('profile-section').classList.add('hidden');
  document.getElementById('game-setup-section').classList.add('hidden');
  document.getElementById('game-section').classList.remove('hidden');
  document.getElementById('game-over-section').classList.add('hidden');

  // Update game info
  const myColor = currentGame.player1Id === currentUser.id ? 'Black' : 'White';
  document.getElementById('your-color').textContent = myColor;
  document.getElementById('game-bet').textContent = currentGame.betAmount;

  drawBoard();
}

function backToLobby() {
  currentGame = null;
  selectedPiece = null;
  loadUserProfile();
}

// Utility functions
async function apiCall(url, method = 'GET', data = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  };

  if (sessionToken) {
    options.headers['X-Session-Token'] = sessionToken;
  }

  if (data && method !== 'GET') {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, options);
    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    return { error: 'Network error' };
  }
}

function showMessage(text, type = 'info') {
  const container = document.getElementById('message-container');
  const message = document.createElement('div');
  message.className = `message ${type}`;
  message.textContent = text;
  
  container.appendChild(message);
  
  setTimeout(() => {
    message.remove();
  }, 4000);
}
