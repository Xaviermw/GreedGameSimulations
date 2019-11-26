import random
import copy

class Deck:

	# Contents are created by child type
	def __init__(self):
		self.exhausted = False
		self.starting_size = len(self.starting_contents)
		self.current_state = copy.deepcopy(self.starting_contents) 
		self.cards_remaining = copy.deepcopy(self.starting_size)

	# Rearrange all cards (including already chosen cards)
	def shuffle(self):
		random.shuffle(self.current_state)

	# Pick the next card in the deck
	def selectNextCard(self):
		if self.exhausted == False:
			for card in self.current_state:
				if card.is_chosen == False:
					return self.selectCard(card)
		else:
			raise Exception("No Cards Remaining in Deck")

	# Find the first card of a certain type
	def selectCardTypeIfPossible(self, desired_type):
		for card in self.current_state:
			if card.is_chosen == False and card.card_type == desired_type:
				return self.selectCard(card)
		print("No " + desired_type + " cards left in deck")
		return None

	# Selects a card at a spot (spot starts at 1)
	def selectCardAt(self, spot):
		if spot > self.starting_size:
			raise Exception("Card spot more than cards in deck")
		elif self.current_state[spot-1].is_chosen == False:
			return self.selectCard(self.current_state[spot-1])
		else:
			raise Exception("Trying to Select Card that is already chosen")

	# A card is picked
	def selectCard(self, card):
		self.cards_remaining = self.cards_remaining - 1
		if self.cards_remaining == 0:
			self.exhausted = True
		return card

	# Amount of a type of card remaining and non-chosen
	def countOfTypeRemaining(self, desired_type):
		card_count = 0
		for card in self.current_state:
			if card.is_chosen == False and card.card_type == desired_type:
				card_count = card_count + 1
		return card_count

	# Amount of a type of card when deck was created (includes chosen)
	def countOfTypeStarting(self, desired_type):
		card_count = 0
		for card in self.current_state:
			if card.card_type == desired_type:
				card_count = card_count + 1
		return card_count

	# Prints each card in the deck on a new line
	def __repr__(self):
		contents = ""
		for x in range(self.starting_size):
			contents = contents + str(self.current_state[x]) + "\n"
		return contents

# Deck that contains two types, singles and doubles. A fixed amount of singles and doubles are initialized, along with any other cards
class TreasureDeck(Deck):

	# Creates starting single and double card content
	def __init__(self, singles, doubles, extra_cards):
		self.starting_contents = [Card("single") for i in range(singles)] + [Card("double") for j in range(doubles)] + [extra_cards]
		super().__init__()

# Simple Card with a type, and whether it has been chosen
class Card:

	# Always starts non-chosen
	def __init__(self, card_type):
		self.card_type = card_type
		self.is_chosen = False

	def __repr__(self):
		return self.card_type + "," + str(self.is_chosen)