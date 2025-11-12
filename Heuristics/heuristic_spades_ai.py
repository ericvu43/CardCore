# Sourced from spades (https://github.com/ReillyBova/spades)
# Spades Heuristic

import random
import getpass
from card import Card
from contract import Contract
from spades_utils import *


class HeuristicAI:
    NAME = "HeuristicAI"

    def __init__(self):
        self.name = HeuristicAI.NAME

    # hand: list of cards AI has
    # lead_suite: suite of first card in current trick(none if AI is first)
    # spades_broken: if spades has been brken or not
    # selectable: list of valid cards 
    def select_card(self, hand, lead_suite=None, spades_broken=False):
        selectable = []
        for card in hand:
            if (lead_suite == -1 and spades_broken):
                selectable.append(card) # Everything is good for first card when a spade has been played
            elif (lead_suite == -1 and card.suiteID != 3):
                selectable.append(card) # Everything is good for first card but spades before a spade has been played
            elif (lead_suite == card.suiteID):
                selectable.append(card) # Otherwise, try to match the lead suite



        if not selectable:
            selectable = hand

        # plays lowest ranked card
        lowest_card = selectable[0]
        for card in selectable:
            if card.rank.value < lowest_card.rank.value:
                lowest_card = card

        return lowest_card
            
