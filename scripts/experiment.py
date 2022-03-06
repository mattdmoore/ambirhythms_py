from os import listdir
from re import findall
from itertools import chain

from scripts import pseudorandomiser


def highest_file_num(directory):
    files = listdir(directory)
    digits = [int(x) for x in chain(*[findall(r'\d+', name) for name in files])]
    return max(digits) if digits else None


def last_cached(directory='data/cache', level=0, result=None):
    if result is None:
        result = [None, None, None]
        if 'data' not in listdir():
            return result

    i = highest_file_num(directory)
    if i is not None:
        result[level] = i
        subdirectory = ['participant', 'block', 'trial'][level]
        directory = '/'.join([directory, subdirectory + '_{}'.format(i)])
        return last_cached(directory, level+1, result) if level < 2 else result
    return result


def new_participant(drum_pad, i):
    blocks = pseudorandomiser.main(i)
    for block in blocks:
        block.run_block(drum_pad, i)


def resume_participant(drum_pad, i, b, t):
    blocks = pseudorandomiser.main(i)
    b += 1 if t == 119 else 0  # increment block if resuming from last trial in block
    t = 0 if t in (None, 119) else t+1  # reset trial to zero if resuming from new block, otherwise increment

    blocks[b].run_block(drum_pad, i, t)
    for block in blocks[b+1:]:
        block.run_block(drum_pad, i)


def main(drum_pad):
    participant_id, last_block, last_trial = last_cached()
    finish_state = [2, 119]

    # First participant
    if participant_id is None:
        new_participant(drum_pad, 0)

    # Last participant reached finish state
    elif [last_block, last_trial] == finish_state:
        participant_id += 1
        new_participant(drum_pad, participant_id)

    # Otherwise, resume last participant
    else:
        resume_participant(drum_pad, participant_id, last_block, last_trial)
