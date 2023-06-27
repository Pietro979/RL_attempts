import pdb

import random


params = {
    'tree_depth': 3,
    'max_number_of_subpages': 2,
    'number_of_main_pages': 1,
    'number_of_bugs_in_states': 2,
    'number_of_bugs_in_actions': 3
}

def create_list_of_tree_elements(tree_depth, max_number_of_subpages, number_of_main_pages, state):
    list1 = []
    if tree_depth == 0:
        return []
    else:
        if not state[-1].isnumeric():
            number_of_subpages = number_of_main_pages
        else:
            # number_of_subpages = randint(1, max_number_of_subpages)
            number_of_subpages = max_number_of_subpages
        for i in range(number_of_subpages):
            substate = state + str(i)
            list1 = list1 + [substate] + create_list_of_tree_elements(state=substate, tree_depth=tree_depth - 1,
                                                                      max_number_of_subpages=max_number_of_subpages,
                                                                      number_of_main_pages=number_of_main_pages)
        return list1

class SystemGenerator:
    def __init__(self, tree_depth=params['tree_depth'],
                 max_number_of_subpages=params['max_number_of_subpages'],
                 number_of_main_pages=params['number_of_main_pages'],
                 number_of_bugs_in_states=params['number_of_bugs_in_states'],
                 number_of_bugs_in_actions=params['number_of_bugs_in_actions']):

        self.tree_depth = tree_depth
        self.max_number_of_subpages = max_number_of_subpages
        self.number_of_main_pages = number_of_main_pages
        self.number_of_bugs_in_states = number_of_bugs_in_states
        self.number_of_bugs_in_actions = number_of_bugs_in_actions

        self.main_actions = {'XToS'+ str(i): 'S'+str(i) for i in range(number_of_main_pages)}
        self.states_dict = {}
        self.list_of_states = []

        self.create_list_of_states()
        self.system = self.generate_system()
        bug_creator = BugCreator(system=self.system)
        self.list_of_bugs = bug_creator.create_bugs_randomly(number_of_bugs_in_states=2, number_of_bugs_in_actions=3)
        self.create_file_with_scheme_code(self.list_of_bugs)

    def create_list_of_states(self):
        self.list_of_states = create_list_of_tree_elements(self.tree_depth,
                                                           self.max_number_of_subpages,
                                                           self.number_of_main_pages, state = 'S')

    def generate_system(self):
        states_dict = {}
        for state in self.list_of_states:
            states_dict[state] = {}
            states_dict[state]['actions'] = {}
            random_substates = [state1 for state1 in self.list_of_states if ((state1 is not state) and (state1[:-1] != state) and (len(state1)!=2) and len(state)!=2)]
            random_substates = random.sample(random_substates, int(len(random_substates)/3))
            for state2 in self.list_of_states:
                if (state is not state2 and (len(state2)-1 <= self.tree_depth) and state2[:-1] == state) or \
                        (state is not state2 and len(state2) == 2) or \
                        (state2 in random_substates):
                    key = state+"To"+state2
                    states_dict[state]['actions'][key] = state2
        self.states_dict = states_dict
        return states_dict

    def create_file_with_scheme_code(self, list_of_bugs):
        """
        USE https://www.nomnoml.com/
        :return:
        """
        with open('system_structure.txt', 'w') as sys_struct:
            sys_struct.write("#.box: dashed\n")
            for key, value in self.states_dict.items():
                actions = value['actions']
                for key1, value1 in actions.items():
                    if (key1 in list_of_bugs) and (value1 in list_of_bugs):
                        sys_struct.write(f"[{key}]-->[<box>{value1}]\n")
                    elif value1 in list_of_bugs:
                        sys_struct.write(f"[{key}]->[<box>{value1}]\n")
                    elif key1 in list_of_bugs:
                        sys_struct.write(f"[{key}]-->[{value1}]\n")
                    elif (key1 not in tuple(list_of_bugs)) and (value1 not in tuple(list_of_bugs)):
                        sys_struct.write(f"[{key}]->[{value1}]\n")

        # with open('system_structure.txt', 'w') as sys_struct:


class BugCreator:
    def __init__(self, system):
        self.list_of_bugs = []
        self.system = system

    def create_bugs_randomly(self, number_of_bugs_in_states, number_of_bugs_in_actions):
        list_of_states = self.system.keys()
        list_of_states_with_bugs = random.sample(list_of_states, number_of_bugs_in_states)
        list_of_actions_with_bugs = random.sample(
            [key for value in self.system.values() for key in value['actions'].keys()],
            number_of_bugs_in_actions)
        self.list_of_bugs = list_of_states_with_bugs + list_of_actions_with_bugs
        print(self.list_of_bugs)
        return self.list_of_bugs

    def print_all_bugs(self):
        print(f"Bugs: {self.list_of_bugs}")




