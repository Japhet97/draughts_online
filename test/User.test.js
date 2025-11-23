const { expect } = require('chai');
const User = require('../src/models/User');

describe('User', () => {
  let user;

  beforeEach(() => {
    user = new User('testuser', 'password123');
  });

  describe('Initialization', () => {
    it('should create user with username and password', () => {
      expect(user.username).to.equal('testuser');
      expect(user.password).to.equal('password123');
    });

    it('should start with 1000 balance', () => {
      expect(user.balance).to.equal(1000);
    });

    it('should start with zero games played and won', () => {
      expect(user.gamesPlayed).to.equal(0);
      expect(user.gamesWon).to.equal(0);
      expect(user.totalWinnings).to.equal(0);
    });
  });

  describe('Betting', () => {
    it('should allow placing bet with sufficient balance', () => {
      expect(user.canPlaceBet(100)).to.be.true;
    });

    it('should not allow placing bet exceeding balance', () => {
      expect(user.canPlaceBet(1500)).to.be.false;
    });

    it('should not allow negative or zero bets', () => {
      expect(user.canPlaceBet(0)).to.be.false;
      expect(user.canPlaceBet(-100)).to.be.false;
    });

    it('should deduct bet from balance', () => {
      const success = user.deductBet(200);
      expect(success).to.be.true;
      expect(user.balance).to.equal(800);
    });

    it('should not deduct if bet exceeds balance', () => {
      const success = user.deductBet(1500);
      expect(success).to.be.false;
      expect(user.balance).to.equal(1000);
    });
  });

  describe('Winnings', () => {
    it('should add winnings to balance', () => {
      user.addWinnings(500);
      expect(user.balance).to.equal(1500);
    });

    it('should track total winnings', () => {
      user.addWinnings(100);
      user.addWinnings(200);
      expect(user.totalWinnings).to.equal(300);
    });

    it('should increment games won', () => {
      expect(user.gamesWon).to.equal(0);
      user.addWinnings(100);
      expect(user.gamesWon).to.equal(1);
    });
  });

  describe('Statistics', () => {
    it('should track games played', () => {
      user.incrementGamesPlayed();
      user.incrementGamesPlayed();
      expect(user.gamesPlayed).to.equal(2);
    });

    it('should calculate win rate correctly', () => {
      user.incrementGamesPlayed();
      user.incrementGamesPlayed();
      user.incrementGamesPlayed();
      user.addWinnings(100); // 1 win
      
      const stats = user.getStats();
      expect(stats.winRate).to.equal('33.33');
    });

    it('should return 0 win rate with no games played', () => {
      const stats = user.getStats();
      expect(stats.winRate).to.equal(0);
    });

    it('should return complete stats', () => {
      user.incrementGamesPlayed();
      user.addWinnings(500);
      
      const stats = user.getStats();
      expect(stats).to.have.property('username');
      expect(stats).to.have.property('balance');
      expect(stats).to.have.property('gamesPlayed');
      expect(stats).to.have.property('gamesWon');
      expect(stats).to.have.property('totalWinnings');
      expect(stats).to.have.property('winRate');
    });
  });
});
