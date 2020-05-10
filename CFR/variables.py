CARDS_DEALINGS = ['JQ', 'JK', 'QJ', 'QK', 'KJ', 'KQ']
JQ, JK, QJ, QK, KJ, KQ = CARDS_DEALINGS

# node type
CHANCE = "CHANCE"
P1 = 'P1'
P2 = 'P2'
TERMINAL = 'TERMINAL'

BET = 'BET'
CHECK = 'CHECK'
CALL = 'CALL'
FOLD = 'FOLD'

CARDS_2_WINLOSE = {JQ: -1,
                   JK: -1,
                   QJ: 1,
                   QK: -1,
                   KJ: 1,
                   KQ: 1}