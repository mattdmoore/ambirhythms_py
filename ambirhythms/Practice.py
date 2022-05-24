from .TrialData import TrialData
from .Stimulus import Stimulus


class Practice:
    def __init__(self, participant_id, rhythm, ioi, inter_trial_interval=.5):
        self.participant_id = participant_id
        self.rhythm = rhythm
        self.ioi = ioi
        self.trial_info = ['practice', 'practice', 0, 0, 0, ioi]
        self.inter_trial_interval = inter_trial_interval

    def begin(self, window, drum_pad, loops=6):
        stimulus = Stimulus(self.rhythm.durations(), self.ioi)
        data, result = self.run_trial(window, drum_pad, stimulus, loops)
        self.end_trial(data, result)

    def run_trial(self, window, drum_pad, stimulus, loops):
        result = [None for _ in range(5)]

        window.fixation_cross(True)
        stimulus.play(loops=loops)
        drum_pad.reset()
        while not drum_pad.beat_found and stimulus.status == 1:
            tmp = drum_pad.find_beat(stimulus.ioi, metre=16, detailed=True, verbose=True)
            if tmp is not None:
                result = tmp

        window.trial_feedback(stimulus, drum_pad.beat_found, result[2], self.inter_trial_interval)
        window.practice_complete()
        data = drum_pad.get_data()
        return [data, result]

    def end_trial(self, data, result):
        trial_data = TrialData(self.participant_id, self.trial_info, data, result)
        trial_data.cache()
