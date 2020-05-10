import random

from playernode import PlayerNode
from variables import CARDS_DEALINGS
from variables import JQ, JK, QJ, QK, KJ, KQ
from variables import CHANCE, P1, P2, TERMINAL
from variables import BET, CHECK, CALL, FOLD
from variables import CARDS_2_WINLOSE


class ChanceNode:

    def __init__(self, actions):
        self.state = CHANCE
        self.parent = None
        self.actions = actions
        self.actions_history = []
        self.cards = None
        self.inf_set = 'CHANCE'
        self.reaching_h_probs = {}

        # build complete tree of kuhn poker via DFS
        self.children = {}
        for action in self.actions:
            self.children[action] = PlayerNode(state=P1,
                                               parent=self,
                                               actions=[BET, CHECK],
                                               actions_history=[],
                                               cards=action)


    def distribute_cards(self):
        cards = random.choice(self.actions)
        return self.children[cards]