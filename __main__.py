from psychopy.core import wait

from ambirhythms.Rhythms import Rhythms
from ambirhythms.Stimulus import Stimulus
from ambirhythms.DrumPad import DrumPad

from scripts import pseudorandomiser

# TODO:
#   Pseudorandomiser checks to prevent clumps   DONE
#     x - Consecutive rhythms
#     x - Consecutive (un-)/ambiguous
#   Save dynamically calculated beat data   DONE
#     x - Phase, mean resultant vector, Rayleigh test z-value
#   Build visual components
#       - Instructions, fixation cross, signposting for taps/breaks/etc
#   Practice trial
#       - Example using 16-unit metre with clear beats
#       - Experimenter check that participant is tapping hard enough
#   Assemble full experiment
#       - Counterbalance blocked and randomised lists
#       - Inter- and intra-block breaks (both skippable but intra-block timed to 2min)
#   Data storage
#       - Pickle cache after every trial, write to csv at end (keep cache)
#   Package for install
#       - Check on clean Python environment in Windows first, then lab install


def run_block(trial_list):
    block = [[], []]
    for i, trial in enumerate(trial_list.trials):
        idx, r, ioi = trial
        durations = rhythms[idx].rotate(r).durations()
        h = 0 if i < len(trial_list) / 2 else 1
        block[h].append(Stimulus(durations, ioi))

    for half in block:
        for stimulus in half:
            stimulus.play(loops=6)
            while stimulus.status == 1 and not drum_pad.beat_found:
                drum_pad.find_beat(stimulus.ioi, verbose=True)
            stimulus.stop()
            drum_pad.reset()
            wait(2)
        wait(120)


def block_order(i):
    orders = {
        0: (0, 1, 2),
        1: (1, 2, 0),
        2: (0, 2, 1),
        3: (2, 1, 0)
    }
    return orders[i % 4]


if __name__ == '__main__':
    participant_id = 0

    drum_pad = DrumPad('SPD')
    rhythms = Rhythms(12, 2)
    blocks = pseudorandomiser.main()
    [run_block(blocks[i]) for i in block_order(participant_id)]
