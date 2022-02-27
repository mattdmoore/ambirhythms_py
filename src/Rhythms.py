from numpy import roll, bincount, cumsum
from sympy.utilities.iterables import necklaces


class Rhythms:
    def __init__(self, n, k):
        self.rhythm = [Rhythm(n[::-1]) for n in necklaces(n, k)]

    def __getitem__(self, idx):
        return self.rhythm[idx]


class Rhythm:
    def __init__(self, onsets):
        self.onsets = tuple(onsets)

    def __repr__(self):
        return str(self.onsets)

    def rotate(self, r):
        return Rhythm(roll(self.onsets, -r))

    def durations(self):
        durations = bincount(cumsum(self.onsets))
        durations[-1] += durations[0]
        return tuple(durations[1:])
