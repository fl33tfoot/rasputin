#!/usr/bin/env python3

import sys
from time import sleep
from ProgressBar import ProgressBar

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from src.Rasputin import Rasputin


# Declarations
activeFace = True
activeCamera = False
button_timeout = 0.4
vol = 0

# TODO: refactor to env variables
rgb = False
loop = False
audio = True

default_data = (rgb, loop, audio)

progress = 0
last_scene = None

current_menu = 0


def load(screen: Screen):
    effects = [
        Print(screen, FigletText("ProtOS v1.4", font='trek'), screen.height // 2 + 2, screen.width // 20, colour=3,
              bg=0),
        ProgressBar(screen)
    ]

    scenes = Scene(effects)
    screen.play(scenes, stop_on_resize=False)


def main(screen, scene):
    _scenes = [
        Scene(Rasputin(screen, default_data=default_data, active_face=activeFace, active_camera=activeCamera,
                       button_timeout=button_timeout, vol=vol, current_menu=current_menu), -1, name="Rasputin"),
    ]
    screen.play(_scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

sleep(1)
Screen.wrapper(load)

while True:
    try:
        sleep(0.1)
        Screen.wrapper(main, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
