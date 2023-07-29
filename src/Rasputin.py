import json
import os
import subprocess
from random import randint
from typing import Tuple
from time import sleep
import sys
from functools import partial

from asciimatics.event import Event
from asciimatics.parsers import AsciimaticsParser
from asciimatics.widgets import Frame, Layout, TextBox, Widget, Button, VerticalDivider, Divider, CheckBox
from asciimatics.screen import Screen


def register_animation(layout: Layout, name: str, column: int, action: callable):
    layout.add_widget(Button(name, action, column))


class Rasputin(Frame):
    def __init__(self, screen: Screen, default_data: Tuple[bool, bool, bool],
                 active_face=True, active_camera=False, button_timeout=0.4, vol=0,
                 current_menu=0) -> None:
        super().__init__(screen, screen.height, screen.width, default_data, can_scroll=False,
                         has_border=True, title="R4SPUT1N")

        self.button_timeout = button_timeout
        self.active_camera = active_camera
        self.active_face = active_face
        self.vol = vol
        self.RGB, self.LOOP, self.AUDIO = default_data
        self.current_menu = current_menu

        # INITIAL COLOR CONFIGURATION
        self.register_palette()

        # INITIAL TOP TAB LAYOUTS
        layout_tabs = Layout([19, 1, 19, 1, 19, 1, 19, 1, 20], fill_frame=False)
        layout_subtabs_main = Layout([19, 1, 19, 1, 19, 1, 19, 1, 20], fill_frame=False)
        layout_subtabs_extra = Layout([19, 1, 19, 1, 19, 1, 19, 1, 20], fill_frame=False)
        layout_subtabs_audio = Layout([19, 1, 19, 1, 19, 1, 19, 1, 20], fill_frame=False)
        layout_subtabs_mgmt = Layout([19, 1, 19, 1, 19, 1, 19, 1, 20], fill_frame=False)

        # INDIVIDUAL TAB LAYOUTS
        layout_content_main = Layout([20, 20, 20, 20, 20], fill_frame=False)
        layout_content_extra = Layout([20, 20, 20, 20, 20], fill_frame=False)
        layout_content_audio = Layout([20, 20, 20, 20, 20], fill_frame=False)
        layout_content_mgmt = Layout([24, 1, 25, 25, 25], fill_frame=False)

        # CONSOLE LAYOUT
        layout_console = Layout([100], fill_frame=True)

        layout1 = Layout([24, 1, 25, 25, 25], fill_frame=False)

        layouts = [layout_tabs, layout_subtabs_main, layout_subtabs_extra,
                   layout_subtabs_audio, layout_subtabs_audio, layout_subtabs_mgmt,
                   layout_content_main, layout_content_extra, layout_content_audio,
                   layout_content_mgmt, layout1, layout_console]

        for layout in layouts:
            self.add_layout(layout)

        # CONSOLE LAYOUT
        self.console = layout_console.add_widget(
            TextBox(Widget.FILL_FRAME, label="CONSOLE:", parser=AsciimaticsParser(), name="CONSOLE", line_wrap=True,
                    readonly=True, as_string=True))
        self.console.custom_colour = 'title'
        self.console.hide_cursor = True
        self.console.disabled = True

        # TOP TAB LAYOUT
        layout_tabs.add_widget(Button("MAIN", self._vol_up), 0)
        layout_tabs.add_widget(VerticalDivider(), 1)
        layout_tabs.add_widget(Button("EXTRA", self._vol_up), 2)
        layout_tabs.add_widget(VerticalDivider(), 3)
        layout_tabs.add_widget(Button("AUDIO", self._vol_up), 4)
        layout_tabs.add_widget(VerticalDivider(), 5)
        layout_tabs.add_widget(Button("MGMT", self._vol_up), 6)
        layout_tabs.add_widget(VerticalDivider(), 7)
        layout_tabs.add_widget(Button("QUIT", self.exit_event), 8)

        # DIVIDER SPACERS
        layout_tabs.add_widget(Divider(draw_line=True), 0)
        layout_tabs.add_widget(Divider(draw_line=True), 0)
        layout_tabs.add_widget(Divider(draw_line=True), 1)
        layout_tabs.add_widget(Divider(draw_line=True), 1)
        layout_tabs.add_widget(Divider(draw_line=True), 2)
        layout_tabs.add_widget(Divider(draw_line=True), 2)
        layout_tabs.add_widget(Divider(draw_line=True), 3)
        layout_tabs.add_widget(Divider(draw_line=True), 3)
        layout_tabs.add_widget(Divider(draw_line=True), 4)
        layout_tabs.add_widget(Divider(draw_line=True), 4)
        layout_tabs.add_widget(Divider(draw_line=True), 5)
        layout_tabs.add_widget(Divider(draw_line=True), 5)
        layout_tabs.add_widget(Divider(draw_line=True), 6)
        layout_tabs.add_widget(Divider(draw_line=True), 6)
        layout_tabs.add_widget(Divider(draw_line=True), 7)
        layout_tabs.add_widget(Divider(draw_line=True), 7)
        layout_tabs.add_widget(Divider(draw_line=True), 8)
        layout_tabs.add_widget(Divider(draw_line=True), 8)

        # SUBTAB MAIN LAYOUT
        layout_subtabs_main.add_widget(CheckBox("RGB", on_change=self._toggle_rbg, name="RGB"), 0)
        layout_subtabs_main.add_widget(VerticalDivider(), 1)
        layout_subtabs_main.add_widget(CheckBox("LOOP", on_change=self._toggle_loop, name="LOOP"), 2)
        layout_subtabs_main.add_widget(VerticalDivider(), 3)
        layout_subtabs_main.add_widget(CheckBox("SOUND", on_change=self._toggle_audio, name="AUDIO"), 4)
        layout_subtabs_main.add_widget(VerticalDivider(), 5)
        layout_subtabs_main.add_widget(Button("PAIR SPEAKER", self._pair_bluetooth_speaker), 6)
        layout_subtabs_main.add_widget(VerticalDivider(), 7)
        layout_subtabs_main.add_widget(Button("KILL FACE", self.force_kill), 8)

        # DIVIDER SPACERS
        layout_subtabs_main.add_widget(Divider(draw_line=True), 0)
        layout_subtabs_main.add_widget(Divider(draw_line=True), 1)
        layout_subtabs_main.add_widget(Divider(draw_line=True), 2)
        layout_subtabs_main.add_widget(Divider(draw_line=True), 3)
        layout_subtabs_main.add_widget(Divider(draw_line=True), 4)
        layout_subtabs_main.add_widget(Divider(draw_line=True), 5)
        layout_subtabs_main.add_widget(Divider(draw_line=True), 6)
        layout_subtabs_main.add_widget(Divider(draw_line=True), 7)
        layout_subtabs_main.add_widget(Divider(draw_line=True), 8)

        # SUBTAB AUDIO LAYOUT
        layout_subtabs_audio.add_widget(Button("VOL +", self._vol_up), 0)
        layout_subtabs_audio.add_widget(VerticalDivider(), 1)
        layout_subtabs_audio.add_widget(Button("VOL -", self._vol_down), 2)
        layout_subtabs_audio.add_widget(VerticalDivider(), 3)
        layout_subtabs_audio.add_widget(CheckBox("SOUND", on_change=self._toggle_audio, name="AUDIO"), 4)
        layout_subtabs_audio.add_widget(VerticalDivider(), 5)
        layout_subtabs_audio.add_widget(Button("PAIR SPEAKER", self._pair_bluetooth_speaker), 6)
        layout_subtabs_audio.add_widget(VerticalDivider(), 7)
        layout_subtabs_audio.add_widget(Button("RANDOM AUDIO", self._play_audio_random), 8)

        # DIVIDER SPACERS
        layout_subtabs_audio.add_widget(Divider(draw_line=True), 0)
        layout_subtabs_audio.add_widget(Divider(draw_line=True), 1)
        layout_subtabs_audio.add_widget(Divider(draw_line=True), 2)
        layout_subtabs_audio.add_widget(Divider(draw_line=True), 3)
        layout_subtabs_audio.add_widget(Divider(draw_line=True), 4)
        layout_subtabs_audio.add_widget(Divider(draw_line=True), 5)
        layout_subtabs_audio.add_widget(Divider(draw_line=True), 6)
        layout_subtabs_audio.add_widget(Divider(draw_line=True), 7)
        layout_subtabs_audio.add_widget(Divider(draw_line=True), 8)

        # MANAGEMENT SUBTAB LAYOUT
        layout_subtabs_mgmt.add_widget(Button("USB UPDATE", self._vol_up), 0)
        layout_subtabs_mgmt.add_widget(VerticalDivider(), 1)
        layout_subtabs_mgmt.add_widget(Button("CLEAR CLI", self.clear_log), 2)
        layout_subtabs_mgmt.add_widget(VerticalDivider(), 3)
        layout_subtabs_mgmt.add_widget(VerticalDivider(), 4)
        layout_subtabs_mgmt.add_widget(VerticalDivider(), 5)
        layout_subtabs_mgmt.add_widget(CheckBox("DELETE", on_change=self._toggle_rbg, name="RGB"), 6)
        layout_subtabs_mgmt.add_widget(VerticalDivider(), 7)
        layout_subtabs_mgmt.add_widget(Button("KILL FACE", self.force_kill), 8)

        # DIVIDER SPACERS
        layout_subtabs_mgmt.add_widget(Divider(draw_line=True), 0)
        layout_subtabs_mgmt.add_widget(Divider(draw_line=True), 1)
        layout_subtabs_mgmt.add_widget(Divider(draw_line=True), 2)
        layout_subtabs_mgmt.add_widget(Divider(draw_line=True), 3)
        layout_subtabs_mgmt.add_widget(Divider(draw_line=True), 4)
        layout_subtabs_mgmt.add_widget(Divider(draw_line=True), 5)
        layout_subtabs_mgmt.add_widget(Divider(draw_line=True), 6)
        layout_subtabs_mgmt.add_widget(Divider(draw_line=True), 7)
        layout_subtabs_mgmt.add_widget(Divider(draw_line=True), 8)

        layout1.add_widget(VerticalDivider(), 1)
        self.register_faces(animations_path='../animations.json', layout=layout1)

        self.fix()
        self.save()

        self.audio = True
        self.loop = False
        self.rgb = False
        sleep(1)
        self.default_face()

    # SWITCH LAYOUTS FUNC
    def _disable(self, new_menu: int) -> None:
        # Disable all widgets in current menu - this had +1 but not sure why?
        for widget in self.layouts[self.current_menu].widgets:
            widget.disabled = True
        self.save()

        # Enable all widgets in new menu  - this said True but meant False?
        for widget in self.layouts[new_menu].widgets:
            widget.disabled = False
        self.save()
        self.current_menu = new_menu

    def register_faces(self, animations_path: str, layout: Layout, root="./led-image-viewer", path="~/rasputin/faces/"):
        with open(animations_path, 'r') as json_file:
            animations = json.load(json_file)
        for button_name in animations:
            metadata = animations[button_name]
            assert isinstance(metadata['filename'], str) and isinstance(metadata['speed'], int)  # So linter is happy
            register_animation(layout,
                               button_name,
                               metadata['column'],
                               partial(self.render_face, animation=metadata['filename'], speed=metadata['speed'],
                                       root=root, path=path))

    def register_palette(self, palette_path='../jsons/palettes.json') -> None:
        with open(palette_path, 'r') as json_file:
            palettes = json.load(json_file)
        for key in palettes:
            palette_info = palettes[key]
            self.palette[key] = [palette_info['foreground_color'],
                                 palette_info['attribute'],
                                 palette_info['background_color']]

    def process_event(self, event: Event) -> [None | Event]:
        if self.active_camera or self.active_face:
            sleep(0)  # Context switch if necessary
        return super().process_event(event)

    def exit_event(self) -> None:
        self.end_current_face()
        self.log("Goodbye!")
        sleep(0.1)
        sys.exit(0)

    def log(self, text: str) -> None:
        self.console.value += f"${{7,1}} {text}\n"

    def clear_log(self) -> None:
        self.console.value = None

    def _toggle_rbg(self) -> None:
        self.rgb = not self.rgb

    def _toggle_loop(self) -> None:
        self.loop = not self.loop

    def _toggle_audio(self) -> None:
        self.audio = not self.audio
        self.vol = 0 if self.vol >= 0 else 5000

    def _vol_up(self) -> None:
        if not self.audio:
            self.log("Audio currently muted")
        else:
            if not self.vol >= 20000:
                self.vol += 250
            self.log(f"Volume: {self.vol}")

    def _vol_down(self) -> None:
        if not self.audio:
            self.log("Audio currently muted")
        else:
            if 0 >= self.vol:
                self.vol -= 250
            self.log(f"Volume: {self.vol}")

    def _play_audio_random(self):
        length = randint(1, 3)

        if self.audio:
            match length:
                case 1:
                    self._play_audio_short()
                case 2:
                    self._play_audio_med()
                case  3:
                    self._play_audio_long()

    def _play_audio_short(self):
        if self.audio:
            cmd = self.format_audio_command(self.vol, 'talk_short', num_files=2)
            self.log(f"> {cmd}")
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _play_audio_med(self):
        if self.audio:
            cmd = self.format_audio_command(self.vol, 'talk_med', num_files=4)
            self.log(f'> {cmd}')
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _play_audio_long(self):
        if self.audio:
            cmd = self.format_audio_command(self.vol, 'talk_long', num_files=2)
            self.log(f'> {cmd}')
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _play_audio_name(self):
        if self.audio:
            cmd = self.format_audio_command(self.vol, 'ya_rasputin', num_files=None)
            self.log(f'> {cmd}')
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    def format_audio_command(volume: int, filename: str, num_files=None, base_dir="/home/admin/rasputin/sounds/"):
        if num_files is not None:
            audio_number = randint(1, num_files)
            filename = f"{filename}{audio_number}"
        return f"mpg123 -a 2 -f {volume} {base_dir}/{filename}.mp3 &"

    def _pair_bluetooth_speaker(self):
        self.log("> ./bt_speaker.sh")
        proc = subprocess.run('./bt_speaker.sh', shell=True, capture_output=True, text=True)
        self.log(proc.stdout)  # Was there a reason that you were not just logging this?

    @staticmethod
    def format_face_command(root_dir: str, speed: int, loop=True) -> str:
        base_cmd = f'{root_dir} --led-slowdown-gpio=4 --led-gpio-mapping=adafruit-hat --led-brightness=100' \
                   f'--led-cols=128 --led-rows=32 -D" + {speed} '

        base_cmd += '--led-daemon' if loop else '-l1'
        return base_cmd

    @staticmethod
    def format_face_animation(filename: str, loop=True, rgb=True) -> str:
        if loop:
            filename = f"{filename}_loop"
        if rgb:
            filename = f'rgb_{filename}'
        return f'{filename}.gif'

    # FACES
    def render_face(self, anim: str, speed: int, root="./led-image-viewer", path="~/rasputin/faces/"):
        if self.rgb:
            speed -= 60

        face_command = self.format_face_command(root, speed, self.loop)
        animation = self.format_face_animation(path+anim, self.loop, self.rgb)

        if self.active_face:
            self.end_current_face()

        self.active_face = True
        self.log("> " + animation)
        subprocess.run(face_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if self.loop:
            self.active_face = True
        else:
            self.default_face()

    def force_kill(self):
        self.end_current_face()
        self.log("KILLED ACTIVE ANIM")

    def end_current_face(self):
        subprocess.run('pgrep -f led-image-viewe | sudo xargs kill -s SIGINT', shell=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        self.active_face = False

    def default_face(self):
        anim = "blink2.gif"
        speed = "50"
        cmd_root = "./led-image-viewer"
        cmd_path = " ~/rasputin/faces/"
        if self.rgb:
            anim = "rgb_" + anim
            speed = "10"
        if self.active_face:
            self.end_current_face()
        cmd = cmd_root + "--led-slowdown-gpio=4 --led-gpio-mapping=adafruit-hat --led-brightness=100 --led-cols=128 " \
                         "--led-rows=32 --led-daemon -D" + speed

        # end_current_face should reset active face
        self.active_face = True
        cmd = "sudo " + cmd + cmd_path + anim
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
