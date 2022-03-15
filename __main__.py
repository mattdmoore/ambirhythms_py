import ambirhythms

from scripts import pseudorandomiser, experiment, practice

# TODO:
#   Build visual components
#       - Instructions, messages for breaks
#       - Explain yellow shades feedback
#   Practice trial
#       - Example using 16-unit metre with clear beats
#       - Experimenter check that participant is tapping hard enough
#   Assemble full experiment (no visuals)
#     x - Counterbalance blocked and randomised lists
#     x - Inter- and intra-block breaks (both skippable but intra-block timed to 2min?)
#       - Jitter inter-trial interval between .5 and 1s
#   Package for install
#       - Check on clean Python environment in Windows first, then lab install
#            - Runs on laptop, soundcard(?) issues on PC; check with soundcard on laptop

if __name__ == '__main__':
    participant_id, finish_state = ambirhythms.last_cached()
    blocks = pseudorandomiser.main(participant_id)

    drum_pad = ambirhythms.DrumPad('SPD')
    window = ambirhythms.Screen((400, 400), 'pyglet')

    practice.main(window, drum_pad, participant_id)
    experiment.main(window, drum_pad, participant_id, finish_state, blocks)
