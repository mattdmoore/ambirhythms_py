from random import random
from psychopy import visual
from .Utilities import get_response


class Screen(visual.Window):
    def __init__(self, size, backend='pyglet'):
        super().__init__(size, color=[0., 0., 0.], winType=backend, allowGUI=False)
        self.frame_rate = self.getActualFrameRate()

    def trial_feedback(self, stimulus, beat_found, rho, duration):
        duration += (random() - .5) / 5  # +/- 100ms jitter to inter-trial feedback
        feedback = visual.Rect(self, size=self.size)
        feedback.color = [0., 0., 0.]
        n_frames = int(self.frame_rate * duration)

        # Visual feedback
        if beat_found:
            feedback.color = [.5, 1., .5]  # green: beat found, trial ended early
        elif rho is not None:
            beat_strength = max(rho)
            feedback.color = [1., beat_strength, 0.]  # yellow: beat not found, shade based on max resultant vector
        else:
            feedback.color = [1., -.5, -.5]  # red: not enough taps to calculate beat

        colour_increment = feedback.foreColor / n_frames
        volume_increment = 1 / n_frames

        for frame in range(n_frames):
            feedback.draw()
            feedback.color = feedback.foreColor - colour_increment
            stimulus.volume -= volume_increment  # fade to avoid popping
            self.flip()
        stimulus.stop()

    def welcome_screen(self):
        text = 'Welcome to the experiment\nPress any key to begin'
        prompt = visual.TextBox2(self, text)
        prompt.draw()
        self.flip()

        get_response()
        self.instructions()

    def instructions(self):
        text = [
            'Use the left and right arrow keys to navigate these instructions',
            'page 2',
            'page 3',
            'Press enter when you are ready to begin the experiment'
        ]

        page_num = 0
        pages = [visual.TextBox2(self, t, alignment='centre') for t in text]

        while True:
            # Draw current page
            pages[page_num].draw()
            self.flip()

            # Navigate instruction pages
            response = get_response()
            if response == 'continue' and page_num == len(text) - 1:
                break
            else:
                page_num += response if 0 <= page_num + response <= len(text) - 1 else 0
