import sys
from time import sleep

from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button, VerticalDivider, Divider, CheckBox

'''Unsure what these do atm, so currently just refactored into classes.
'''

# TODO: much of this code is duplicated code from other classes
#   once we figure out what they do, we should refactor and perhaps
#   abstract out these frames


class RasputinExtra(Frame):
    def __init__(self, screen, data):
        super().__init__(screen, screen.height, screen.width, data=data, can_scroll=False, has_border=True,
                         title="R4SPUT1N")

        # INITIAL COLOR CONFIGURATION
        self.palette['background'] = [0, Screen.A_BOLD, 0]
        self.palette['button'] = [7, Screen.A_BOLD, 0]
        self.palette['control'] = [7, Screen.A_BOLD, 0]
        self.palette['selected_control'] = [0, Screen.A_BOLD, 7]
        self.palette['field'] = [7, Screen.A_BOLD, 0]
        self.palette['selected_field'] = [0, Screen.A_BOLD, 7]
        self.palette['edit_text'] = [7, Screen.A_BOLD, 0]
        self.palette['focus_edit_text'] = [0, Screen.A_BOLD, 7]
        self.palette['focus_field'] = [7, Screen.A_BOLD, 0]
        self.palette['selected_focus_field'] = [0, Screen.A_BOLD, 7]
        self.palette['focus_button'] = [0, Screen.A_BOLD, 7]
        self.palette['focus_control'] = [0, Screen.A_BOLD, 7]
        self.palette['selected_focus_control'] = [0, Screen.A_BOLD, 7]
        self.palette['red'] = [1, Screen.A_BOLD, 0]
        self.palette['disabled'] = [7, Screen.A_BOLD, 0]
        self.palette['title'] = [3, Screen.A_BOLD, 0]
        self.palette['borders'] = [3, Screen.A_BOLD, 0]
        self.palette['label'] = [7, Screen.A_BOLD, 0]

        # FRAME LAYOUTS
        layout_tabs = Layout([19, 1, 19, 1, 19, 1, 19, 1, 20], fill_frame=False)
        layout_subtabs = Layout([19, 1, 19, 1, 19, 1, 19, 1, 20], fill_frame=False)
        layout_content = Layout([20, 20, 20, 20, 20], fill_frame=True)

        self.add_layout(layout_tabs)
        self.add_layout(layout_subtabs)
        self.add_layout(layout_content)

        # TABS LAYOUT
        layout_tabs.add_widget(Button("MAIN", self._volUp), 0)
        layout_tabs.add_widget(VerticalDivider(), 1)
        layout_tabs.add_widget(Button("EXTRA", self._volUp), 2)
        layout_tabs.add_widget(VerticalDivider(), 3)
        layout_tabs.add_widget(Button("AUDIO", self._volUp), 4)
        layout_tabs.add_widget(VerticalDivider(), 5)
        layout_tabs.add_widget(Button("MGMT", self._volUp), 6)
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

        # SUBTABS LAYOUT
        layout_subtabs.add_widget(Button("1", self._volUp), 0)
        layout_subtabs.add_widget(VerticalDivider(), 1)
        layout_subtabs.add_widget(Button("2", self._volDown), 2)
        layout_subtabs.add_widget(VerticalDivider(), 3)
        layout_subtabs.add_widget(CheckBox("3", on_change=self._toggleAudio, name="AUDIO"), 4)
        layout_subtabs.add_widget(VerticalDivider(), 5)
        layout_subtabs.add_widget(Button("4", self._volUp), 6)
        layout_subtabs.add_widget(VerticalDivider(), 7)
        layout_subtabs.add_widget(Button("5", self._volUp), 8)

        # DIVIDER SPACERS
        layout_subtabs.add_widget(Divider(draw_line=True), 0)
        layout_subtabs.add_widget(Divider(draw_line=True), 1)
        layout_subtabs.add_widget(Divider(draw_line=True), 2)
        layout_subtabs.add_widget(Divider(draw_line=True), 3)
        layout_subtabs.add_widget(Divider(draw_line=True), 4)
        layout_subtabs.add_widget(Divider(draw_line=True), 5)
        layout_subtabs.add_widget(Divider(draw_line=True), 6)
        layout_subtabs.add_widget(Divider(draw_line=True), 7)
        layout_subtabs.add_widget(Divider(draw_line=True), 8)

    # MAIN METHODS
    def exit_event(self):
        self.endCurrentFace()
        self.log("Goodbye!")
        sleep(0.1)
        sys.exit(0)

    def log(self, text):
        self.console.value += "${7,1}" + text + "\n"

    def clear_log(self):
        self.console.value = None
