from ambirhythms import Experiment


def main(window, drum_pad, participant_id, finish_state, blocks):
    experiment = Experiment(participant_id, finish_state, blocks)
    experiment.begin(window, drum_pad)


if __name__ == '__main__':
    pass
