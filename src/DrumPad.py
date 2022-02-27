import mido
from warnings import warn
from operator import itemgetter
from psychopy.clock import Clock
from numpy import array, pi, cos, sin, sqrt, arctan2


class DrumPad:
    def __init__(self, device=''):
        # Device
        self.port = []
        self.open_port(device)
        self.clock = Clock()

        # States
        self.listening = False
        self.new_tap = False
        self.beat_found = False

        # Data
        self.taps = []
        self.velocities = []

    def open_port(self, device):
        inputs = mido.get_input_names()
        devices = [match for match in inputs if device in match]
        devices = list(dict.fromkeys(devices))

        if len(devices) == 0:
            raise ValueError('No device found matching name: {}'.format(device))

        if len(devices) == 1:
            idx = 0

        else:
            prompt = 'Multiple devices found:\n' + \
                     ''.join(['{}: {}\n'.format(i, device) for i, device in enumerate(devices)])
            print(prompt, '\n')

            while True:
                try:
                    idx = int(input('Select a device:'))
                    if 0 <= idx <= len(devices) + 1:
                        break

                except ValueError:
                    print('Please enter a number')

        self.port = mido.open_input(devices[idx], callback=self.tap)

    def tap(self, msg):
        if self.listening:
            t = self.clock.getTime()
            if msg.velocity == 0:
                return
            self.taps.append(t)
            self.velocities.append(msg.velocity)
            self.new_tap = True

    def find_beat(self, ioi, metre=12, n=10):
        beat, rotation = [None] * 2

        if len(self.taps) >= n and self.new_tap:
            self.new_tap = False
            taps = array([2 * pi * t / (ioi / 1000) for t in self.taps[-n:]])

            divisors = [i for i in range(1, metre + 1) if metre % i == 0]
            critical_value = [5.297, 5.556, 5.743, 5.885, 5.996, 6.085, 6.158, 6.219, 6.271][n-6]

            rho, theta, z, phase = [[None] * len(divisors)] * 4
            for i, d in enumerate(divisors):
                scaled = taps / d

                rho[i] = resultant_vector(scaled)
                theta[i] = circular_mean(scaled)
                z[i] = n * rho[i] ** 2

                if i == 0:
                    if z[i] > critical_value:
                        phase[i] = theta / (2 * pi)
                    else:
                        phase[i] = 0
                        warn('Unit phase too inconsistent for latency estimate')
                else:
                    phase[i] = round(d * (theta / (2 * pi) % 1) - phase[0]) % d

            accepted = dict([(divisors[i + 1], (Z, int(P))) for i, (Z, P) in enumerate(zip(z[1:], phase[1:]))
                             if Z > critical_value and z[0] > critical_value])
            if accepted:
                beat, (_, rotation) = max(accepted.items(), key=itemgetter(1))
                self.beat_found = True

            return beat, rotation

    def listen(self):
        self.reset()
        self.listening = True

    def stop(self):
        self.listening = False

    def reset(self, delay=0):
        self.clock.reset(delay)

        self.listening = False
        self.new_tap = False
        self.beat_found = False

        self.taps = []
        self.velocities = []


def resultant_vector(rads):
    x = sum(cos(rads)) ** 2
    y = sum(sin(rads)) ** 2
    return sqrt(x + y) / len(rads)


def circular_mean(rads):
    x = sum(cos(rads))
    y = sum(sin(rads))
    return arctan2(y, x)
