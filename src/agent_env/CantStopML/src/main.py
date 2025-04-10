import random
import time
import numpy as np
import copy


class CantStopGame:
    def __init__(self, logs: bool = True):
        self.logs = logs

        self.COL_LEN = {2: 3, 3: 5, 4: 7, 5: 9, 6: 11, 7: 13, 8: 11, 9: 9, 10: 7, 11: 5, 12: 3}
        self.state_size = 28
        self.action_size = 4

        self.current_player = 0
        self.blocked_columns = [0, 0]
        self.active_columns = set()
        self.last_dice_roll = []
        self.is_over = False

        self.reward = 0
        self.action = 0
        self.board = {column: {"length": length, "progress": [0, 0], "blocked": False} \
                      for column, length in self.COL_LEN.items()}
        self.actions = self.possible_actions()


        self.reset()



    def reset(self):

        self.current_player = 0
        self.blocked_columns = [0, 0]
        self.last_dice_roll = []
        self.is_over = False
        self.reward = 0
        self.action = 0


        self.active_columns = set()

        self.board = {column: {"length": length, "progress": [0, 0], "blocked": False} \
                      for column, length in self.COL_LEN.items()}



    def state_vector(self) -> np.array:
        state_board = np.array([self.board[col]["progress"] for col in self.board])

        # print("current_player", self.current_player)

        self.actions = self.possible_actions()


        actions_for_state = copy.deepcopy(self.actions)



        if len(actions_for_state) < 3:
            actions_for_state.extend([(0, 0)] * (3 - len(actions_for_state)))

        # print("current_player", self.current_player)
        #
        # print("state_board", state_board)
        # print('type state_board', type(state_board))
        # print("self.actions", self.actions)
        # print('type self.actions', type(self.actions))

        state_all = np.concatenate((state_board, actions_for_state)).flatten()

        return state_all

    def observe(self):

        # Extract progress values
        progress_values = [self.board[col]['progress'] for col in self.board]

        # Convert into numpy arrays and split in two sub arrays
        progress_arrays = np.array(progress_values).T  # Transpose to split values
        return progress_arrays

    def show_board_status(self):

        board_status_parts = []
        for col in self.board:
            col_status = f"Column {col}: {self.board[col]['progress'][self.current_player]}/{self.board[col]['length']} {'(Blocked)' if self.board[col]['blocked'] else ''}"
            board_status_parts.append(col_status)
        board_status = ', '.join(board_status_parts)
        if self.logs: print(f"Player {self.current_player + 1} Board Status: [{board_status}]")

    def possible_actions(self):

        self.last_dice_roll = self.roll_dice()
        if self.logs: print("Dices rolled:", self.last_dice_roll)
        combinations = self.get_combinations(self.last_dice_roll)

        valid_combinations = []
        for comb in combinations:
            if not self.board[comb[0]]['blocked'] and not self.board[comb[1]]['blocked']:
                valid_combinations.append(comb)

            # elif not self.board[comb[0]]['blocked'] and self.board[comb[1]]['blocked']:
            #     valid_combinations.append((comb[0],0))
            #
            # elif self.board[comb[0]]['blocked'] and not self.board[comb[1]]['blocked']:
            #     valid_combinations.append((comb[1],0))

        if not valid_combinations:

            if self.current_player == 0:
                if self.logs: print("No valid combinations. Player 2 take leads.")
                self.current_player = 1
                self.active_columns = set()
                self.player_random()

                letsste = 0
                while not valid_combinations:

                    self.last_dice_roll = self.roll_dice()
                    if self.logs: print("Dices rolled:", self.last_dice_roll)
                    combinations = self.get_combinations(self.last_dice_roll)

                    valid_combinations = []
                    for comb in combinations:
                        if not self.board[comb[0]]['blocked'] and not self.board[comb[1]]['blocked']:
                            valid_combinations.append(comb)

                        # elif not self.board[comb[0]]['blocked'] and self.board[comb[1]]['blocked']:
                        #     valid_combinations.append((comb[0],0))
                        #
                        # elif self.board[comb[0]]['blocked'] and not self.board[comb[1]]['blocked']:
                        #     valid_combinations.append((comb[1],0))

                return valid_combinations

            else:
                if self.logs: print("No valid combinations. Player 1 take leads.")
                self.current_player = 0
                self.active_columns = set()
                letsste = 0
                while not valid_combinations:

                    self.last_dice_roll = self.roll_dice()
                    if self.logs: print("Dices rolled:", self.last_dice_roll)
                    combinations = self.get_combinations(self.last_dice_roll)

                    valid_combinations = []
                    for comb in combinations:
                        if not self.board[comb[0]]['blocked'] and not self.board[comb[1]]['blocked']:
                            valid_combinations.append(comb)

                        # elif not self.board[comb[0]]['blocked'] and self.board[comb[1]]['blocked']:
                        #     valid_combinations.append((comb[0], 0))
                        #
                        # elif self.board[comb[0]]['blocked'] and not self.board[comb[1]]['blocked']:
                        #     valid_combinations.append((comb[1], 0))

                return valid_combinations



        if self.logs: print("Valid combinations:", valid_combinations)
        return valid_combinations

    def roll_dice(self):

        return [random.randint(1, 6) for _ in range(4)]

    def get_combinations(self, dice_roll):

        return [
            (dice_roll[0] + dice_roll[1], dice_roll[2] + dice_roll[3]),
            (dice_roll[0] + dice_roll[2], dice_roll[1] + dice_roll[3]),
            (dice_roll[0] + dice_roll[3], dice_roll[1] + dice_roll[2])
        ]

    def step(self, action):

        self.reward = 0

        columns_to_advance = action
        if self.logs: print("Selected columns:", columns_to_advance)

        for column in columns_to_advance:
            if len(self.active_columns) < 3 or column in self.active_columns:
                if self.board[column]["progress"][self.current_player] < self.board[column]["length"] and not \
                self.board[column]["blocked"]:
                    self.board[column]["progress"][self.current_player] += 1  # Advance
                    self.active_columns.add(column)
            else:
                if self.logs: print(f"Cannot advance in column {column} as already 3 columns are active.")
                continue

        for col in self.board:
            if self.board[col]["progress"][self.current_player] >= self.board[col]["length"] and not self.board[col]["blocked"]:
                self.board[col]["blocked"] = True
                self.blocked_columns[self.current_player] += 1
                if self.logs: print(f"Player {self.current_player + 1} has blocked column {col}.")
                # self.reward += 1

        if self.blocked_columns[self.current_player] >= 3:
            self.is_over = True

            if self.current_player == 0:
                if self.logs: print(f"Win. Player {self.current_player + 1} is the winner")
                self.reward += 2
            else:

                if self.logs: print(f"Loose. Player {self.current_player + 1} is the winner")
                self.reward = -2


        self.show_board_status()



    def is_game_over(self) -> bool:
        return self.is_over

    def available_actions_ids(self) -> list:



        return range(len(self.actions) + 1)

    def available_actions_mask(self) -> np.array:
        aa = np.zeros(4)
        a=self.actions
        for i in range(len(a)):
            aa[i] = 1
        return aa

    def act_with_action_id(self, action_id: int):

        if action_id == len(self.actions) :

            if self.current_player == 0:
                if self.logs: print("No valid combinations. Player 2 take leads.")
                self.current_player = 1
                self.active_columns = set()
                self.player_random()
                return

            else:
                if self.logs: print("No valid combinations. Player 1 take leads.")
                self.current_player = 0
                self.active_columns = set()
                return


        possible_actions = self.actions[action_id]

        action_id = possible_actions

        if action_id[1] == 0:
            action_id = (action_id[0],)

        self.step(action_id)

    def player_random(self):

        action_id = random.choice(self.available_actions_ids())
        self.act_with_action_id(action_id)

    def score(self) -> float:

        return self.reward

