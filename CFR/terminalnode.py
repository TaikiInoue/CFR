from variables import CARDS_DEALINGS
from variables import JQ, JK, QJ, QK, KJ, KQ
from variables import CHANCE, P1, P2, TERMINAL
from variables import BET, CHECK, CALL, FOLD
from variables import CARDS_2_WINLOSE


class TerminalNode:

    def __init__(self,
                 parent, 
                 actions_history,
                 cards):
        self.state = TERMINAL
        self.parent = parent
        self.actions = []
        self.actions_history = actions_history
        self.cards = cards
        self.inf_set = self.get_inf_set()
        self.reaching_h_probs = {}
        self.children = {}



    def get_inf_set(self):
        inf_set = [TERMINAL] + [self.cards] + self.actions_history
        return '/'.join(inf_set)


    def get_utility(self):
        if   self.actions_history[-2:] == ['action_P1_CHECK', 'action_P2_CHECK']:
            return CARDS_2_WINLOSE[self.cards] * 1
        elif self.actions_history[-2:] == ['action_P1_BET', 'action_P2_CALL']:
            return CARDS_2_WINLOSE[self.cards] * 2
        elif self.actions_history[-3:] == ['action_P1_CHECK', 'action_P2_BET', 'action_P1_CALL']:
            return CARDS_2_WINLOSE[self.cards] * 2
        elif self.actions_history[-3:] == ['action_P1_CHECK', 'action_P2_BET', 'action_P1_FOLD']:
            return -1
        elif self.actions_history[-2:] == ['action_P1_BET', 'action_P2_FOLD']:
            return 1
        else:
            print(self.actions_history)