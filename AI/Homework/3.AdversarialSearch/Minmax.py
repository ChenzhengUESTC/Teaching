# 请加入注释...
class State:

    # 请加入注释...
    def __init__(self, name, type,  father_state=None, possibility=1.0, is_terminal=False, utility=0):
        self.name = name
        self.father_state = father_state
        if self.father_state is not None:
            self.father_state.get_successors().append(self)
            self.father_state.transition[self] = possibility
        self.is_terminal = is_terminal
        self.type = type
        self.utility = utility

        self.successors = list()
        self.transition = dict()

    # 请加入注释...
    def is_MAX(self):
        if self.type == "MAX":
            return True
        return False

    # 请加入注释...
    def is_EXP(self):
        if self.type == "EXP":
            return True
        return False

    # 请加入注释...
    def is_MIN(self):
        if self.type == "MIN":
            return True
        return False

    # 请加入注释...
    def get_value(self):
        if self.is_terminal:
            return self.get_utility()
        elif self.is_MAX():
            return max_value(self)
        elif self.is_MIN():
            return min_value(self)
        elif self.is_EXP():
            return exp_value(self)

    # 请加入注释...
    def get_utility(self):
        return self.utility

    # 请加入注释...
    def get_successors(self):
        return self.successors

    # 请加入注释...
    def get_probability(self, successor):
        return self.transition[successor]


    # 请加入注释...
def max_value(state):
    v = float('-inf')
    for successor in state.get_successors():
        v = max(v, successor.get_value())
    return v


    # 请加入注释...
def min_value(state):
    v = float('inf')
    for successor in state.get_successors():
        v = min(v, successor.get_value())
    return v


    # 请加入注释...
def exp_value(state):
    v = 0
    for successor in state.get_successors():
        p = state.get_probability(successor)
        v += p * successor.get_value()
    return v


if __name__ == '__main__':

    # 请加入注释...
    state_D = State(name='D', type='MAX')

    state_A = State(name='A', type='MIN', father_state=state_D)
    state_B = State(name='B', type='MIN', father_state=state_D)
    state_C = State(name='C', type='MIN', father_state=state_D)

    state_6 = State(name='6', type='', father_state=state_A,
                    is_terminal=True, utility=6)
    state_9 = State(name='9', type='', father_state=state_A,
                    is_terminal=True, utility=9)
    state_5 = State(name='5', type='', father_state=state_A,
                    is_terminal=True, utility=5)

    state_3 = State(name='3', type='', father_state=state_B,
                    is_terminal=True, utility=3)
    state_4 = State(name='4', type='', father_state=state_B,
                    is_terminal=True, utility=4)
    state_8 = State(name='8', type='', father_state=state_B,
                    is_terminal=True, utility=8)

    state_1 = State(name='1', type='', father_state=state_C,
                    is_terminal=True, utility=1)
    state_7 = State(name='7', type='', father_state=state_C,
                    is_terminal=True, utility=7)
    state_2 = State(name='2', type='', father_state=state_C,
                    is_terminal=True, utility=2)

    # 请加入注释...
    print(state_D.get_value())

    # 请加入注释...
    state_G = State(name='G', type='MAX')

    state_E = State(name='E', type='MIN', father_state=state_G)
    state_F = State(name='F', type='MIN', father_state=state_G)

    state_A = State(name='A', type='EXP', father_state=state_E)
    state_B = State(name='B', type='EXP', father_state=state_E)
    state_C = State(name='C', type='EXP', father_state=state_F)
    state_D = State(name='D', type='EXP', father_state=state_F)

    state_15 = State(name='15', type='', father_state=state_A,
                     possibility=1/3, is_terminal=True, utility=15)
    state_9 = State(name='9', type='', father_state=state_A,
                    possibility=1/3, is_terminal=True, utility=9)
    state_33 = State(name='33', type='', father_state=state_A,
                     possibility=1/3, is_terminal=True, utility=33)

    state_24 = State(name='24', type='', father_state=state_B,
                     possibility=1/3, is_terminal=True, utility=24)
    state_3 = State(name='3', type='', father_state=state_B,
                    possibility=1/3, is_terminal=True, utility=3)
    state_30 = State(name='30', type='', father_state=state_B,
                     possibility=1/3, is_terminal=True, utility=30)

    state_18 = State(name='18', type='', father_state=state_C,
                     possibility=1/3, is_terminal=True, utility=18)
    state_6 = State(name='6', type='', father_state=state_C,
                    possibility=1/3, is_terminal=True, utility=6)
    state_27 = State(name='27', type='', father_state=state_C,
                     possibility=1/3, is_terminal=True, utility=27)

    state_21 = State(name='21', type='', father_state=state_D,
                     possibility=1/3, is_terminal=True, utility=21)
    state_12 = State(name='12', type='', father_state=state_D,
                     possibility=1/3, is_terminal=True, utility=12)
    state_01 = State(name='0', type='', father_state=state_D,
                     possibility=1/3, is_terminal=True, utility=0)

    # 请加入注释...
    print(state_G.get_value())
