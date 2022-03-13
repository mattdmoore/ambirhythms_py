from numpy import roll, bincount, cumsum, zeros
from sympy.utilities.iterables import necklaces


class Rhythms:
    def __init__(self, n, k):
        self.rhythm = [Rhythm(n[::-1]) for n in necklaces(n, k)]

    def __getitem__(self, idx):
        return self.rhythm[idx]

    def __iter__(self):
        yield self.rhythm

    def __len__(self):
        return len(self.rhythm)


class Rhythm:
    def __init__(self, onsets):
        self.onsets = tuple(onsets)
        if max(onsets) > 1:
            self.from_durations(onsets)

    def __repr__(self):
        return str(self.onsets)

    def rotate(self, r):
        return Rhythm(roll(self.onsets, -r))

    def durations(self):
        durations = bincount(cumsum(self.onsets))
        durations[-1] += durations[0]
        return tuple(durations[1:])

    def from_durations(self, durations):
        idx = cumsum(durations) - durations
        onsets = zeros(sum(durations), dtype=int)
        onsets[idx] = 1
        self.onsets = tuple(onsets)
