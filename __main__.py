import ambirhythms

from scripts import pseudorandomiser
from scripts import experiment

# TODO:
#   Pseudorandomiser checks to prevent clumps
#     x - Consecutive rhythms
#     x - Consecutive (un-)/ambiguous
#     x - BUG: improper tempo shuffling due to pseudorandomiser call on resume (fixed by caching block data)
#   Store dynamically calculated beat data   DONE
#     x - Phase, mean resultant vector, Rayleigh test z-value
#   Build visual components
#       - Instructions, messages for breaks
#     x - Feedback (experimental): screen colour flash between trials
#         x - Green: beat found, trial ended early
#         x - Yellow to orange: beat not found, yellow shade uses beat with max resultant vector
#         x - Red: not enough taps to reliably calculate statistics
#   Practice trial
#       - Example using 16-unit metre with clear beats
#       - Experimenter check that participant is tapping hard enough
#   Assemble full experiment (no visuals)   DONE
#     x - Counterbalance blocked and randomised lists
#     x - Inter- and intra-block breaks (both skippable but intra-block timed to 2min?)
#   Data storage
#     x - Pickle cache after every trial
#     x - Write to csv between blocks
#   Package for install
#       - Check on clean Python environment in Windows first, then lab install
#            - Runs on laptop, soundcard(?) issues on PC; check with soundcard on laptop

if __name__ == '__main__':
    participant_id, finish_state = ambirhythms.last_cached()
    blocks = pseudorandomiser.main(participant_id)

    experiment.main(participant_id, finish_state, blocks)
