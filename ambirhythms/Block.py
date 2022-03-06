import csv
from os import listdir, path
from pickle import load
from psychopy import core, event

from ambirhythms.Rhythms import Rhythms
from ambirhythms.Stimulus import Stimulus
from ambirhythms.TrialData import TrialData


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

    def run_block(self, drum_pad, participant_id, resume=None, loops=6):
        print('Participant: {0}\n' 
              'Block: {1} (\'{2}\')\n'
              'Trial: {3}'.format(participant_id,
                                  self.block_num,
                                  self.block_name,
                                  0 if resume is None else resume))
        if resume:
            self.resume_block(drum_pad, participant_id, resume, loops)
        else:
            for trial_num, trial in enumerate(self.trial_list):
                stimulus, trial_info = self.prepare_trial(trial_num, trial)
                data, result = self.run_trial(drum_pad, stimulus, loops)
                self.end_trial(participant_id, trial_info, data, result)

    def resume_block(self, drum_pad, participant_id, start, loops):
        for trial_num, trial in enumerate(self.trial_list[start:]):
            trial_num += start
            stimulus, trial_info = self.prepare_trial(trial_num, trial)
            data, result = self.run_trial(drum_pad, stimulus, loops)
            self.end_trial(participant_id, trial_info, data, result)

    @staticmethod
    def run_trial(drum_pad, stimulus, loops):
        result = [None for _ in range(5)]
        stimulus.play(loops=loops)
        drum_pad.reset()
        while not drum_pad.beat_found and stimulus.status == 1:
            tmp = drum_pad.find_beat(stimulus.ioi, detailed=True, verbose=True)
            if tmp is not None:
                result = tmp
        while stimulus.volume > 0:  # fade to avoid popping
            stimulus.volume -= 1e-5
        stimulus.stop()
        data = drum_pad.get_data()
        return [data, result]

    def prepare_trial(self, trial_num, trial):
        idx, r, ioi = trial
        durations = self.rhythms[idx].rotate(r).durations()
        stimulus = Stimulus(durations, ioi)
        trial_info = [self.block_num, self.block_name, trial_num, idx, r, ioi]
        return stimulus, trial_info

    def end_trial(self, participant_id, trial_info, data, result):
        trial_data = TrialData(participant_id, trial_info, data, result)
        core.wait(.5)
        trial_data.cache()
        self.trial_break(trial_data)

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

    def trial_break(self, trial_data):
        n = trial_data.trial_info['trial']
        if n == (len(self.trial_list) / 2) - 1:
            print('break')
            event.waitKeys(maxWait=2)
        elif n == len(self.trial_list)-1:
            self.write_block(trial_data.participant_id, trial_data)
            if self.block_num == 2:
                core.quit()
            else:
                print('next block')
                event.waitKeys(maxWait=2)
        else:
            pass
