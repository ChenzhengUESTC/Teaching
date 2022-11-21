# import random


class Sample:
    def __init__(self, A, B, Y=None):
        self.A = A
        self.B = B
        self.Y = Y

    def get_feature_vector(self):
        return [self.A, self.B]

    def get_label(self):
        return self.Y


def initialize_train_set():
    train_set = list()
    train_set.append(Sample(A=1, B=1, Y='Negative'))
    train_set.append(Sample(A=3, B=2, Y='Positive'))
    train_set.append(Sample(A=2, B=4, Y='Positive'))
    train_set.append(Sample(A=3, B=4, Y='Positive'))
    train_set.append(Sample(A=2, B=3, Y='Negative'))

    return train_set


class Perceptron:
    def __init__(self):
        self.w = [0, 0]

    def predict(self, sample_vector):
        temp = 0
        for i in range(len(self.w)):
            temp += self.w[i] * sample_vector[i]
        if temp > 0:
            return 'Positive'
        return 'Negative'

    def modify_weight_vector(self, sample_vector, true_label):
        if true_label == 'Positive':
            for i in range(len(self.w)):
                self.w[i] += sample_vector[i]
        if true_label == 'Negative':
            for i in range(len(self.w)):
                self.w[i] -= sample_vector[i]

    def learn(self, train_set):
        # has_error = True
        # while has_error:
        # has_error = False
        # random.shuffle(train_set)
        for sample in train_set:
            predicted_label = self.predict(sample.get_feature_vector())
            if predicted_label != sample.get_label():
                # has_error = True
                self.modify_weight_vector(sample.get_feature_vector(), sample.get_label())


if __name__ == '__main__':
    train_set = initialize_train_set()
    perceptron = Perceptron()
    perceptron.learn(train_set)
    print("The perceptron's weight vector:", perceptron.w)

    for sample in train_set:
        predicted_label = perceptron.predict(sample.get_feature_vector())
        print("sample:", sample.get_feature_vector(), "predicted label:", predicted_label, "true label:",
              sample.get_label())
