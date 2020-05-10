import numpy as np
import utils as U
from variables import CARDS_DEALINGS
from variables import JQ, JK, QJ, QK, KJ, KQ
from variables import CHANCE, P1, P2, TERMINAL
from variables import BET, CHECK, CALL, FOLD
from variables import CARDS_2_WINLOSE


class CFRMinimization:

    def __init__(self, chance_node):

        self.chance_node = chance_node
        self.sigma = U.init_sigma(chance_node)
        self.cumulative_cfr = U.init_cumulative_vector(chance_node)
        self.update_reaching_h_probs(self.chance_node)


    def update_reaching_h_probs(self, node, probs={P1: 1, P2: 1}):
        node.reaching_h_probs = probs
        for action in node.actions:
            child_probs = probs.copy()
            if node.state in [P1, P2]:
                child_probs[node.state] *= self.sigma[node.inf_set][action]
            child_node = node.children[action]
            self.update_reaching_h_probs(child_node, child_probs)


    def compute_cfr_recursive(self, node):
        inf_set = node.inf_set
        state = node.state

        if state == CHANCE:
            child_node = node.distribute_cards()
            return self.compute_cfr_recursive(child_node)
        elif state == TERMINAL:
            return node.get_utility()
        
        if state == P1:
            cfr_h_prob = node.reaching_h_probs[P2]
        elif state == P2:
            cfr_h_prob = node.reaching_h_probs[P1]

        # compute utility for a current node and actions
        utility_for_node = 0
        utilities_for_action = {}
        for action in node.actions:
            utility_for_action = self.compute_cfr_recursive(node.play(action))
            utilities_for_action[action] = utility_for_action

            action_prob = self.sigma[inf_set][action]
            utility_for_node += action_prob * utility_for_action

        # compute counterfactual regret
        for action in node.actions:
            utility_for_action = utilities_for_action[action]
            cfr = cfr_h_prob * utility_for_action
            self.cumulative_cfr[inf_set][action] += cfr
        
        return utility_for_node


    def update_sigma(self):
        
        for inf_set in self.cumulative_cfr.keys():
            
            if inf_set.split('/')[0] == TERMINAL:
                continue

            sum_cfr = self.cumulative_cfr[inf_set].values()
            sum_cfr = sum(filter(lambda x: x > 0, sum_cfr))
            actions = self.cumulative_cfr[inf_set].keys()
            if sum_cfr > 0:
                for action in actions:
                    cfr = self.cumulative_cfr[inf_set][action]
                    cfr = max(cfr, 0)
                    self.sigma[inf_set][action] = cfr / sum_cfr
            else:
                for action in actions:
                    self.sigma[inf_set][action] = 1 / len(actions)


    def run(self, iterations):

        for _ in range(iterations):
            self.compute_cfr_recursive(self.chance_node)
            self.update_sigma()
