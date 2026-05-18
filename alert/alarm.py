import platform
import threading

try:
    import winsound
except ImportError:
    winsound = None

try:
    import numpy as np
    import simpleaudio as sa
except ImportError:
    np = None
    sa = None

class Alarm:
    def __init__(self, frequency=1200, duration=0.15):
        self.frequency = frequency
        self.duration = duration
        self.active = False

    def trigger(self):
        if self.active:
            return
        self.active = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        try:
            if winsound and platform.system() == 'Windows':
                winsound.Beep(self.frequency, int(self.duration * 1000))
            elif sa and np is not None:
                self._play_tone()
        finally:
            self.active = False

    def _play_tone(self):
        sample_rate = 44100
        length = int(sample_rate * self.duration)
        time_axis = np.linspace(0, self.duration, length, False)
        tone = np.sin(self.frequency * time_axis * 2 * np.pi)
        audio = (tone * 32767).astype(np.int16)
        sa.play_buffer(audio, 1, 2, sample_rate)
