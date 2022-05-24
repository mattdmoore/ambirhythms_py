import csv
from os import listdir, path
from pickle import load

from psychopy import core

from .Rhythms import Rhythms
from .Stimulus import Stimulus
from .TrialData import TrialData


class Block:
    def __init__(self, block_num, block_name, trial_list):
        self.trial_list = trial_list
        self.block_num = block_num
        self.block_name = ['blocked_ambiguous',
                           'blocked_unambiguous',
                           'randomised'][block_name]
        self.rhythms = Rhythms(12, 2)

    def __len__(self):
        return len(self.trial_list)

    def run_block(self, window, drum_pad, participant_id, resume=None):
        print('Participant: {0}\n' 
              'Block: {1} (\'{2}\')\n'
              'Trial: {3}'.format(participant_id,
                                  self.block_num,
                                  self.block_name,
                                  0 if not resume else resume))
        if resume is None:
            resume = 0
        for trial_num, trial in enumerate(self.trial_list[resume:]):
            trial_num += resume
            stimulus, trial_info = self.prepare_trial(trial_num, trial)
            data, result = self.run_trial(window, drum_pad, stimulus)
            self.end_trial(window, participant_id, trial_info, data, result)

    def prepare_trial(self, trial_num, trial):
        idx, r, ioi = trial
        durations = self.rhythms[idx].rotate(r).durations()
        stimulus = Stimulus(durations, ioi)
        trial_info = [self.block_num, self.block_name, trial_num, idx, r, ioi]
        return stimulus, trial_info

    def run_trial(self, window, drum_pad, stimulus, loops=6):
        result = [None for _ in range(5)]

        window.fixation_cross()
        stimulus.play(loops=loops)
        drum_pad.reset()
        while not drum_pad.beat_found and stimulus.status == 1:
            tmp = drum_pad.find_beat(stimulus.ioi, detailed=True, verbose=True)
            if tmp is not None:
                result = tmp

        window.trial_feedback(stimulus, drum_pad.beat_found, result[2], duration=.6)
        data = drum_pad.get_data()
        return [data, result]

    def end_trial(self, window, participant_id, trial_info, data, result):
        trial_data = TrialData(participant_id, trial_info, data, result)
        core.wait(.5)
        trial_data.cache()

        n = trial_info[2]
        if n == (len(self.trial_list) // 2) - 1:  # Block middle
            window.break_prompt(self.block_num)
        elif n == len(self.trial_list) - 1:  # Block end
            self.write_block(trial_data.participant_id, trial_data)
            window.break_prompt(self.block_num, True)

    def write_block(self, participant_id, trial_data):
        data = {'participant_id': participant_id,
                **trial_data.trial_info,
                **trial_data.data,
                **trial_data.result
                }
        target = 'data/participant_{:02d}.csv'.format(participant_id)
        cache_dir = 'data/cache/participant_{}/block_{}'.format(participant_id,
                                                                self.block_num)
        cache_files = ['/'.join([cache_dir, file]) for file in sorted(listdir(cache_dir))]

        exists = path.isfile(target)
        with open(target, 'a', newline='') as data_file:
            if not exists:
                csv.DictWriter(data_file, fieldnames=list(data.keys())).writeheader()
            for cache_file in cache_files:
                with open(cache_file, 'rb') as c:
                    cache = load(c)
                    cache.write_csv(data_file)
