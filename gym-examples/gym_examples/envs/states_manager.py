

class StatesManager:
    def __init__(self, states_dict):
        self.actual_state = list(states_dict.keys())[0]
        self.previous_state = self.actual_state
