from player import Player
import numpy as np

a = Player()
b = Player()
episodes = 10000
for episode in range(episodes):
    a_action = a.action()
    b_action = b.action()
    a.learn(a_action)
    b.learn(b_action)


print(a.cumlative_p / episodes)
print(b.cumlative_p / episodes)