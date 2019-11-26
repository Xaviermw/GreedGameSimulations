import random
from .players import AlwaysRandomPlayer
from .deck import TreasureDeck, Card

class RoundResult:

	# Basic Description of Result of Game
	def __init__(self, result, note):
		self.result = result
		self.note = note

	def __repr__(self):
		return str(self.result) + "," + str(self.note)

# One Round of Card Selection with a Card leftover for next round, Player Accusation, and Win Condition Checks 
class ExtraCardGameRound:

	# Set initial values and create the deck
	def __init__(self, players, leftover_card):
		self.result = RoundResult("continue", 0)
		self.had_elimination = False
		self.players = players
		self.guiltyPlayers = []
		self.num_players = len(self.players)
		self.deck = TreasureDeck(len(self.players)-1, 1, leftover_card)
		self.deck.shuffle()

		self.drawCards()
		self.accusePlayer()
		self.findWinner()

	# All players pick a card, player that pick a double are guilty
	def drawCards(self):
		for player in self.players:
			player.pickCard(self.deck)
			if player.card_chosen.card_type == "double":
				self.guiltyPlayers.append(player)
		if self.deck.cards_remaining != 1:
			raise Exception("Should by 1 card left at end of round")

	# Determines if a guilty player is forced to walk the plank
	def accusePlayer(self):

		# Only 1 double was taken
		if len(self.guiltyPlayers) == 1:
			guiltyPlayer = self.guiltyPlayers[0]

			# Just a suspicion level call, suspicion level changes should be handled elsewhere
			if random.random() < guiltyPlayer.suspicion_level:
				self.eliminatePlayer(guiltyPlayer)

		# 2 doubles were taken
		elif len(self.guiltyPlayers) == 2:

			# Value 0 to 1
			elimVal = random.random()
			# Probably needs a more sophisticated algorithm, max used to make sure guilty player nevel less than 1/players to be caught, should be changed later if suspicion can be lowered enough
			oneVal = max(self.guiltyPlayers[0].suspicion_level/2, 1/len(self.players))
			twoVal = oneVal + max(self.guiltyPlayers[1].suspicion_level/2, 1/len(self.players))

			# Will only eliminate one player at most
			if elimVal < oneVal:
				self.eliminatePlayer(self.guiltyPlayers[0])
			elif elimVal < twoVal:
				self.eliminatePlayer(self.guiltyPlayers[1])

	# Remove a player from the player pool
	def eliminatePlayer(self, player):
		player.eliminated = True
		self.players.remove(player)
		print(str(player) + " - Walks the Plank")


	# After elimination, sees if any player has won, or players left is 2 for a duel
	def findWinner(self):
		for player in self.players:
			if player.is_winner:
				self.result.result = "scoreWin"
				self.result.note = str(int(self.result.note) + 1)
		if self.result.result != "scoreWin" and len(self.players) == 2:
			self.duel()

	# Victory if 1 remaining player has more than another remaining player, Tie Otherwise
	def duel(self):
		p_one_score = self.players[0].score
		p_two_score = self.players[1].score

		if p_one_score > p_two_score:
			self.result = RoundResult("duelWin", str(p_one_score) + " to " + str(p_two_score))
		elif p_two_score > p_one_score:
			self.result = RoundResult("duelWin", str(p_two_score) + " to " + str(p_one_score))
		else:						
			self.result = RoundResult("duelTie", str(p_one_score))

	# Contains the last card in the deck after the round is over
	def getLeftoverCard(self):
		if self.deck.cards_remaining != 1:
			raise Exception("Not 1 card leftover")
		else:
			return self.deck.selectNextCard()

	# Prints RoundResult, and the players that took the double that round
	def __repr__(self):
		return "Round Result: [" + str(self.result) + "] Double Takers: " + str(self.guiltyPlayers)