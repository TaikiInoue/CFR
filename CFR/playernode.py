from terminalnode import TerminalNode
from variables import CARDS_DEALINGS
from variables import JQ, JK, QJ, QK, KJ, KQ
from variables import CHANCE, P1, P2, TERMINAL
from variables import BET, CHECK, CALL, FOLD
from variables import CARDS_2_WINLOSE


class PlayerNode:

    def __init__(self,
                 state,
                 parent, 
                 actions,
                 actions_history,
                 cards):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.actions_history = actions_history
        self.cards = cards
        self.inf_set = self.get_inf_set()
        self.reaching_h_probs = {}

        # build complete tree of kuhn poker via DFS
        self.children = {}
        for action in self.actions:
            next_state = self.get_next_state(action)
            next_actions = self.get_next_actions(action)
            if next_state == TERMINAL:
                self.children[action] = TerminalNode(parent=self,
                                                     actions_history=actions_history + [f'action_{state}_{action}'],
                                                     cards=cards)
            else:
                self.children[action] = PlayerNode(state=next_state,
                                                   parent=self,
                                                   actions=next_actions,
                                                   actions_history=actions_history + [f'action_{state}_{action}'],
                                                   cards=cards)


    def get_next_state(self, action):
        if   self.state == P1 and action in [BET, CHECK]:
            return P2
        elif self.state == P2 and action == BET:
            return P1
        else:
            return TERMINAL


    def get_next_actions(self, action):
        if   self.state == P1 and action == CHECK:
            return [BET, CHECK]
        elif action == BET:
            return [CALL, FOLD]
        else:
            return []


    def get_inf_set(self):
        if   self.state == P1:
            public_card = self.cards[0]
        elif self.state == P2:
            public_card = self.cards[1]    

        inf_set = [f'player_{self.state}'] + [f'card_{public_card}'] + self.actions_history
        return '/'.join(inf_set)


    def play(self, action):
        return self.children[action]