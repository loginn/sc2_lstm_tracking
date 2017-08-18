from sc2reader import factories
from sc2reader import events
import json
import gzip


class DataSetGenerator:
    def __init__(self, path):
        self.path = path
        self.replays = []
        self.raw_data = []
        self.normalized_data = []
        self.target_output = []
        self.max_len = 0
        self.factory = factories.SC2Factory()
        self.min_values = {}
        self.max_values = {}

    def load_replays(self):
        print("Loading replays...")
        self.replays = self.factory.load_replays(self.path, load_level=4)
        print("Done")

    def load_data_from_replays(self):
        print("Loading relevant data...")

        for i, replay in enumerate(self.replays):
            print("replay #", i)
            temp_list = []
            self.raw_data.append([])
            count = 0
            for player in replay.players:
                if player.result == "Win":
                    self.target_output.append(2 - player.pid)

            for event in replay.events:
                if type(event) == events.tracker.PlayerStatsEvent:
                    if count % 2 == 0:
                        for _, value in event.stats.items():
                            temp_list.append(value)
                    else:
                        if event.pid == 2:
                            for _, value in event.stats.items():
                                temp_list.append(value)
                        else:
                            temp_list2 = []
                            for _, value in event.stats.items():
                                temp_list2.append(value)
                            temp_list2.extend(temp_list)
                            temp_list = temp_list2

                        self.raw_data[i].append(temp_list)
                        temp_list = []
                    count += 1
        print("Done")

    def normalize(self):
        self.normalized_data = self.raw_data.copy()
        for replay in self.normalized_data:
            for stats in replay:
                for idx, v in enumerate(stats):
                    if self.max_values[idx] != self.min_values[idx]:
                        normalized_value = ((v - self.min_values[idx]) / (self.max_values[idx] - self.min_values[idx]))
                        stats[idx] = normalized_value

    def find_min_max_values(self):
        for replay in self.raw_data:
            for stats in replay:
                for idx, v in enumerate(stats):
                    if v > self.max_values[idx]:
                        self.max_values[idx] = v
                    elif v < self.min_values[idx]:
                        self.min_values[idx] = v

    def normalize_data_set(self):
        print("Normalizing data...")
        self.max_values = self.raw_data[0][0].copy()
        self.min_values = self.raw_data[0][0].copy()

        self.find_min_max_values()
        self.normalize()
        print("Done")

    def pad_data(self):
        lengths = []

        for replay in self.raw_data:
            lengths.append(len(replay))
        self.max_len = max(lengths)
        print("max_len =", self.max_len)

        for replay in self.raw_data:
            if len(replay) < self.max_len:
                replay.extend([[0] * 78] * (self.max_len - len(replay)))

    def gen_data_set(self):
        self.load_data_from_replays()
        self.pad_data()

    def save_data_to_file(self):
        print("Writing data into JSON files")
        input_file = gzip.open("/home/loginn/Kent/LSTM/json/input.json.gz", 'wt')
        target_output_file = open("/home/loginn/Kent/LSTM/json/target_output.json", 'w')
        json.dump(self.normalized_data, input_file)
        json.dump(self.target_output, target_output_file)
        print("Done")
