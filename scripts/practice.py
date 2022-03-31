from ambirhythms.Rhythms import Rhythm
from ambirhythms.Practice import Practice


def main(window, drum_pad, participant_id):
    ioi = 160
    rhythm = Rhythm([1, 0, 0, 0,
                     1, 0, 1, 0,
                     1, 0, 1, 1,
                     1, 0, 0, 0])

    practice = Practice(participant_id, rhythm, ioi)
    # practice.begin(window, drum_pad)
