from DataSetGenerator import *
from Network import Network
import numpy as np

path = "/home/loginn/Kent/LSTM/replays/used"

"""
seq = [[1, 2, 3, 4], [1, 2], [1, 2, 3]]
x = (np.ones((3, 4)) * 0).astype("int")

print("X 1 :\n", x)

for idx, s in enumerate(seq):
    trunc = s[:4]
    print(trunc)
    x[idx, :len(trunc)] = trunc

print("X 2 :\n", x)
"""

data_set_generator = DataSetGenerator(path)
network = Network()

data_set_generator.load_replays()
data_set_generator.gen_data_set()
data_set_generator.normalize_data_set()

input_data = data_set_generator.raw_data
target_output = data_set_generator.target_output

network.setup_data(input_data, target_output)
network.setup_model(data_set_generator.max_len)
network.train_network()
