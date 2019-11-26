from Components.round import ExtraCardGameRound
from Components.players import AlwaysRandomPlayer, playerUpdateRelations
from Components.deck import Card

# Function that prints results of each line to the command line
def printRoundResults(leftover_card, game_round, players):
	print(str(game_round))
	print("Players Left: " + str(players))
	print("Leftover Card: " + str(leftover_card))
	print()

NUMBER_OF_PLAYERS = 6

# Create Players
# Win Threshold, PlayerID, Default Threshold Level
players = [AlwaysRandomPlayer(3, i+1, 0.5) for i in range(NUMBER_OF_PLAYERS)]

# First Round
game_round = ExtraCardGameRound(players, Card("single"))
end_of_round_players = game_round.players

# Repeat Until A Winner is Found
while game_round.result.result == "continue":

	leftover_card = game_round.getLeftoverCard()

	printRoundResults(leftover_card, game_round, end_of_round_players)

	end_of_round_players = playerUpdateRelations(end_of_round_players)

	game_round = ExtraCardGameRound(end_of_round_players, leftover_card)

	end_of_round_players = game_round.players


leftover_card = game_round.getLeftoverCard()
printRoundResults(leftover_card, game_round, end_of_round_players)