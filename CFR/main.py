from chancenode import ChanceNode
from algorithm import CFRMinimization
from variables import CARDS_DEALINGS
from variables import JQ, JK, QJ, QK, KJ, KQ
from variables import CHANCE, P1, P2, TERMINAL
from variables import BET, CHECK, CALL, FOLD


chance_node = ChanceNode(actions=CARDS_DEALINGS)

cfr = CFRMinimization(chance_node)
cfr.run(iterations=10000)
for k, v in cfr.cumulative_cfr.items():
    print(k, v)