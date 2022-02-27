from psychopy import prefs; prefs.hardware['audioLib'] = ['PTB']
from psychopy.sound import Sound

from src.Rhythms import Rhythms
from src.Stimulus import Stimulus

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
rhythm = rhythms[idx]
rotations = nonzero(rhythm.onsets)[0]

for r in rotations:
    obj = Stimulus(rhythm.rotate(r).durations())

    sound = Sound(obj.y, sampleRate=obj.fs)
    sound.play(loops=5)

    m = [i * obj.ioi for i in range(12)]

    plt.plot(obj.t, obj.y)
    plt.vlines(m, min(obj.y), max(obj.y), color='red')
    plt.title('Rhythm {0}\nRotation {1}'.format(idx, r))
    plt.show()
