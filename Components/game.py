from .round import ExtraCardGameRound
from .players import playerUpdateRelations
from .deck import Card

class ExtraCardGame:

	round_logging = False
	is_over = False
	last_round = None
	ending_players = None

	def __init__(self, players, doubles, round_logging):
		self.round_logging = round_logging
		self.starting_players = players
		self.doubles = doubles
		self.rounds_played = 0

	def run_game(self):

		# First Round
		game_round = ExtraCardGameRound(self.starting_players, self.doubles, Card("single"))
		self.rounds_played = self.rounds_played + 1
		end_of_round_players = game_round.players

		# Repeat Until A Winner is Found
		while game_round.result.result == "continue":
			leftover_card = game_round.getLeftoverCard()

			if self.round_logging == True:
				self.printRoundResults(leftover_card, game_round, end_of_round_players)

			# Prepare Players for new round
			updated_players = playerUpdateRelations(end_of_round_players)

			game_round = ExtraCardGameRound(updated_players, self.doubles, leftover_card)
			self.rounds_played = self.rounds_played + 1
			end_of_round_players = game_round.players

		if self.round_logging == True:
			self.printRoundResults(game_round.getLeftoverCard(), game_round, end_of_round_players)	

		self.ending_players = end_of_round_players
		self.last_round = game_round
		self.is_over = True

	def getGameStatsForCSV(self):
		return str(self.last_round.result.result) + "," + str(self.last_round.result.note) + "," + str(self.rounds_played) + "," + str(len(self.ending_players))

		# Function that prints results of each line to the command line
	def printRoundResults(self, leftover_card, game_round, players):
		print(str(game_round))
		print("Players Left: " + str(players))
		print("Leftover Card: " + str(leftover_card.card_type))
		print()