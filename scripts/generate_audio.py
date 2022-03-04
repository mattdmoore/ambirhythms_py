from ambirhythms.Rhythms import Rhythms
from ambirhythms.Stimulus import Stimulus
from ambirhythms.DrumPad import DrumPad

from numpy import nonzero
import matplotlib.pyplot as plt

rhythms = Rhythms(12, 2)

ambiguous = [57, 62, 90, 229, 259,
             120, 121, 133, 187, 349,
             35, 76, 96, 148, 196]

unambiguous = [135, 131, 175, 300, 200,
               232, 165, 82, 300, 347,
               11, 140, 24, 75, 136]

idx = 57
ioi = 200
rhythm = rhythms[idx]
rotations = nonzero(rhythm.onsets)[0]

drum_pad = DrumPad('SPD')
for r in rotations:
    obj = Stimulus(rhythm.rotate(r).durations(), ioi)

    obj.play(loops=6)
    while obj.status == 1 and not drum_pad.beat_found:
        beat, rotation = drum_pad.find_beat(ioi, verbose=True)
    obj.stop()
    drum_pad.reset()

    m = [i * obj.ioi for i in range(12)]

    plt.plot(obj.time, obj.value)
    plt.vlines(m, min(obj.value), max(obj.value), color='red')
    plt.title('Rhythm {0}\nRotation {1}'.format(idx, r))
    plt.show()
