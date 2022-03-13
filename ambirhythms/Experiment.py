from os import path
from pickle import dump, load, HIGHEST_PROTOCOL

from .Utilities import block_cache_path


class Experiment:
    def __init__(self, participant_id, finish_state, blocks):
        self.participant_id = participant_id
        self.finish_state = finish_state
        self.blocks = blocks

    def begin(self, window, drum_pad):
        if self.last_participant_finished():
            self.participant_id += 1
            self.new_participant(window, drum_pad)
        else:
            self.resume_participant(window, drum_pad, *self.finish_state)

    def last_participant_finished(self):
        return self.finish_state == [2, 119]

    def save_blocks(self):
        block_cache = block_cache_path(self.participant_id)
        try:
            with open(block_cache, 'wb') as b:
                dump(self.blocks, b, protocol=HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object:", ex)

    def load_blocks(self):
        block_cache = block_cache_path(self.participant_id)
        if not path.isfile(block_cache):
            return self.save_blocks()
        try:
            with open(block_cache, 'rb') as b:
                self.blocks = load(b)
        except Exception as ex:
            print("Error during unpickling object:", ex)

    def new_participant(self, window, drum_pad):
        self.save_blocks()
        for block in self.blocks:
            block.run_block(window, drum_pad, self.participant_id)

    def resume_participant(self, window, drum_pad, b, t):
        self.load_blocks()
        b = 0 if b is None else b + 1 if t == 119 else b  # increment block if resuming from last trial in block
        t = 0 if t in (None, 119) else t + 1  # reset trial to zero if resuming from new block, otherwise increment

        self.blocks[b].run_block(window, drum_pad, self.participant_id, t)
        for block in self.blocks[b + 1:]:
            block.run_block(window, drum_pad, self.participant_id)
