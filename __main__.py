from psychopy import visual
from ambirhythms.DrumPad import DrumPad
from scripts import experiment

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
#   Assemble full experiment    DONE
#     x - Counterbalance blocked and randomised lists
#     x - Inter- and intra-block breaks (both skippable but intra-block timed to 2min)
#   Data storage
#     x - Pickle cache after every trial
#     x - Write to csv between blocks
#   Package for install
#       - Check on clean Python environment in Windows first, then lab install

if __name__ == '__main__':
    drum_pad = DrumPad('SPD')
    window = visual.Window((10, 10), allowGUI=False)
    experiment.main(drum_pad)
