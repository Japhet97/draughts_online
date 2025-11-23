const Board = require('./Board');

class DraughtsGame {
  constructor(player1Id, player2Id, betAmount = 0) {
    this.id = null; // Will be set when game is created
    this.player1Id = player1Id; // Black pieces
    this.player2Id = player2Id; // White pieces
    this.board = new Board();
    this.currentPlayer = player1Id; // Black always starts
    this.winner = null;
    this.betAmount = betAmount;
    this.betsLocked = false;
    this.gameStarted = false;
    this.gameOver = false;
    this.moveHistory = [];
  }

  getCurrentPlayerColor() {
    return this.currentPlayer === this.player1Id ? 'black' : 'white';
  }

  isPlayerTurn(playerId) {
    return this.currentPlayer === playerId && !this.gameOver;
  }

  getValidMoves(row, col) {
    const piece = this.board.getPiece(row, col);
    if (piece === 0) return [];

    const playerColor = this.getCurrentPlayerColor();
    const isBlack = this.board.isBlackPiece(piece);
    const isWhite = this.board.isWhitePiece(piece);
    
    // Check if piece belongs to current player
    if ((playerColor === 'black' && !isBlack) || (playerColor === 'white' && !isWhite)) {
      return [];
    }

    const moves = [];
    const captures = [];

    // Direction vectors for movement
    const isKing = this.board.isKing(piece);
    let directions = [];
    
    if (isBlack && !isKing) {
      directions = [[1, -1], [1, 1]]; // Forward for black
    } else if (isWhite && !isKing) {
      directions = [[-1, -1], [-1, 1]]; // Forward for white
    } else if (isKing) {
      directions = [[-1, -1], [-1, 1], [1, -1], [1, 1]]; // All directions
    }

    // Check simple moves and captures
    for (const [dr, dc] of directions) {
      const newRow = row + dr;
      const newCol = col + dc;

      if (this.board.isValidPosition(newRow, newCol)) {
        const targetPiece = this.board.getPiece(newRow, newCol);
        
        if (targetPiece === 0) {
          // Simple move
          moves.push({ fromRow: row, fromCol: col, toRow: newRow, toCol: newCol, isCapture: false });
        } else {
          // Check for capture
          const canCapture = (isBlack && this.board.isWhitePiece(targetPiece)) ||
                           (isWhite && this.board.isBlackPiece(targetPiece));
          
          if (canCapture) {
            const jumpRow = newRow + dr;
            const jumpCol = newCol + dc;
            
            if (this.board.isValidPosition(jumpRow, jumpCol)) {
              const landingPiece = this.board.getPiece(jumpRow, jumpCol);
              if (landingPiece === 0) {
                captures.push({
                  fromRow: row,
                  fromCol: col,
                  toRow: jumpRow,
                  toCol: jumpCol,
                  capturedRow: newRow,
                  capturedCol: newCol,
                  isCapture: true
                });
              }
            }
          }
        }
      }
    }

    // If captures are available, only return captures (forced capture rule)
    return captures.length > 0 ? captures : moves;
  }

