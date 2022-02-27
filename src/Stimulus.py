from numpy import linspace, sin, pi


class Stimulus:
    def __init__(self, durations, ioi, attack=2, decay=48):
        self.y = []
        self.t = []
        self.fs = 44.1e3

        self.ioi = ioi
        self.attack = attack
        self.decay = decay

        self.generate_rhythm(durations)

    def generate_rhythm(self, durations):
        for d in durations:
            self.append_sine()
            self.append_silence(d * self.ioi - (self.attack + self.decay))
        self.t = linspace(0, len(self.y) / self.fs, num=len(self.y)) * 1000

    def append_silence(self, ms):
        n = self.n_samples(ms)
        for _ in range(int(n)):
            self.y.append(0.0)

    def append_sine(self, hz=440):
        envelope = self.envelope(self.attack, self.decay)
        for i, x in enumerate(envelope):
            self.y.append(x * sin(2 * pi * hz * (i / self.fs)))

    def n_samples(self, ms):
        return ms * (self.fs / 1000)

    def envelope(self, attack, decay):
        attack_samples = int(self.n_samples(attack))
        decay_samples = int(self.n_samples(decay))

        A = list(linspace(0, 1, attack_samples))
        D = list(linspace(1, 0, decay_samples) ** 2)
        return A + D
