import pdb
import random
import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces
from system_manager import SystemManager

LIST_OF_ALREADY_PERFORMED_ACTIONS = []
IS_REUSED = None

def calculate_conditions_for_truncation():
    pass
def calculate_conditions_for_termination():
    pass

def reward(action_result):
    sum1 = 0
    global IS_REUSED
    if action_result == 1:
        sum1 += 10
    if action_result == 2:
        sum1 += 10
    if action_result == 0:
        sum1 += 0
    if IS_REUSED is True:
        sum1 += -1
        IS_REUSED = None
    else:
        sum1 += 1
        IS_REUSED = None
    return sum1

def action(list_of_actions):
    global IS_REUSED
    for act in list_of_actions:
        if act not in LIST_OF_ALREADY_PERFORMED_ACTIONS:
            LIST_OF_ALREADY_PERFORMED_ACTIONS.append(act)
            IS_REUSED = False
            return act
    IS_REUSED = True
    act = random.choice(list_of_actions)
    return act


class WebPageTesterEnv(gym.Env):
    def __init__(self):
        self.sm = SystemManager()
        self._agent_location = self.sm.actual_state
        self._action_space = self.sm.list_all_possible_actions_in_current_state()
        self.discovered_bugs = []

    def sample(self):
        actions = self._action_space
        action_to_perform = action(actions)
        return action_to_perform

    # Returns next step, reward, ...
    def _get_obs(self):
        self._agent_location = self.sm.actual_state
        self._action_space = self.sm.list_all_possible_actions_in_current_state()
        return {"Actual state": self._agent_location}

    def _get_info(self):
        self._agent_location = self.sm.actual_state
        self._action_space = self.sm.list_all_possible_actions_in_current_state()
        return {"Actual state": self._agent_location,
                "Previous state": self.sm.previous_state,
                "Actions to perform": self._action_space}

    def reset(self, seed=None, options = None):
        super().reset(seed=seed)

        for state in self.sm.list_all_states():
            if state not in self.sm.list_of_bugs:
                self.sm.force(state)

        self._agent_location = self.sm.actual_state
        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action_to_perform=None):
        result = self.sm.action(action_to_perform)
        if result == 1 and (action_to_perform not in self.discovered_bugs):
            self.discovered_bugs.append(action_to_perform)
        elif result == 2 and (self.sm.actual_actions[action_to_perform] not in self.discovered_bugs):
            self.discovered_bugs.append(self.sm.actual_actions[action_to_perform])
        rew = reward(result)
        print(f"Action to be performed {action_to_perform}")
        observation = self._get_obs()
        info = self._get_info()
        terminated = True if len(self.sm.list_of_bugs) == len(self.discovered_bugs) else False

        return observation, rew, terminated, False, info
