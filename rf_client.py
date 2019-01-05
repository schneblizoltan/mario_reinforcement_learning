from environment import environment as env
from agents import q_agent, deep_q_agent, sarsa_agent
from analyser.analyser import analyser

import numpy as np

env = env.Environment()
env.set_game_mode("maximum")                                 # Set the game speed
env.set_frame_divisor(2)                                     # Set how many frames should be skipped
observation_space = env.reset()
dist_file_name = "dist_15k_sarsa_test.txt"
reward_file_name = "reward_15k_sarsa_test.txt"

# agent = q_agent.QAgent(observation_space, env.state_n, env.action_n, dist_file_name, reward_file_name)
# agent.learn(env)

# agent = deep_q_agent.DeepQAgent(observation_space, env.state_n, env.action_n, dist_file_name, reward_file_name)
# agent.learn(env)

agent2 = sarsa_agent.SarsaAgent(observation_space, env.state_n, env.action_n, dist_file_name, reward_file_name)
agent2.learn(env)

analyse = analyser.Analyser()
r_param = analyse.pearson_r(dist_file_name, reward_file_name)
print("Pearson r coeff. parameter: {}".format(r_param))

win_rate = analyse.win_percentage(dist_file_name)
print("Win rate: {}".format(win_rate))
