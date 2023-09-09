import simpy
import statistics
import numpy as np
import pandas as pd

# Generic helper class to hold information regarding to resources
# This simplifies how we pass information from main program to entity process
class Moderator(object):
    def __init__(self, env, name, market, productivity, utilisation, handling_time, accuracy):
        self.env = env
        self.name = name
        self.market = market
        self.productivity = productivity
        self.utilisation = utilisation
        self.handling_time = handling_time
        self.accuracy = accuracy
        self.resource = simpy.Resource(env)
        self.task = 0

    def print_stats(self):
        print("\t[{}] {} moderating, {} in queue".format(self.name, self.resource.count, len(self.resource.queue)))

    def get_handling_time(self):
        return self.handling_time

    def get_queue_size(self):
        return self.resource.count + len(self.resource.queue)
    
    def get_utilisation(self):
        return self.task/self.productivity

# Generic helper class to hold information regarding to processes
class Advertisement(object):
    def __init__(self, name, market, score, profit):
        self.name = name
        self.market = market
        self.score = score
        self.profit = profit

def assignment(env, advertisements, moderators):
    abs_mismatch_list = []
    # helper class for moderation

    def dispatcher(moderators): # looting
        assigned_queue_size = -1
        assigned_moderator = None
        for moderator in moderators:
            queue_size = moderator.resource.count + len(moderator.resource.queue)
            if queue_size < assigned_queue_size or assigned_queue_size == -1:
                assigned_queue_size = queue_size
                assigned_moderator = moderator
        return assigned_moderator, assigned_queue_size


    # moderation - Entity Process
    # Describe how advertisement performs at each moderator
    def moderation(env, advertisement, moderators):
        # arrival statement
        # print("[{:6.2f}:{}] - arrive at dispatcher".format(env.now, advertisement.name))

        # Debugging statement to print state of moderators
        for moderator in moderators:
            moderator.print_stats()

        # dispatcher logic: looting
        # advertisement will choose a moderator based on the dispatcher function
        moderator, num_in_moderator = dispatcher(moderators)
        abs_mismatch_list.append(abs(moderator.accuracy - advertisement.score))
        # print("[{:6.2f}:{}] - chooses {} with {} ads in queue".format(env.now, advertisement.name, moderator.name, num_in_moderator))
        
        # process logic to handle the request for a spot at the assigned moderator
        with moderator.resource.request() as request:
            yield request
            # print('[{:6.2f}:{}] - begin moderation'.format(env.now, advertisement.name))
            handling_time = moderator.get_handling_time()
            yield env.timeout(handling_time)
            # print('[{:6.2f}:{}] - finish moderation'.format(env.now, advertisement.name))
        # print('[{:6.2f}:{}] - depart from queue'.format(env.now, name))
        moderator.task += 1

    # moderation event generator - Supporting Process
    def moderation_event_generator(env, advertisements, moderators):
        for index in range(len(advertisements)):
            adv = advertisements[index]
            mod = moderation(env, adv, moderators)
            env.process(mod)
            next_entity_arrival = 0
            yield env.timeout(next_entity_arrival)
    env.process(moderation_event_generator(env, advertisements, moderators))
    env.run()
    mismatch_score = statistics.mean(abs_mismatch_list)
    utilisation_score = statistics.mean([x.get_utilisation() for x in moderators])
    return mismatch_score, utilisation_score

def simulate(adv, mod):
    advertisements, moderators = [], []
    env = simpy.Environment()
    for index, row in adv.iterrows():
        advertisements.append(Advertisement(name=row["ad_id"],market=row["market"], score=row["score"], profit=row["ad_revenue"]))
    for index, row in mod.iterrows():
        moderators.append(Moderator(env,name=row["mod_id"],market=row["market"],productivity=row["productivity"],utilisation=row["utilisation"],handling_time=row["handling_time"],accuracy=row["accuracy"]))
    return assignment(env, advertisements, moderators)
