import tflearn
from tflearn.data_utils import to_categorical


class Network:
    def __init__(self):
        self.net = None

        self.trainX = None
        self.trainY = None

        self.testX = []
        self.testY = []

    def setup_data(self, input_data, target_output):
        self.trainX = input_data[:int(len(input_data) * 0.95)]
        self.trainY = target_output[:int(len(input_data) * 0.95)    ]

        self.trainY = to_categorical(self.trainY, 2)

        self.testX = input_data[int(len(input_data) * 0.95):]
        self.testY = target_output[int(len(input_data) * 0.95):]

        self.testY = to_categorical(self.testY, 2)

    def setup_model(self, seq_len):
        print("Setting TF model up...")
        self.net = tflearn.input_data([None, seq_len, 78])
        self.net = tflearn.lstm(self.net, 128, dropout=0.8)
        self.net = tflearn.fully_connected(self.net, 2, activation='softmax')
        self.net = tflearn.regression(self.net, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy')
        print("Done")

    def train_network(self):
        print("Training Network")
        model = tflearn.DNN(self.net, tensorboard_verbose=3)
        model.fit(self.trainX, self.trainY, validation_set=(self.testX, self.testY), show_metric=True)
        print("Done")
