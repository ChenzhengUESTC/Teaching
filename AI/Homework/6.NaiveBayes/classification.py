

def initialize_train_set():
    train_set = set()
    train_set.add(Sample(A=1, B=1, Y=1))
    train_set.add(Sample(A=1, B=0, Y=1))
    train_set.add(Sample(A=1, B=0, Y=0))
    train_set.add(Sample(A=1, B=1, Y=0))
    train_set.add(Sample(A=0, B=1, Y=0))
    train_set.add(Sample(A=1, B=1, Y=1))
    train_set.add(Sample(A=0, B=1, Y=1))
    train_set.add(Sample(A=1, B=0, Y=0))
    train_set.add(Sample(A=1, B=1, Y=0))
    train_set.add(Sample(A=1, B=1, Y=0))
    return train_set


def maximum_likelihood_estimation(train_set):
    P_A_Y = dict()
    for A in [0, 1]:
        for Y in [0, 1]:
            count_Y = 0
            count_A_Y = 0
            for sample in train_set:
                if sample.Y == Y:
                    count_Y += 1
                    if sample.A == A:
                        count_A_Y += 1
            P_A_Y[(A, Y)] = count_A_Y / count_Y

    print("P(A|Y):", P_A_Y)

    P_B_Y = dict()

    for B in [0, 1]:
        for Y in [0, 1]:
            count_Y = 0
            count_B_Y = 0
            for sample in train_set:
                if sample.Y == Y:
                    count_Y += 1
                    if sample.B == B:
                        count_B_Y += 1
            P_B_Y[(B, Y)] = count_B_Y / count_Y

    print("P(B|Y):", P_B_Y)

    P_Y = dict()
    for Y in [0, 1]:
        count_Y = 0
        for sample in train_set:
            if sample.Y == Y:
                count_Y += 1
        P_Y[Y] = count_Y / len(train_set)
    print("P(Y):", P_Y)

    return P_A_Y, P_B_Y, P_Y


def laplace_smoothing(train_set):
    P_A_Y = dict()
    for A in [0, 1]:
        for Y in [0, 1]:
            count_Y = 2
            count_A_Y = 1
            for sample in train_set:
                if sample.Y == Y:
                    count_Y += 1
                    if sample.A == A:
                        count_A_Y += 1
            P_A_Y[(A, Y)] = count_A_Y / count_Y

    print("P(A|Y):", P_A_Y)

    P_B_Y = dict()

    for B in [0, 1]:
        for Y in [0, 1]:
            count_Y = 2
            count_B_Y = 1
            for sample in train_set:
                if sample.Y == Y:
                    count_Y += 1
                    if sample.B == B:
                        count_B_Y += 1
            P_B_Y[(B, Y)] = count_B_Y / count_Y

    print("P(B|Y):", P_B_Y)

    P_Y = dict()
    for Y in [0, 1]:
        count_Y = 1
        for sample in train_set:
            if sample.Y == Y:
                count_Y += 1
        P_Y[Y] = count_Y / (len(train_set) + 2)
    print("P(Y):", P_Y)

    return P_A_Y, P_B_Y, P_Y


def predict(sample, P_A_Y, P_B_Y, P_Y):
    P_Y_A_B = dict()
    P_Y_A_B[0] = P_Y[0] * P_A_Y[(sample.A, 0)] * P_B_Y[(sample.A, 0)]
    P_Y_A_B[1] = P_Y[1] * P_A_Y[(sample.B, 1)] * P_B_Y[(sample.B, 1)]
    print("P(Y,A,B):", P_Y_A_B)
    if P_Y_A_B[0] > P_Y_A_B[1]:
        return 0
    else:
        return 1


class Sample:
    def __init__(self, A, B, Y=-1):
        self.A = A
        self.B = B
        self.Y = Y


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    train_set = initialize_train_set()
    P_A_Y, P_B_Y, P_Y = maximum_likelihood_estimation(train_set)
    new_sample = Sample(A=1, B=1)
    result = predict(new_sample, P_A_Y, P_B_Y, P_Y)
    print("The label of sample[", new_sample.A, ",", new_sample.B, "] is predicted to be", result,
          "by using maximum likelihood estimation.")
    print()

    P_A_Y, P_B_Y, P_Y = laplace_smoothing(train_set)
    result = predict(new_sample, P_A_Y, P_B_Y, P_Y)
    print("The label of sample[", new_sample.A, ",", new_sample.B, "] is predicted to be", result,
          "by using laplace smoothing.")
