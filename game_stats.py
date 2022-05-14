class GameStats:

    def __init__(self, ai_game):
        """Initialize Statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Active state
        self.game_active = False
        self.high_score = 0
        self.level = 1
    
    def reset_stats(self):
        """Initialize Statistics so that they can change during the game"""
        self.lives = self.settings.stats_max_lives
        self.score = 0