class  SpadesMoves:

    def __init__(self):
        self.state_history = []

        self.state = {
            "hands": [[],[],[],[]],
            "trick": [],
            "spades_broken": False,
            "tricks_won": [0,0,0,0],
            "turn": 0
        }

#get valid moves
    def getAllValidMoves(self, hand, lead_suite=-1, spades_broken=False):
        selectable = []
        for card in hand:
            if (lead_suite == -1 and spades_broken):
                selectable.append(card) 
            elif (lead_suite == -1 and card.suiteID != 3):
                selectable.append(card) 
            elif (lead_suite == card.suiteID):
                selectable.append(card) 



        if not selectable:
            selectable = hand

        return selectable


#apply move
    def makeMove(self, player, card):
        #save move
        self.state_history.append({
            "player": player,
            "card": card,
            "hands": [list(h) for h in self.state["hands"]],
            "trick": list(self.state["trick"]),
            "spades_broken": self.state["spades_broken"],
            "tricks_won": list(self.state["tricks_won"]),
            "turn": self.state["turn"]
        })

        #remove card from hand and add trick
        self.state["hands"][player].remove(card)
        self.state["trick"].append((player, card))

        #spades broken?
        if card.suiteID == 3:
            self.state["spades_broken"] = True

        if len(self.state["trick"]) == 4:

            lead_suite = self.state["trick"][0][1].suite
            trick = self.state["trick"]
            winning = None
            for s, c in trick:
                if winning is None:
                    winning = (s,c)
                else:
                    ws, wc = winning
                    if (c.suite == 3 and wc.suite != 3) or \
                        (c.suite == wc.suite and c.orderID > wc.orderID) or \
                        (c.suite == 3 and wc.suite == 3 and c.orderID > wc.orderID):
                        winning = (s,c)
            winner_seat, _ = winning

            self.state["tricks_won"][winner_seat] += 1
            self.state["trick"] = []
            self.state["turn"] = winner_seat

        else:
            self.state["turn"] = (player + 1) % 4


    def undoMove(self):
        last = self.state_history.pop()

        self.state["hands"] = [list(h) for h in last["hands"]]
        self.state["trick"] = list(last["trick"])
        self.state["spades_broken"] = last["spades_broken"]
        self.state["tricks_won"] = list(last["tricks_won"])
        self.state["turn"] = last["turn"]
