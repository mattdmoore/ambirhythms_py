from random import random
from psychopy import visual, event
from os import listdir
from .Utilities import keyboard_response


class Screen(visual.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, color=(-.62, -.62, -.62), allowGUI=False)
        self.mouse = event.Mouse(visible=False, win=self)
        self.frame_rate = self.getActualFrameRate()

        files = sorted(listdir('./instructions'))
        self.pages = [visual.ImageStim(self, 'instructions/' + f) for f in files]

    def fixation_cross(self, practice=False):
        size = 10
        fixation = [visual.Line(win=self, start=[-size, 0], end=[size, 0], units='pix'),
                    visual.Line(win=self, start=[0, -size], end=[0, size], units='pix')]

        if practice:
            text = visual.TextBox2(win=self,
                                   text='Practice trial',
                                   pos=[0, .2],
                                   font='Roboto light',
                                   letterHeight=.08,
                                   alignment='center')
            text.draw()
        [line.draw() for line in fixation]
        self.flip()

    def trial_feedback(self, stimulus, beat_found, rho, duration, jitter_amount=75):
        jitter = jitter_amount * ((random() - .5) * 2) / 1000
        duration += jitter
        feedback = visual.Rect(self, size=self.size)
        feedback.color = (-.62, -.62, -.62)
        n_frames = int(self.frame_rate * duration)

        # Visual feedback
        if beat_found:
            feedback.color = [.31, 1., .31]  # green: beat found, trial ended early
        elif rho is not None:
            beat_strength = max(rho)
            feedback.color = [1., beat_strength, beat_strength / 2 - .5]  # yellow: beat not found
        else:
            feedback.color = [.5, -.75, -.75]  # red: not enough taps to calculate beat
        colour_increment = (feedback.foreColor + .62) / n_frames
        volume_increment = 1 / n_frames

        for frame in range(n_frames):
            feedback.draw()
            feedback.color = feedback.foreColor - colour_increment * (2 * frame / (n_frames - 1))  # quadratic decay
            stimulus.volume -= volume_increment  # fade to avoid popping
            self.flip()
        self.flip()
        stimulus.stop()

    def welcome_screen(self, resume=False):
        self.pages[0].draw()
        self.flip()

        event.waitKeys()
        return None if resume else self.instructions()

    def instructions(self):
        def clamp(x, lower, upper): return lower if x < lower else upper if x > upper else x

        first, last = 1, 12
        i = first
        while True:
            self.pages[i].draw()
            self.flip()

            key = keyboard_response()
            if i == last and key == 0:
                self.flip()
                return
            i = clamp(i + key, first, last)

    def practice_complete(self):
        self.pages[19].draw()
        self.flip()
        while keyboard_response() != 0:
            continue
        self.flip()

    def break_prompt(self, block, end=False):
        idx = 13 + (block * 2) + int(end)
        self.pages[idx].draw()
        self.flip()
        while keyboard_response() != 0:
            continue
        self.flip()
