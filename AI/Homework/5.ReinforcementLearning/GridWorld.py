import random


class GridWorld:

    def __init__(self, size=(8, 8), exit_diamond=(0, 0), exit_pit=(1, 1), diamond_reward=10, pit_reward=-10,
                 living_reward=-0.1, p=0.8, discount=0.95, actions=('UP', 'DOWN', 'RIGHT', 'LEFT')):
        self.size = size
        self.exit_diamond = exit_diamond
        self.exit_pit = exit_pit
        self.diamond_reward = diamond_reward
        self.pit_reward = pit_reward
        self.living_reward = living_reward
        self.p = p
        self.discount = discount
        self.actions = actions

        self.states = set()
        for i in range(size[0]):
            for j in range(size[1]):
                state = State(location=(i, j))
                if (i, j) == exit_diamond:
                    state.is_diamond = True
                    state.value = diamond_reward
                if (i, j) == exit_pit:
                    state.is_pit = True
                    state.value = pit_reward
                self.states.add(state)

    def __str__(self):
        temp_string = ""
        for i in range(size[0]):
            for j in range(size[1]):
                state = self.find_state_at_location(location=(i, j))
                temp_string += str(round(state.value, 1)).ljust(6) + "\t"
            temp_string += "\n"
        return temp_string

    def get_rand_state(self, non_terminal=True):
        state = random.sample(self.states, 1)[0]
        if non_terminal == True:
            while state.is_pit or state.is_diamond:
                state = random.sample(self.states, 1)[0]
        return state

    def get_rand_action(self):
        action = random.sample(self.actions, 1)[0]
        return action

    def find_state_at_location(self, location):
        for state in self.states:
            if state.location[0] == location[0] and state.location[1] == location[1]:
                return state

    def find_state_in_direction(self, state, direction):
        for state_in_direction in self.states:
            if direction == "DOWN":
                if (state_in_direction.location[1] == state.location[1]) and (
                        state_in_direction.location[0] == (state.location[0] + 1) if (
                                state.location[0] + 1 <= self.size[0]) else state.location[0]):
                    return state_in_direction
            if direction == "UP":
                if (state_in_direction.location[1] == state.location[1]) and (
                        state_in_direction.location[0] == (state.location[0] - 1) if (
                                state.location[0] - 1 >= 0) else state.location[0]):
                    return state_in_direction
            if direction == "LEFT":
                if (state_in_direction.location[0] == state.location[0]) and (
                        state_in_direction.location[1] == (state.location[1] - 1) if (
                                state.location[1] > 0) else state.location[1]):
                    return state_in_direction
            if direction == "RIGHT":
                if (state_in_direction.location[0] == state.location[0]) and (
                        state_in_direction.location[1] == (state.location[1] + 1) if (
                                state.location[1] + 1 <= self.size[1]) else state.location[1]):
                    return state_in_direction

    def transition(self, state, action, next_state):
        if action == 'UP' or action == 'DOWN':
            if self.find_state_in_direction(state, action) == next_state:
                return self.p
            if self.find_state_in_direction(state, 'LEFT') == next_state or self.find_state_in_direction(
                    state,
                    'RIGHT') == next_state:
                return (1 - self.p) / 2
        if action == 'LEFT' or action == 'RIGHT':
            if self.find_state_in_direction(state, action) == next_state:
                return self.p
            if self.find_state_in_direction(state, 'UP') == next_state or self.find_state_in_direction(
                    state,
                    'DOWN') == next_state:
                return (1 - self.p) / 2
        if state == next_state:
            self_p = 0
            if self.find_state_in_direction(state, action) is None:
                self_p += p
            if action == 'UP' or action == 'DOWN':
                if self.find_state_in_direction(state, 'LEFT') is None or self.find_state_in_direction(state,
                                                                                                       'RIGHT') is None:
                    self_p += (1 - self.p) / 2
            if action == 'LEFT' or action == 'RIGHT':
                if self.find_state_in_direction(state, 'UP') is None or self.find_state_in_direction(state,
                                                                                                     'DOWN') is None:
                    self_p += (1 - self.p) / 2
            return self_p
        return 0

    def move(self, state, action):
        if random.random() < p:
            direction = action
        else:
            if action == 'UP' or action == 'DOWN':
                if random.random() < 0.5:
                    direction = 'LEFT'
                else:
                    direction = 'RIGHT'
            if action == 'LEFT' or action == 'RIGHT':
                if random.random() < 0.5:
                    direction = 'UP'
                else:
                    direction = 'DOWN'

        if self.find_state_in_direction(state, direction) is not None:
            return self.find_state_in_direction(state, direction)
        else:
            return state