  getAllValidMoves() {
    const playerColor = this.getCurrentPlayerColor();
    const allMoves = [];
    const allCaptures = [];

    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const piece = this.board.getPiece(row, col);
        if (piece === 0) continue;

        const isCorrectColor = (playerColor === 'black' && this.board.isBlackPiece(piece)) ||
                              (playerColor === 'white' && this.board.isWhitePiece(piece));

        if (isCorrectColor) {
          const moves = this.getValidMoves(row, col);
          for (const move of moves) {
            if (move.isCapture) {
              allCaptures.push(move);
            } else {
              allMoves.push(move);
            }
          }
        }
      }
    }

    // Return captures if available, otherwise regular moves
    return allCaptures.length > 0 ? allCaptures : allMoves;
  }

  makeMove(fromRow, fromCol, toRow, toCol) {
    if (this.gameOver) {
      return { success: false, error: 'Game is over' };
    }

    const piece = this.board.getPiece(fromRow, fromCol);
    if (piece === 0) {
      return { success: false, error: 'No piece at source position' };
    }

    const validMoves = this.getValidMoves(fromRow, fromCol);
    const move = validMoves.find(m => m.toRow === toRow && m.toCol === toCol);

    if (!move) {
      return { success: false, error: 'Invalid move' };
    }

    // Make the move
    this.board.setPiece(toRow, toCol, piece);
    this.board.setPiece(fromRow, fromCol, 0);

    // Handle capture
    if (move.isCapture) {
      this.board.setPiece(move.capturedRow, move.capturedCol, 0);
    }

    // Promote to king if reached opposite end
    const promoted = this.board.promoteToKing(toRow, toCol);

    // Record move
    this.moveHistory.push({
      from: { row: fromRow, col: fromCol },
      to: { row: toRow, col: toCol },
      piece,
      captured: move.isCapture,
      promoted
    });

    // Check for multi-jump
    let hasMoreCaptures = false;
    if (move.isCapture && !promoted) {
      const nextCaptures = this.getValidMoves(toRow, toCol).filter(m => m.isCapture);
      hasMoreCaptures = nextCaptures.length > 0;
    }

    // Switch player if no more captures available
    if (!hasMoreCaptures) {
      this.currentPlayer = this.currentPlayer === this.player1Id ? this.player2Id : this.player1Id;
    }

    // Check win condition
    this.checkWinCondition();

    return {
      success: true,
      hasMoreCaptures,
      promoted,
      gameOver: this.gameOver,
      winner: this.winner
    };
  }

  checkWinCondition() {
    // Count pieces
    let blackPieces = 0;
    let whitePieces = 0;

    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const piece = this.board.getPiece(row, col);
        if (this.board.isBlackPiece(piece)) blackPieces++;
        if (this.board.isWhitePiece(piece)) whitePieces++;
      }
    }

    // Check if a player has no pieces
    if (blackPieces === 0) {
      this.gameOver = true;
      this.winner = this.player2Id;
      return;
    }
    if (whitePieces === 0) {
      this.gameOver = true;
      this.winner = this.player1Id;
      return;
    }

    // Check if current player has no valid moves (stalemate)
    const validMoves = this.getAllValidMoves();
    if (validMoves.length === 0) {
      this.gameOver = true;
      this.winner = this.currentPlayer === this.player1Id ? this.player2Id : this.player1Id;
    }
  }

  startGame() {
    if (!this.gameStarted) {
      this.gameStarted = true;
      this.betsLocked = true;
    }
  }

  getState() {
    return {
      id: this.id,
      player1Id: this.player1Id,
      player2Id: this.player2Id,
      board: this.board.toJSON(),
      currentPlayer: this.currentPlayer,
      winner: this.winner,
      betAmount: this.betAmount,
      betsLocked: this.betsLocked,
      gameStarted: this.gameStarted,
      gameOver: this.gameOver,
      moveCount: this.moveHistory.length
    };
  }

  toJSON() {
    return {
      id: this.id,
      player1Id: this.player1Id,
      player2Id: this.player2Id,
      board: this.board.toJSON(),
      currentPlayer: this.currentPlayer,
      winner: this.winner,
      betAmount: this.betAmount,
      betsLocked: this.betsLocked,
      gameStarted: this.gameStarted,
      gameOver: this.gameOver,
      moveHistory: this.moveHistory
    };
  }

  static fromJSON(data) {
    const game = new DraughtsGame(data.player1Id, data.player2Id, data.betAmount);
    game.id = data.id;
    game.board.fromJSON(data.board);
    game.currentPlayer = data.currentPlayer;
    game.winner = data.winner;
    game.betsLocked = data.betsLocked;
    game.gameStarted = data.gameStarted;
    game.gameOver = data.gameOver;
    game.moveHistory = data.moveHistory || [];
    return game;
  }
}

module.exports = DraughtsGame;
