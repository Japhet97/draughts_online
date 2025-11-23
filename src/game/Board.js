class Board {
  constructor() {
    this.board = this.initializeBoard();
  }

  initializeBoard() {
    // 8x8 board, only dark squares are used in draughts
    // 0 = empty, 1 = black piece, 2 = black king, 3 = white piece, 4 = white king
    const board = Array(8).fill(null).map(() => Array(8).fill(0));
    
    // Place black pieces (rows 0-2)
    for (let row = 0; row < 3; row++) {
      for (let col = 0; col < 8; col++) {
        if ((row + col) % 2 === 1) {
          board[row][col] = 1; // Black piece
        }
      }
    }
    
    // Place white pieces (rows 5-7)
    for (let row = 5; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        if ((row + col) % 2 === 1) {
          board[row][col] = 3; // White piece
        }
      }
    }
    
    return board;
  }

  getPiece(row, col) {
    if (row < 0 || row >= 8 || col < 0 || col >= 8) return null;
    return this.board[row][col];
  }

  setPiece(row, col, piece) {
    if (row >= 0 && row < 8 && col >= 0 && col < 8) {
      this.board[row][col] = piece;
    }
  }

  isValidPosition(row, col) {
    return row >= 0 && row < 8 && col >= 0 && col < 8;
  }

  isBlackPiece(piece) {
    return piece === 1 || piece === 2;
  }

  isWhitePiece(piece) {
    return piece === 3 || piece === 4;
  }

  isKing(piece) {
    return piece === 2 || piece === 4;
  }

  promoteToKing(row, col) {
    const piece = this.getPiece(row, col);
    if (piece === 1 && row === 7) {
      this.setPiece(row, col, 2); // Promote black to king
      return true;
    } else if (piece === 3 && row === 0) {
      this.setPiece(row, col, 4); // Promote white to king
      return true;
    }
    return false;
  }

  clone() {
    const newBoard = new Board();
    newBoard.board = this.board.map(row => [...row]);
    return newBoard;
  }

  toJSON() {
    return this.board;
  }

  fromJSON(boardData) {
    this.board = boardData.map(row => [...row]);
  }
}

module.exports = Board;
