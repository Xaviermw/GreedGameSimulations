import random
from .deck import *

# Base Player
class Player:

	# Who is sitting next to the player
	left_player = None
	right_player = None

	# Card Chosen for the Round
	card_chosen = None

	# Is the player eliminated
	eliminated = False

	# Has the player won
	is_winner = False

	def __init__(self, win_threshold, player_num):

		# Set Score to 0 and other player traits
		self.score = 0
		self.win_threshold = win_threshold
		self.player_num = player_num

	# Add to score, and check if player meets victory threshold
	def tallyScore(self, value):
		self.score = self.score + value
		if self.score == self.win_threshold:
			self.is_winner = True
		elif self.score > self.win_threshold:
			raise Exception("Unexpected Error, player score over win threshold")

	# Basic Player Info
	def __repr__(self):
		return "Player " + str(self.player_num) + " Score: " + str(self.score)

# A player that always randomly selects a card
class AlwaysRandomPlayer(Player):

	# Initialize Player and starting suspicion level
	def __init__(self, win_threshold, player_num, base_suspicion_level):
		self.base_suspicion_level = base_suspicion_level
		self.suspicion_level = self.base_suspicion_level
		super().__init__(win_threshold, player_num)

	# Picks a random card from the deck by checking how many doubles left (note this is somewhat redundant if deck is shuffled)
	def pickCard(self, deck):
		if random.random() > deck.countOfTypeRemaining("double")/deck.cards_remaining:
			self.card_chosen = deck.selectCardTypeIfPossible("single")
		else:
			self.card_chosen = deck.selectCardTypeIfPossible("double")
			self.tallyScore(1)
		self.card_chosen.is_chosen = True
		if self.card_chosen == None:
			raise Exception("Unexpected Error, player did not choose a card")

	def suspicionUpdate(self):
		pass

	def __repr__(self):
		return "AlwaysRandom" + str(super().__repr__())

class NeighborSuspicionAlwaysRandomPlayer(AlwaysRandomPlayer):

	def __init__(self, win_threshold, player_num, suspicion_level, higher_rate, lower_rate):
		self.higher_rate = higher_rate
		self.lower_rate = lower_rate
		super().__init__(win_threshold, player_num, suspicion_level)

	def suspicionUpdate(self):
		if self.score > max(self.right_player.score, self.left_player.score):
			self.suspicion_level = self.base_suspicion_level*self.higher_rate
		elif self.score < min(self.right_player.score, self.left_player.score):
			self.suspicion_level = self.base_suspicion_level*self.lower_rate
		else:
			self.suspicion_level = self.base_suspicion_level
		return self

	def __repr__(self):
		return "NeighborSuspicion" + str(super().__repr__())

# Update after each round
def playerUpdateRelations(players):
	neighbor_players = create_neighbors_from_array_spot(players)
	shifted_players = shift_right(neighbor_players)
	suspicion_updated_players = updateSuspicions(shifted_players)
	return suspicion_updated_players

# Adds left and right neighbors to each person
def create_neighbors_from_array_spot(players):
	amount_players = len(players)
	for x in range(amount_players):
		players[x].right_player = players[(x+1)%amount_players]
		players[x].left_player = players[(x+(amount_players-1))%amount_players]
	return players

def updateSuspicions(players):
	for player in players:
		player.suspicionUpdate()
	return players

# Changes who draws first (while keeping order)
def shift_right(lst):
	return [lst[-1]] + lst[:-1]

def shift_left(lst):
	return lst[1:] + [lst[0]]