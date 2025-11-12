"""
Credit for this heuristic goes to dennis-ho's project at https://github.com/dennis-ho/blackjack-simulator


Blackjack Heuristic Strategy Isolated (Pulled Directly from Simulator)
-----------------------------------
Implements rule-based heuristics for blackjack decisions:
- Basic strategy tables (hard, soft, split)
- Insurance rules
- Hi-Lo card counting
These are static heuristics, not adaptive learning algorithms.

Possible Actions:

Compress tables:
The tables have identical rows for some values. Represent them as ranges.

Multi-Objective Strategy:
Add risk tolerance to balance between aggressive and conservative plays.
Requires weights for different objectives.

"""


H = 'H'  # Hit
S = 'S'  # Stand
Dh = 'DH'  # Double Down if allowed, otherwise Hit
Ds = 'DS'  # Double Down if allowed, otherwise Stand
P = 'P'  # Split
Ph = 'PH'  # Split if allowed, otherwise Hit
Rh = 'RH'  # Surrender if allowed, otherwise Hit
Rs = 'RS'  # Surrender if allowed, otherwise Stand
Rp = 'RP'  # Surrender if allowed, otherwise Split

split_strategy = [
    #2   3   4   5   6   7   8   9   10  A
    [Ph, Ph, P,  P,  P,  P,  H,  H,  H,  H],   # 2/2
    [Ph, Ph, P,  P,  P,  P,  H,  H,  H,  H],   # 3/3
    [H,  H,  H,  Ph, Ph, H,  H,  H,  H,  H],   # 4/4
    [Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, H,  H],   # 5/5
    [Ph, P,  P,  P,  P,  H,  H,  H,  H,  H],   # 6/6
    [P,  P,  P,  P,  P,  P,  H,  H,  H,  H],   # 7/7
    [P,  P,  P,  P,  P,  P,  P,  P,  P,  Rp],  # 8/8
    [P,  P,  P,  P,  P,  S,  P,  P,  S,  S],   # 9/9
    [S,  S,  S,  S,  S,  S,  S,  S,  S,  S],   # 10/10
    [P,  P,  P,  P,  P,  P,  P,  P,  P,  P],   # A/A
]

soft_strategy = [
    #2   3   4   5   6   7   8   9   10  A
    [H,  H,  H,  Dh, Dh, H,  H,  H,  H,  H],  # 13
    [H,  H,  H,  Dh, Dh, H,  H,  H,  H,  H],  # 14
    [H,  H,  Dh, Dh, Dh, H,  H,  H,  H,  H],  # 15
    [H,  H,  Dh, Dh, Dh, H,  H,  H,  H,  H],  # 16
    [H,  Dh, Dh, Dh, Dh, H,  H,  H,  H,  H],  # 17
    [Ds, Ds, Ds, Ds, Ds, S,  S,  H,  H,  H],  # 18
    [S,  S,  S,  S,  Ds, S,  S,  S,  S,  S],  # 19
    [S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 20
    [S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 21
]

hard_strategy = [
    #2   3   4   5   6   7   8   9   10  A
    [H,  H,  H,  H,  H,  H,  H,  H,  H,  H],   # 4
    [H,  H,  H,  H,  H,  H,  H,  H,  H,  H],   # 5
    [H,  H,  H,  H,  H,  H,  H,  H,  H,  H],   # 6
    [H,  H,  H,  H,  H,  H,  H,  H,  H,  H],   # 7
    [H,  H,  H,  H,  H,  H,  H,  H,  H,  H],   # 8
    [H,  Dh, Dh, Dh, Dh, H,  H,  H,  H,  H],   # 9
    [Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, H,  H],   # 10
    [Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh],  # 11
    [H,  H,  S,  S,  S,  H,  H,  H,  H,  H],   # 12
    [S,  S,  S,  S,  S,  H,  H,  H,  H,  H],   # 13
    [S,  S,  S,  S,  S,  H,  H,  H,  H,  H],   # 14
    [S,  S,  S,  S,  S,  H,  H,  H,  Rh, Rh],  # 15
    [S,  S,  S,  S,  S,  H,  H,  Rh, Rh, Rh],  # 16
    [S,  S,  S,  S,  S,  S,  S,  S,  S,  Rs],  # 17
    [S,  S,  S,  S,  S,  S,  S,  S,  S,  S],   # 18
    [S,  S,  S,  S,  S,  S,  S,  S,  S,  S],   # 19
    [S,  S,  S,  S,  S,  S,  S,  S,  S,  S],   # 20
    [S,  S,  S,  S,  S,  S,  S,  S,  S,  S],   # 21
]


def insurance_strategy_counting(table):
    return 'I' if table.true_count() >= 2.3 else 'N'


def insurance_strategy_never(table):
    return 'N'


def insurance_strategy_even_money(table):
    return 'I' if table.curr().is_blackjack() == 21 else 'N'


def basic_strategy(table, available_actions):
    if 'I' in available_actions:
        action = insurance_strategy_never(table)
    elif 'P' in available_actions:
        action = split_strategy[table.curr().cards[0] - 2][table.dealer_hand.cards[0] - 2]
    elif table.curr().is_soft():
        action = soft_strategy[table.curr().value() - 13][table.dealer_hand.cards[0] - 2]
    else:
        action = hard_strategy[table.curr().value() - 4][table.dealer_hand.cards[0] - 2]
    return action[0] if action[0] in available_actions else action[1]


def count_hi_lo(cards):
    count_val = sum([1 if card in [2, 3, 4, 5, 6] else -1 if card in [10, 11] else 0 for card in cards])
    return count_val