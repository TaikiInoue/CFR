import numpy as np

class Player():
    

    def __init__(self):
        '''
        reward_vectors: 
        expected_reward:
        experts_reward:
        regrets:
        '''
        self.experts = ['rock', 'paper', 'scissors']
        self.reward_vectors = {'rock':     np.array([0, 1, -1]),  # opponent's action is rock
                               'paper':    np.array([-1, 0, 1]),  # opponent's action is paper
                               'scissors': np.array([1, -1, 0])}  # opponent's action is scissors
        self.n = len(self.experts)
        self.episode = 0
        self.expected_reward = 0
        self.experts_reward = np.zeros(self.n)
        self.regrets = np.zeros(self.n)
        self.p = np.ones(self.n) / self.n
        self.cumlative_p = 0


    def action(self):
        action = np.random.choice(self.experts, 1,  p=self.p)
        return action[0]

    def learn(self, action):
        reward_vector = self.reward_vectors[action]
        self.update_expected_reward(reward_vector)
        self.update_experts_reward(reward_vector)
        self.compute_regret()
        self.compute_p()

        self.episode += 1
        self.cumlative_p += self.p

    def update_experts_reward(self, reward_vector):
        self.experts_reward += np.dot(self.p, reward_vector)

    def update_expected_reward(self, reward_vector):
        self.expected_reward += reward_vector

    def compute_regret(self):
        self.regrets = self.experts_reward - self.expected_reward
    
    def compute_p(self):
        experts_weight = np.array([max(0, regret) for regret in self.regrets])
        if sum(experts_weight) > 0:
            self.p = experts_weight / sum(experts_weight)
        else:
            self.p = np.ones(self.n) / self.n
