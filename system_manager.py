from states_generator import SystemGenerator


class SystemManager():
    def __init__(self):
        self.generator = SystemGenerator()
        self.system = self.generator.system
        self.list_of_bugs = self.generator.list_of_bugs
        self.actual_state = list(self.system.keys())[0]
        self.actual_actions = self.system[self.actual_state]['actions']
        self.previous_state = None

    def list_all_actions_of_state(self, state):
        print(f"Possible actions of state {state}: {self.system[state]['actions']}")
        return self.system[state]['actions'].keys()

    def list_all_possible_actions_in_current_state(self):
        return list(self.system[self.actual_state]['actions'].keys())

    def list_all_states(self):
        return list(self.system.keys())

    def list_all_states_and_their_actions(self):
        print("All states listed: ", self.system.keys())

    def action(self, action):

        if action not in self.actual_actions.keys():
            print("You can not perform the action in this state.")
        else:
            if action in self.list_of_bugs:
                # print("The action contains a bug.")
                return 1
            elif self.actual_actions[action] in self.list_of_bugs:
                # print("The state contains a bug.")
                return 2
            else:
                self.previous_state = self.actual_state
                self.actual_state = self.actual_actions[action]
                self.actual_actions = self.system[self.actual_state]['actions']
                return 0

    def status(self):
        print(f'ACTUAL STATE: {self.actual_state}\nPREVIOUS STATE: {self.previous_state}')

    def force(self, state):
        if state in self.list_of_bugs:
            print("The state contains a bug.")
            return 2
        else:
            self.previous_state = None
            self.actual_state = state
            self.actual_actions = self.system[self.actual_state]['actions']
            return 0


