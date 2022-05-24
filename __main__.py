import ambirhythms
from os import chdir, listdir
from scripts import pseudorandomiser, experiment, practice


if __name__ == '__main__':
    if '__main__.py' not in listdir():  # if called as project folder
        chdir('ambirhythms')

    participant_id, finish_state = ambirhythms.last_cached()
    resume = any([state is not None for state in finish_state])

    blocks = pseudorandomiser.main(participant_id)

    drum_pad = ambirhythms.DrumPad('SPD')
    window = ambirhythms.Screen(size=(2000, 1125))
    window.welcome_screen(resume)

    if not resume:
        practice.main(window, drum_pad, participant_id)
    experiment.main(window, drum_pad, participant_id, finish_state, blocks)
