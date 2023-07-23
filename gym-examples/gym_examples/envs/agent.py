import pdb
import random
import numpy as np
import pygame

import gymnasium as gym
from gym import spaces
from .system_manager import SystemManager

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
        self.action_space = spaces.Discrete(len(self.sm.all_actions))
        self.observation_space = spaces.Discrete(len(self.sm.list_all_states()))
        self.discovered_bugs = []
        self.obs_mapper = self.observation_mapper()
        self.act_mapper = self.action_mapper()
        self._agent_location = self.obs_mapper[self.sm.actual_state]

    def action_mapper(self):
        act_mapper = {}
        for index, value in enumerate(self.sm.all_actions):
            act_mapper[index] = value
        return act_mapper


    def observation_mapper(self):
        obs_mapper = {}
        for index, value in enumerate(self.sm.list_all_states()):
            obs_mapper[value] = index
        return obs_mapper

    def sample(self):
        all_possible_actions_in_current_state = self.sm.list_all_possible_actions_in_current_state()
        all_possible_actions_in_current_state_mapped = [key for key, value in self.act_mapper.items() if value in all_possible_actions_in_current_state]
        action_to_perform_mapped = random.choice(all_possible_actions_in_current_state_mapped)
        action_to_perform = self.act_mapper[action_to_perform_mapped]
        # action_to_perform = actions.sample()
        return action_to_perform

    # Returns next step, reward, ...
    def _get_obs(self):
        self._agent_location = self.sm.actual_state
        self.action_space = spaces.Discrete(len(self.sm.list_all_possible_actions_in_current_state()))
        return {"Actual state": self._agent_location}

    def _get_info(self):
        # self._agent_location = self.sm.actual_state
        # self.action_space = spaces.Space(self.sm.list_all_possible_actions_in_current_state())
        return {"Actual state": self._agent_location,
                "Previous state": self.sm.previous_state}

    def reset(self, seed=None, options = None):
        super().reset(seed=seed)

        for state in self.sm.list_all_states():
            if state not in self.sm.list_of_bugs:
                self.sm.force(state)

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
