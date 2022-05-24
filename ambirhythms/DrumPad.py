import mido
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
        if self.listening and msg.type == 'note_on':
            t = self.clock.getTime()
            if msg.velocity == 0:  # ignore note off messages
                return
            if self.taps and t - self.taps[-1] < .1:  # ignore sub-100ms taps (stick bounce)
                return
            self.taps.append(t)
            self.velocities.append(msg.velocity)
            self.new_tap = True

    def find_beat(self, ioi, metre=12, n=9, verbose=False, detailed=False):
        if not 5 < n < 15:
            raise ValueError('n must be between 6 and 14 (inclusive)')
        if not self.listening:
            self.listen()

        if self.new_tap and len(self.taps) >= n:
            self.new_tap = False

            # Raw taps are in seconds before conversion e.g., [1.1, 1.4, 1.7, 2.0, 2.3 ...]
            taps = array([2 * pi * t * 1e3 / ioi for t in self.taps[-n:]])  # scale to metre, convert to radians

            # Rayleigh test vals
            # critical_value = [5.297, 5.556, 5.743, 5.885, 5.996, 6.085, 6.158, 6.219, 6.271, 6.316][n-6]  # p = .001
            critical_value = [4.985, 5.181, 5.322, 5.430, 5.514, 5.582, 5.638, 5.685, 5.725, 5.759][n - 6]  # p = .002

            divisors = [i for i in range(1, metre + 1) if metre % i == 0]  # 1, 2, 3, 4, 6, 12
            rho, theta, z, phase = [[None] * len(divisors) for _ in range(4)]  # preallocate variables

            for i, d in enumerate(divisors):
                scaled = taps / d  # scale taps using each divisor

                # Circular stats
                rho[i] = resultant_vector(scaled)
                theta[i] = circular_mean(scaled)
                z[i] = n * rho[i] ** 2  # Rayleigh test

                if i == 0:
                    if z[i] > critical_value:  # if unit-level vector length is significant, use to estimate latency
                        phase[i] = theta[i] / (2 * pi)
                    else:
                        phase[i] = 0
                else:  # use unit-level phase to correct beat phases
                    phase[i] = d * (theta[i] / (2 * pi) % 1) - phase[0]
                    phase[i] = int(round(phase[i]) % d)

            # Only accept significant beat vector lengths if unit vector length is also significant
            accepted = dict([(divisors[i+1], (Z, P)) for i, (Z, P) in enumerate(zip(z[1:], phase[1:]))
                             if Z > critical_value and z[0] > critical_value])

            if accepted:
                beat, (_, phase) = max(accepted.items(), key=itemgetter(1))
                if verbose:
                    self.print_summary(beat, phase, taps, metre)
                self.beat_found = True

                # Beat found
                return [beat, phase, rho, theta, z] if detailed else [beat, phase]
            # Beat not found
            return [None, None, rho, theta, z] if detailed else [None, None]

    def get_data(self):
        self.stop()
        return [self.taps, self.velocities]

    def listen(self, delay=0):
        self.reset(delay)
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

    def print_summary(self, beat, phase, taps, metre):
        print('Beat: {0} \tPhase: {1}'.format(beat,
                                              phase))
        print('Found in {0:.1f} cycles | {1} taps'.format(taps[-1] / (2 * metre * pi),
                                                          len(self.taps)))


def resultant_vector(rads):
    x = sum(cos(rads)) ** 2
    y = sum(sin(rads)) ** 2
    return sqrt(x + y) / len(rads)


def circular_mean(rads):
    x = sum(cos(rads))
    y = sum(sin(rads))
    return arctan2(y, x)
