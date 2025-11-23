const { expect } = require('chai');
const DraughtsGame = require('../src/game/DraughtsGame');

describe('DraughtsGame', () => {
  let game;
  const player1Id = 'player1';
  const player2Id = 'player2';

  beforeEach(() => {
    game = new DraughtsGame(player1Id, player2Id, 100);
  });

  describe('Game Initialization', () => {
    it('should create a game with correct players', () => {
      expect(game.player1Id).to.equal(player1Id);
      expect(game.player2Id).to.equal(player2Id);
    });

    it('should set correct bet amount', () => {
      expect(game.betAmount).to.equal(100);
    });

    it('should start with player1 (black) turn', () => {
      expect(game.currentPlayer).to.equal(player1Id);
    });

    it('should not be game over initially', () => {
      expect(game.gameOver).to.be.false;
      expect(game.winner).to.be.null;
    });
  });

  describe('Move Validation', () => {
    it('should allow valid forward move for black piece', () => {
      const moves = game.getValidMoves(2, 1);
      expect(moves).to.be.an('array');
      expect(moves.length).to.be.greaterThan(0);
    });

    it('should not allow moves for empty squares', () => {
      const moves = game.getValidMoves(3, 0);
      expect(moves).to.be.an('array');
      expect(moves).to.have.lengthOf(0);
    });

    it('should only allow moves for current player pieces', () => {
      const moves = game.getValidMoves(5, 0); // White piece
      expect(moves).to.have.lengthOf(0); // Black's turn
    });
  });

  describe('Making Moves', () => {
    it('should successfully make a valid move', () => {
      const result = game.makeMove(2, 1, 3, 0);
      expect(result.success).to.be.true;
      expect(result.gameOver).to.be.false;
    });

    it('should reject invalid moves', () => {
      const result = game.makeMove(2, 1, 5, 0); // Too far
      expect(result.success).to.be.false;
      expect(result.error).to.exist;
    });

    it('should switch player after move', () => {
      expect(game.currentPlayer).to.equal(player1Id);
      game.makeMove(2, 1, 3, 0);
      expect(game.currentPlayer).to.equal(player2Id);
    });

    it('should reject moves when not player turn', () => {
      game.currentPlayer = player2Id;
      const result = game.makeMove(2, 1, 3, 0); // Black piece
      expect(result.success).to.be.false;
    });
  });

  describe('Capturing', () => {
    it('should capture opponent piece', () => {
      // Clear the board for a simple capture test
      for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
          game.board.setPiece(row, col, 0);
        }
      }
      
      // Set up a capture scenario
      game.board.setPiece(3, 2, 1); // Black piece
      game.board.setPiece(4, 3, 3); // White piece to capture
      game.currentPlayer = game.player1Id; // Black's turn
      
      const result = game.makeMove(3, 2, 5, 4);
      expect(result.success).to.be.true;
      expect(game.board.getPiece(4, 3)).to.equal(0); // Captured piece removed
      expect(game.board.getPiece(5, 4)).to.equal(1); // Black piece at new position
    });
  });

  describe('Win Conditions', () => {
    it('should detect win when opponent has no pieces', () => {
      // Remove all white pieces
      for (let row = 5; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
          game.board.setPiece(row, col, 0);
        }
      }
      
      game.checkWinCondition();
      expect(game.gameOver).to.be.true;
      expect(game.winner).to.equal(player1Id);
    });
  });

  describe('Game State', () => {
    it('should return correct game state', () => {
      const state = game.getState();
      expect(state).to.have.property('id');
      expect(state).to.have.property('player1Id');
      expect(state).to.have.property('player2Id');
      expect(state).to.have.property('board');
      expect(state).to.have.property('currentPlayer');
      expect(state).to.have.property('betAmount');
      expect(state.betAmount).to.equal(100);
    });
  });

  describe('Betting', () => {
    it('should lock bets when game starts', () => {
      expect(game.betsLocked).to.be.false;
      game.startGame();
      expect(game.betsLocked).to.be.true;
    });

    it('should mark game as started', () => {
      expect(game.gameStarted).to.be.false;
      game.startGame();
      expect(game.gameStarted).to.be.true;
    });
  });
});
