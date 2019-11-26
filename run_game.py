from Components.players import NeighborSuspicionAlwaysRandomPlayer, AlwaysRandomPlayer
from Components.game import ExtraCardGame
import random

NUMBER_OF_PLAYERS = 6
NUMBER_OF_DOUBLES_PER_ROUND = 1
TREASURE_THRESHOLD = 3
SEE_LOGS_FROM_EACH_ROUND = True

# Chance of getting caught, lower is less likely
BASE_SUSPICION_THRESHOLD = 0.5

# Increases the suspicion of a player when they have more doubles than those next to them (Multiplies with Base)
INCREASED_SUSPICION_RATE = 1.5

# Decreased the suspicion of a player when they have less doubles than those next to them (Multiplies with Base)
DECREASED_SUSPICION_RATE = 0.5

players = [NeighborSuspicionAlwaysRandomPlayer(TREASURE_THRESHOLD, i+1, BASE_SUSPICION_THRESHOLD, INCREASED_SUSPICION_RATE, DECREASED_SUSPICION_RATE) for i in range(NUMBER_OF_PLAYERS)]

random.shuffle(players)
new_game = ExtraCardGame(players, NUMBER_OF_DOUBLES_PER_ROUND, SEE_LOGS_FROM_EACH_ROUND)
new_game.run_game()
print("")
print("outcome, number score winners or duel score, rounds played, players left at end")
print(new_game.getGameStatsForCSV())
print("")