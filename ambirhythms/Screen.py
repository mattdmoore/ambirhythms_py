from psychopy import visual


class Screen(visual.Window):
    def __init__(self, size, backend):
        super().__init__(size, color=[0., 0., 0.], winType=backend, allowGUI=False)
        self.frame_rate = self.getActualFrameRate()

    def trial_feedback(self, stimulus, beat_found, rho, duration):
        feedback = visual.Rect(self, size=self.size)
        feedback.color = [0., 0., 0.]
        n_frames = int(self.frame_rate * duration)

        # Visual feedback
        if beat_found:
            feedback.color = [0., 1., 0.]  # green: beat found, trial ended early
        elif rho is not None:
            beat_strength = max(rho)
            feedback.color = [1., beat_strength, 0.]  # yellow: beat not found, shade based on max resultant vector
        else:
            feedback.color = [1., 0., 0.]  # red: not enough taps to calculate beat

        colour_increment = feedback.foreColor / n_frames
        volume_increment = 1 / n_frames

        for frame in range(n_frames):
            feedback.draw()
            feedback.color = feedback.foreColor - colour_increment
            stimulus.volume -= volume_increment  # fade to avoid popping
            self.flip()
        stimulus.stop()
