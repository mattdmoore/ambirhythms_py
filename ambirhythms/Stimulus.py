from psychopy import prefs; prefs.hardware['audioLib'] = ['PTB']
from psychopy.sound import Sound
from numpy import linspace, sin, pi


class Stimulus(Sound):
    def __init__(self, durations, ioi, fs=44.1e3, attack=2, decay=48, hz=440):
        self.value = []
        self.time = []

        self.sampleRate = fs
        self.ioi = ioi
        self.attack = attack
        self.decay = decay
        self.hz = hz

        self.generate_rhythm(durations)
        super().__init__(self.value, sampleRate=fs)

    def generate_rhythm(self, durations):
        for d in durations:
            self.append_sine()
            self.append_silence(d * self.ioi - (self.attack + self.decay))
        self.time = linspace(0, len(self.value) / self.sampleRate, num=len(self.value)) * 1e3

    def append_silence(self, ms):
        n = self.n_samples(ms)
        for _ in range(int(n)):
            self.value.append(0.0)

    def append_sine(self):
        envelope = self.envelope(self.attack, self.decay)
        for i, x in enumerate(envelope):
            self.value.append(x * sin(2 * pi * self.hz * (i / self.sampleRate)))

    def n_samples(self, ms):
        return ms * (self.sampleRate / 1e3)

    def envelope(self, attack, decay):
        attack_samples = int(self.n_samples(attack))
        decay_samples = int(self.n_samples(decay))

        A = list(linspace(0, 1, attack_samples))
        D = list(linspace(1, 0, decay_samples) ** 2)
        return A + D
