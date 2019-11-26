from Components.players import NeighborSuspicionAlwaysRandomPlayer, AlwaysRandomPlayer
from Components.game import ExtraCardGame
import random

NUMBER_OF_PLAYERS = 6
NUMBER_OF_DOUBLES_PER_ROUND = 1
TREASURE_THRESHOLD = 3
SEE_LOGS_FROM_EACH_ROUND = False

# Chance of getting caught, lower is less likely
BASE_SUSPICION_THRESHOLD = 0.5

# Increases the suspicion of a player when they have more doubles than those next to them (Multiplies with Base)
INCREASED_SUSPICION_RATE = 1.5

# Decreased the suspicion of a player when they have less doubles than those next to them (Multiplies with Base)
DECREASED_SUSPICION_RATE = 0.5

# players = [AlwaysRandomPlayer(3, i+1, 0.5) for i in range(NUMBER_OF_PLAYERS)]

SIMULATIONS = 10000
duelWins = 0
duelTies = 0
scoreWins = 0
rounds = 0

# Counts of different types of players winning
# neighborCount = 0
# nonCount = 0

for i in range(SIMULATIONS):
	
	print("Simulation Number " + str(i))
	print("")

	# Create new players each game
	players = [NeighborSuspicionAlwaysRandomPlayer(TREASURE_THRESHOLD, i+1, BASE_SUSPICION_THRESHOLD, INCREASED_SUSPICION_RATE, DECREASED_SUSPICION_RATE) for i in range(NUMBER_OF_PLAYERS)]

	# Combined players of different types instead
	# players = [NeighborSuspicionAlwaysRandomPlayer(TREASURE_THRESHOLD, i+1, BASE_SUSPICION_THRESHOLD, INCREASED_SUSPICION_RATE, DECREASED_SUSPICION_RATE) for i in range(3)] + [AlwaysRandomPlayer(TREASURE_THRESHOLD, j+4, BASE_SUSPICION_THRESHOLD) for j in range(3)]

	random.shuffle(players)

	new_game = ExtraCardGame(players, NUMBER_OF_DOUBLES_PER_ROUND, SEE_LOGS_FROM_EACH_ROUND)
	new_game.run_game()
	print("")
	print("outcome, number score winners or duel score, rounds played, players left at end")
	print(new_game.getGameStatsForCSV())
	print("")
	if new_game.last_round.result.result == "duelWin":
		duelWins = duelWins + 1
	elif new_game.last_round.result.result == "duelTie":
		duelTies = duelTies + 1
	elif new_game.last_round.result.result == "scoreWin":
		scoreWins = scoreWins + 1
	else:
		raise Exception("Weird Result: " + str(new_game.result.result))
	rounds = rounds + new_game.rounds_played

	# Code for seeing what types of players win
	# for x in new_game.ending_players:
	# 	if x.is_winner == True:
	# 		if type(x).__name__ == "NeighborSuspicionAlwaysRandomPlayer":
	# 			neighborCount = neighborCount + 1
	# 		elif type(x).__name__ == "AlwaysRandomPlayer":
	# 			nonCount = nonCount + 1

print("Duel Wins: " + str(duelWins/SIMULATIONS))
print("Duel Ties: " + str(duelTies/SIMULATIONS))
print("Score Wins: " + str(scoreWins/SIMULATIONS))
print("Average Rounds: " + str(rounds/SIMULATIONS))

# Player Type Stats
# print("Neighbor Wins: " + str(neighborCount/SIMULATIONS))
# print("Non Neighbor Wins: " + str(nonCount/SIMULATIONS))