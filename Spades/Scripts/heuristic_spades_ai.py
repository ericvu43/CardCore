# Sourced from spades (https://github.com/ReillyBova/spades)
# Spades Heuristic

import random
import getpass
from card import Card


class HeuristicAI:
    NAME = "HeuristicAI"

    def __init__(self):
        self.name = HeuristicAI.NAME
        self.points = 0


    # looks at and assigns a score value for current state
    def evaluate_state(self, state, hero_seat):

        score = 0

        team = 0
        if hero_seat in (0,2):
            team = 0
        else: 
            team = 1

        tricks = state.state["tricks_won"]
        team_tricks = 0
        opp_tricks = 0

        if team == 0:
            team_tricks = tricks[0] + tricks[2]
            opp_tricks = tricks[1] + tricks[3]
        else:
            team_tricks = tricks[1] + tricks[3]
            opp_tricks = tricks[0] + tricks[2]

        score += (team_tricks - opp_tricks) * 10
        
        #extra score for better cards

        hand = state.state["hands"][hero_seat]

    
        for card in hand:
            if card.orderID == 14:
                score += 12
            elif card.orderID == 13:
                score += 8
            elif card.orderID == 12:
                score += 5
            elif card.orderID == 11:
                score += 3
            elif card.orderID == 10:
                score += 1
            
            if card.suiteID == 3:
                score += .5


        return score
        

    #Assign scores for each move

    WIN_SCORE = 100
    LOSS_SCORE = -100

    #trick won- boolean, true if AI won current trick
    # card_played, card AI just played
    
    def evaluate_move(self, trick_won):
        if trick_won:
            self.points += 10
        else:
            self.points -= 10


    def evaluate_game(self, tricks_won, bids, ai_seat):
        self.points = 0
        
        team = [0,0]
        if ai_seat == 0 or ai_seat == 2:
            team = [0,2]
        else:
            team = [1,3]

        team_tricks_won = 0
        team_bid = 0

        if team == [0,2]:
            team_tricks_won = tricks_won[0] + tricks_won[2]
            team_bid = bids[0] + bids[2]
        else:
            team_tricks_won = tricks_won[1] + tricks_won[3]
            team_bid = bids[1] + bids[3]

        if team_tricks_won >= team_bid:
            return self.WIN_SCORE + self.points
        else:
            return self.LOSS_SCORE + self.points



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
            if card.orderID < lowest_card.orderID:
                lowest_card = card

        return lowest_card
