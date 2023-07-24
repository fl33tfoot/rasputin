#!/usr/bin/env python3

import json
import os
from pathlib import Path

'''Helper script to convert hard-coded animation files/speeds/columns to json.

Exports method to add new animations to json should you need to
'''

if __name__ == '__main__':

    out_dir = Path('../../jsons/')
    os.makedirs(out_dir, exist_ok=True)

    # Name: (filename, speed, column)
    button_names = ['Attention', 'Yes', 'No',
                    'Annoyed', 'Blink 2', 'Blink 3',
                    'Charging', 'Coffee', 'Cry',
                    'Dizzy', 'Error', 'Heart Eyes',
                    'Laugh', 'Load', 'Low Battery',
                    'Music', 'Happy', 'Sleep',
                    'Sorry', 'Vaporwave', 'Glitch',
                    'Ahegao', 'Sheesh', 'Ratio',
                    'Pacman', 'X Eyes', 'O Eyes',
                    'OwO', 'UwU', 'Big UwU',
                    'Big OwO']

    file_names = ['attention', 'yes', 'no',
                  'blink1', 'blink2', 'blink3',
                  'charging', 'coffee', 'cry',
                  'dizzy', 'error', 'heart',
                  'laugh', 'load', 'lowbattery',
                  'music', 'party', 'sleep',
                  'sorry', 'vapor', 'glitch',
                  'ahegao', 'sheesh', 'ratio',
                  'pacman', 'xeyes', 'oeyes',
                  'owo2', 'owo1', 'uwu2',
                  'uwu1']

    speeds = [75, 75, 75,
              60, 60, 60,
              80, 90, 70,
              90, 60, 70,
              85, 80, 80,
              70, 75, 120,
              65, 5000, 60,
              2000, 60, 30,
              50, 60, 60,
              120, 60, 120,
              60]

    animations = {}
    for i, name in enumerate(button_names):
        animation_metadata = {
            'filename': file_names[i],
            'speed': speeds[i],
            'column': (i % 3) + 2
        }

        animations[name] = animation_metadata

    with open(out_dir / 'animations.json', 'w') as json_file:
        json.dump(animations, json_file, indent=2)


def add_animation_to_json(name_: str, fname_: str, speed: int, filepath='../jsons/animations.json'):
    with open(filepath, 'rw') as file:
        animations_dict = json.load(file)
        num_entries = len(animations_dict.keys())
        metadata = {
            'filename': fname_,
            'speed': speed,
            'column': (num_entries % 3) + 1
        }

        animations_dict[name_] = metadata

        json.dump(animations_dict, file, indent=2)
