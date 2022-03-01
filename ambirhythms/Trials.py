from random import choice, sample
from itertools import permutations


class Trials:
    def __init__(self, rhythms, rotations, iois):
        self.trials = []
        self.idx = self.generate_index(rhythms, rotations, iois)
        self.shuffle_trials(rhythms, rotations, iois)

    def __repr__(self):
        return str(self.trials)

    def __iter__(self):
        yield self.trials

    def shuffle_trials(self, rhythms, rotations, iois):
        # Shuffle rhythms and rotations within ioi groups
        trial_idx = [sample([sample(j, len(j)) for j in i], len(i)) for i in self.idx]

        # Sample equally from ioi groups using permutations
        k = len(iois)
        perms = [p for p in permutations(range(k))]
        ioi_idx = [*choice(perms)]

        for _ in range(len(rotations[0])):
            for i in range(len(rhythms)):
                for j in ioi_idx:
                    ioi, rhythm, rotation = trial_idx[j][i].pop()
                    self.trials.extend([(rhythm, rotation, ioi)])

                # Choose next permutation without repeating iois
                ioi_idx = [*choice([p for p in perms if p[0] != ioi_idx[-1]])]

        if not self.valid_shuffle():
            self.trials = []
            self.shuffle_trials(rhythms, rotations, iois)

    def valid_shuffle(self):
        valid_shuffle = all([x[:-1] != y[:-1] for x, y in zip(self.trials[:-1], self.trials[1:])])
        return valid_shuffle

    @staticmethod
    def generate_index(rhythms, rotations, iois):
        return [[[(ioi, rhythm, rotation)
                  for rotation in rotations[i]]
                 for i, rhythm in enumerate(rhythms)]
                for ioi in iois]
