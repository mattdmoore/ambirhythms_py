from ambirhythms import Experiment, DrumPad, Screen


def main(participant_id, finish_state, blocks):
    experiment = Experiment(participant_id, finish_state, blocks)
    drum_pad = DrumPad('SPD')
    window = Screen((400, 400), 'pyglet')

    experiment.begin(window, drum_pad)


if __name__ == '__main__':
    pass