def policy_extraction(mdp):
    for state in mdp.states:
        if state.is_pit or state.is_diamond:
            state.best_action = 'EXIT'
        else:
            temp_max = float('-inf')
            for action in mdp.actions:
                temp = 0
                for next_state in mdp.states:
                    transition = mdp.transition(state, action, next_state)
                    if transition > 0:
                        temp += transition * (mdp.living_reward + mdp.discount * next_state.value)
                if temp > temp_max:
                    temp_max = temp
                    state.best_action = action
    temp_string = ""
    for i in range(mdp.size[0]):
        for j in range(mdp.size[1]):
            state = mdp.find_state_at_location(location=(i, j))
            temp_string += state.best_action.ljust(6) + "\t"
        temp_string += "\n"
    print(temp_string)


def Q_learning(mdp, epsilon=0.8, epsilon_decrease=0.9999, alpha=0.1, Max_episodes=5000):
    delta = float('inf')
    for iteration in range(Max_episodes):
        delta = 0

        state_intial = mdp.get_rand_state()
        state = state_intial
        while state.is_pit is not True and state.is_diamond is not True:
            if random.random() < epsilon:
                action = mdp.get_rand_action()
            else:
                action = state_intial.get_best_action()
            next_state = mdp.move(state, action)
            delta += (1 - alpha) * state.get_q_state(action).value + alpha * (
                    mdp.living_reward + mdp.discount * next_state.value) - state.get_q_state(action).value
            state.get_q_state(action).value = (1 - alpha) * state.get_q_state(action).value + alpha * (
                    mdp.living_reward + mdp.discount * next_state.value)
            state.update_value()
            state = next_state

        epsilon *= epsilon_decrease
        print('iteration:', iteration, 'delta:', delta, 'epsilon', epsilon)
        iteration += 1


class Q_state:
    def __init__(self, action, value=0):
        self.action = action
        self.value = value


class State:
    def __init__(self, location, is_diamond=False, is_pit=False, value=0, actions=('UP', 'DOWN', 'RIGHT', 'LEFT')):
        self.location = location
        self.is_diamond = is_diamond
        self.is_pit = is_pit
        self.value = value
        self.q_states = set()
        self.actions = actions
        for action in actions:
            self.q_states.add(Q_state(action))
        self.best_action = None

    def __str__(self):
        return '[' + str(self.location[0]) + ',' + str(self.location[1]) + ']'

    def get_q_state(self, action):
        for q_state in self.q_states:
            if q_state.action == action:
                return q_state

    def update_value(self):
        for q_state in self.q_states:
            if q_state.value > self.value:
                self.value = q_state.value
                self.best_action = q_state.action

    def get_best_action(self):
        if self.best_action is None:
            return random.sample(self.actions, 1)[0]
        return self.best_action


if __name__ == '__main__':
    random.seed(10)

    size = (8, 8)
    exit_diamond = (random.randint(0, size[0] - 1), random.randint(0, size[1] - 1))
    exit_pit = (random.randint(0, size[0] - 1), random.randint(0, size[1] - 1))
    while exit_pit == exit_diamond:
        exit_pit = (random.randint(0, size[0] - 1), random.randint(0, size[1] - 1))
    p = 0.75 + random.random() / 4
    living_reward = -random.random() / 10
    discount = 1 - random.random() / 10
    grid_world = GridWorld(size=size, exit_diamond=exit_diamond, exit_pit=exit_pit, p=p, living_reward=living_reward,
                           discount=discount)

    print('size =', size, 'p =', p, 'living_reward =', living_reward, 'discount =', discount)

    print()
    print('Grid world initialized:')
    print(grid_world)

    Q_learning(grid_world)

    print()
    print()
    print()
    print('Grid world finished:')
    print(grid_world)
    print()
    print()
    print('Best policy is extracted as:')
    policy_extraction(grid_world)
