class User {
  constructor(username, password) {
    this.id = null; // Will be set when user is created
    this.username = username;
    this.password = password; // In production, this should be hashed
    this.balance = 1000; // Starting balance
    this.gamesPlayed = 0;
    this.gamesWon = 0;
    this.totalWinnings = 0;
  }

  canPlaceBet(amount) {
    return this.balance >= amount && amount > 0;
  }

  deductBet(amount) {
    if (this.canPlaceBet(amount)) {
      this.balance -= amount;
      return true;
    }
    return false;
  }

  addWinnings(amount) {
    this.balance += amount;
    this.totalWinnings += amount;
    this.gamesWon++;
  }

  incrementGamesPlayed() {
    this.gamesPlayed++;
  }

  getStats() {
    return {
      username: this.username,
      balance: this.balance,
      gamesPlayed: this.gamesPlayed,
      gamesWon: this.gamesWon,
      totalWinnings: this.totalWinnings,
      winRate: this.gamesPlayed > 0 ? (this.gamesWon / this.gamesPlayed * 100).toFixed(2) : 0
    };
  }

  toJSON() {
    return {
      id: this.id,
      username: this.username,
      password: this.password,
      balance: this.balance,
      gamesPlayed: this.gamesPlayed,
      gamesWon: this.gamesWon,
      totalWinnings: this.totalWinnings
    };
  }

  static fromJSON(data) {
    const user = new User(data.username, data.password);
    user.id = data.id;
    user.balance = data.balance;
    user.gamesPlayed = data.gamesPlayed || 0;
    user.gamesWon = data.gamesWon || 0;
    user.totalWinnings = data.totalWinnings || 0;
    return user;
  }
}

module.exports = User;
