from random import sample
from itertools import chain
from numpy import mean
from sys import argv

from ambirhythms.Trials import Trials
from ambirhythms.Block import Block


def pseudo_randomise_trials(ioi_list, participant_id):
    rhythms = {'ambiguous': {57: (4, 6, 0), 62: (4, 5, 6), 90: (3, 5, 4), 229: (2, 3, 4), 259: (4, 7, 6),
                             120: (0, 1, 2), 121: (0, 1, 2), 133: (0, 1, 2), 187: (0, 1, 2), 349: (0, 1, 2),
                             35: (2, 0, 6), 76: (3, 1, 7), 96: (2, 0, 1), 148: (8, 6, 0), 196: (8, 6, 0)},

               'unambiguous': {135: (0, 3, 5), 131: (0, 2, 1), 175: (0, 1, 4), 300: (5, 3, 8), 200: (4, 6, 7),
                               232: (1, 3, 0), 165: (2, 0, 6), 82: (3, 5, 0), 192: (4, 1, 3), 347: (0, 2, 3),
                               11: (0, 2, 4), 140: (4, 2, 5), 24: (1, 2, 3), 75: (3, 4, 7), 136: (1, 0, 3)}
               }

    n = len(rhythms['ambiguous'].keys())
    idx_pool = sample(range(n), n)

    split_point = -int(n / 3)
    blocked_idx = idx_pool[:split_point]  # first 2/3 of pool
    randomised_idx = idx_pool[split_point:]  # last 1/3 of pool

    blocked_trials, randomised_trials = [[None] for _ in range(2)]
    for idx in [blocked_idx, randomised_idx]:
        rhy = [[list(rhythms[key].items())[i] for i in idx] for key in rhythms.keys()]
        if idx == blocked_idx:
            blocked_trials = [Trials(rhythms=[r[0] for r in rhy[i]],
                                     rotations=[r[1] for r in rhy[i]],
                                     iois=ioi_list) for i in range(len(rhythms.keys()))]
        else:
            rhy = [*chain(*rhy)]
            randomised_trials = Trials(rhythms=[r[0] for r in rhy],
                                       rotations=[r[1] for r in rhy],
                                       iois=ioi_list)
            trials = randomised_trials.trials
            consecutive = 0
            for last_trial, trial in zip(trials[:-1], trials[1:]):
                # If current and last rhythms were from different lists, reset consecutive
                if (trial[0] in rhythms['ambiguous'].keys()) ^ (last_trial[0] in rhythms['ambiguous'].keys()):
                    consecutive = 0
                else:
                    consecutive += 1

                if consecutive == 2:
                    randomised_trials.shuffle_trials()

    blocks = [*blocked_trials, randomised_trials]
    return [Block(i, j, blocks[j]) for i, j in enumerate(block_order(participant_id))]


def block_order(i):
    orders = {
        0: (0, 1, 2),
        1: (2, 0, 1),
        2: (1, 0, 2),
        3: (2, 1, 0)
    }
    return orders[i % 4]


def estimate_duration(block, ioi_list):
    metre = 12
    cycles = 6
    milliseconds_per_min = 6e4

    estimated_duration = len(block) * metre * cycles * mean(ioi_list) / milliseconds_per_min
    print('Estimated duration: {0:.1f} minutes \n'
          'Based on 3 x {1:.1f} minute blocks of {2} trials at {3} cycles/trial'.format(
            estimated_duration * 3,
            estimated_duration,
            len(block),
            cycles))
    return None


def main(participant_id):
    ioi_list = (124, 153, 188, 232)
    # ioi_list = (10, 20, 30, 40)
    blocks = pseudo_randomise_trials(ioi_list, participant_id)
    estimate_duration(blocks[0], ioi_list)
    return blocks


if __name__ == '__main__':
    if any(argv[1:]):
        main(argv[1])
    else:
        main(0)
