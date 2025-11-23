const { expect } = require('chai');
const Board = require('../src/game/Board');

describe('Board', () => {
  let board;

  beforeEach(() => {
    board = new Board();
  });

  describe('Initialization', () => {
    it('should create an 8x8 board', () => {
      expect(board.board).to.have.lengthOf(8);
      expect(board.board[0]).to.have.lengthOf(8);
    });

    it('should place black pieces in rows 0-2', () => {
      let blackPieces = 0;
      for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 8; col++) {
          if ((row + col) % 2 === 1) {
            expect(board.getPiece(row, col)).to.equal(1);
            blackPieces++;
          }
        }
      }
      expect(blackPieces).to.equal(12);
    });

    it('should place white pieces in rows 5-7', () => {
      let whitePieces = 0;
      for (let row = 5; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
          if ((row + col) % 2 === 1) {
            expect(board.getPiece(row, col)).to.equal(3);
            whitePieces++;
          }
        }
      }
      expect(whitePieces).to.equal(12);
    });

    it('should have empty squares in rows 3-4', () => {
      for (let row = 3; row < 5; row++) {
        for (let col = 0; col < 8; col++) {
          expect(board.getPiece(row, col)).to.equal(0);
        }
      }
    });
  });

  describe('Piece Operations', () => {
    it('should get and set pieces correctly', () => {
      board.setPiece(4, 4, 1);
      expect(board.getPiece(4, 4)).to.equal(1);
    });

    it('should validate position bounds', () => {
      expect(board.isValidPosition(0, 0)).to.be.true;
      expect(board.isValidPosition(7, 7)).to.be.true;
      expect(board.isValidPosition(-1, 0)).to.be.false;
      expect(board.isValidPosition(8, 0)).to.be.false;
    });

    it('should identify black pieces', () => {
      expect(board.isBlackPiece(1)).to.be.true;
      expect(board.isBlackPiece(2)).to.be.true;
      expect(board.isBlackPiece(3)).to.be.false;
    });

    it('should identify white pieces', () => {
      expect(board.isWhitePiece(3)).to.be.true;
      expect(board.isWhitePiece(4)).to.be.true;
      expect(board.isWhitePiece(1)).to.be.false;
    });

    it('should identify kings', () => {
      expect(board.isKing(2)).to.be.true;
      expect(board.isKing(4)).to.be.true;
      expect(board.isKing(1)).to.be.false;
    });
  });

  describe('King Promotion', () => {
    it('should promote black piece to king at row 7', () => {
      board.setPiece(7, 1, 1);
      const promoted = board.promoteToKing(7, 1);
      expect(promoted).to.be.true;
      expect(board.getPiece(7, 1)).to.equal(2);
    });

    it('should promote white piece to king at row 0', () => {
      board.setPiece(0, 1, 3);
      const promoted = board.promoteToKing(0, 1);
      expect(promoted).to.be.true;
      expect(board.getPiece(0, 1)).to.equal(4);
    });

    it('should not promote pieces in other rows', () => {
      board.setPiece(3, 1, 1);
      const promoted = board.promoteToKing(3, 1);
      expect(promoted).to.be.false;
      expect(board.getPiece(3, 1)).to.equal(1);
    });
  });
});
