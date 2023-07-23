from asciimatics.effects import Print
from asciimatics.renderers import BarChart
from asciimatics.exceptions import StopApplication
from asciimatics.screen import Screen


class ProgressBar(Print):
    def __init__(self, screen: Screen):
        super().__init__(
            screen,
            BarChart(
                1, screen.width - 20, [self.get_progress],
                char="/",
                scale=100,
                labels=False,
                axes=0,
                border=False,
                colour=3),
            x=10,
            y=(screen.height - 3),
            speed=2,
            transparent=False)
        self.progress = 0

    def _update(self, frame_no: int):
        if self.progress >= 100:
            raise StopApplication("Load Finished")
        else:
            self.progress += 100
            super()._update(frame_no)
