# # ekhem
import pdb

from agent import WebPageTesterEnv
from system_manager import SystemManager
#
# # generator.create_list_of_states()
# # system = generator.generate_system()
# #
# # bugCreator = BugCreator(system=system)
# # list_of_bugs = bugCreator.create_bugs_randomly(number_of_bugs_in_states=2, number_of_bugs_in_actions=3)
# # bugCreator.print_all_bugs()
# #
# # generator.create_file_with_scheme_code(list_of_bugs)
#
#
# # sm = SystemManager(ideal_system=system, list_of_bugs=list_of_bugs)
env = WebPageTesterEnv()
#
# env.reset()
# actual_state = env.sm.actual_state
#
# with open('system_logging.txt', 'w') as file:
#     for i in range(100):
#         action = env.sample()
#         file.write(f"Actual state: {actual_state}, Action to be performed: {action} \n")
#         actual_state, rew = env.step(action)
#         file.write(f"Reward: {rew}\n")
#
#
# print(f"Bugs which were discovered: {env.discovered_bugs}")
env.reset()
print(env._get_obs())
for i in range(100):
    action = env.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    print(observation)
    print(info)

print(env.discovered_bugs)