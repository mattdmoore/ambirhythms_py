from random import choice, sample
from itertools import permutations


class Trials:
    def __init__(self, rhythms, rotations, iois):
        self.trials = []
        self.rhythms = rhythms
        self.rotations = rotations
        self.iois = iois

        self.idx = self.generate_index(rhythms, rotations, iois)
        self.shuffle_trials()

    def __repr__(self):
        return '\n'.join(str(t) for t in self.trials)

    def __iter__(self):
        yield self.trials

    def __len__(self):
        return len(self.trials)

    def shuffle_trials(self):
        # Shuffle rhythms and rotations within ioi groups
        trial_idx = [sample([sample(j, len(j)) for j in i], len(i)) for i in self.idx]

        # Sample equally from ioi groups using permutations
        k = len(self.iois)
        perms = [p for p in permutations(range(k))]
        ioi_idx = [*choice(perms)]

        for _ in range(len(self.rotations[0])):
            for i in range(len(self.rhythms)):
                for j in ioi_idx:
                    ioi, rhythm, rotation = trial_idx[j][i].pop()
                    self.trials.extend([(rhythm, rotation, ioi)])

                # Choose next permutation without repeating iois
                ioi_idx = [*choice([p for p in perms if p[0] != ioi_idx[-1]])]

        cutoff = 2
        if not self.valid_shuffle(cutoff):
            self.trials = []
            self.shuffle_trials()

    def valid_shuffle(self, cutoff):
        consecutive = 0
        for last_trial, trial in zip(self.trials[:-1], self.trials[1:]):
            consecutive += 1 if trial[0] == last_trial[0] else -consecutive
            if consecutive == cutoff or last_trial[:-1] == trial[:-1]:
                return False
        return True

    @staticmethod
    def generate_index(rhythms, rotations, iois):
        return [[[(ioi, rhythm, rotation)
                  for rotation in rotations[i]]
                 for i, rhythm in enumerate(rhythms)]
                for ioi in iois]
