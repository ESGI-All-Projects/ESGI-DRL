import numpy as np

from src.agent_env.SingleAgentEnv import SingleAgentDeepEnv




class TicTacToeEnv(SingleAgentDeepEnv):
    def __init__(self, play_first=True):
        self.state_size = 18
        self.action_size = 9
        self.states = np.zeros(9)
        self.play_first = play_first
        self.reset()

    def state_vector(self) -> np.array:
        state_vector = [[0, 0] if s == 0 else [1, 0] if s == 1 else [0, 1] for s in self.states]
        return np.array(state_vector).flatten()
        # return self.states.copy()

    def is_game_over(self) -> bool:
        for i in range(0, 9, 3):
            if self.states[i] == self.states[i+1] == self.states[i+2] != 0:
                return True
        for i in range(3):
            if self.states[i] == self.states[i+3] == self.states[i+6] != 0:
                return True
        if self.states[0] == self.states[4] == self.states[8] != 0:
            return True
        if self.states[2] == self.states[4] == self.states[6] != 0:
            return True
        if not any(x == 0 for x in self.states):
            return True
        return False

    def act_with_action_id(self, action_id: int):

        assert not self.is_game_over(), "Attempted to act in a finished game."
        if action_id not in self.available_actions_ids():
            # Properly format the error message
            available_actions = self.available_actions_ids()
            error_message = f'Action ID {action_id} is not in the available actions: {available_actions}'
            raise ValueError(error_message)

        self.states[action_id] = 1 if self.play_first else 2
        # Proceed with the opponent's random policy if the game is not over
        if not self.is_game_over():
            opponent_action = np.random.choice(self.available_actions_ids())
            self.states[opponent_action] = 2 if self.play_first else 1
    def score(self) -> float:
        for i in range(0, 9, 3):
            if self.states[i] == self.states[i + 1] == self.states[i + 2] != 0:
                return 1 if ((self.states[i] == 1 and self.play_first) or \
                             (self.states[i] == 2 and not self.play_first)) else -1
        for i in range(3):
            if self.states[i] == self.states[i + 3] == self.states[i + 6] != 0:
                return 1 if ((self.states[i] == 1 and self.play_first) or \
                             (self.states[i] == 2 and not self.play_first)) else -1
        if self.states[0] == self.states[4] == self.states[8] != 0:
            return 1 if ((self.states[0] == 1 and self.play_first) or \
                         (self.states[0] == 2 and not self.play_first)) else -1
        if self.states[2] == self.states[4] == self.states[6] != 0:
            return 1 if ((self.states[2] == 1 and self.play_first) or \
                         (self.states[2] == 2 and not self.play_first)) else -1
        return 0

    def available_actions_ids(self) -> list:
        if not self.is_game_over():
            return np.where(self.states == 0)[0]
        return []

    def available_actions_mask(self) -> np.array:
        aa = np.zeros(9)
        if not self.is_game_over():
            for i, value in enumerate(self.states):
                if value == 0:
                    aa[i] = 1
        return aa

    def reset(self):
        self.states = np.zeros(9)
        if not self.play_first:
            self.states[np.random.choice(self.available_actions_ids())] = 1

    def reset_with_states(self, states):
        assert (len(states) == self.state_size)
        assert (all(state == 0 or state == 1 for state in states))
        states_intern = []
        for i in range(0, len(states), 2):
            if states[i] == 0 and states[i + 1] == 0:
                states_intern.append(0)
            elif states[i] == 1 and states[i + 1] == 0:
                states_intern.append(1)
            elif states[i] == 0 and states[i + 1] == 1:
                states_intern.append(2)
            else:
                raise Exception("Les 2 joueurs ont joué sur la même case")
        self.states = np.array(states_intern)

    def view(self):
        for cell in range(self.cells_count):
            print('X' if cell == self.agent_pos else '_', end='')
        print()

    # same than reset
    def reset_random(self):
        self.states = np.zeros(9)
        if not self.play_first:
            self.states[np.random.choice(self.available_actions_ids())] = 1