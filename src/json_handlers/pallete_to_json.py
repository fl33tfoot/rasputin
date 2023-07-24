import json
from asciimatics.screen import Screen
from pathlib import Path

if __name__ == "__main__":
    BOLD = Screen.A_BOLD  # integer, not sure why it's not enum but not my library
    out_dir = Path('../../jsons')

    keys = [
        'background', 'button', 'control',
        'selected_control', 'field', 'selected_field',
        'edit_text', 'focus_edit_text', 'focus_field',
        'selected_focus_field', 'focus_button', 'focus_control',
        'selected_focus_control', 'red', 'disabled',
        'title', 'borders', 'label'
    ]

    foreground_colors = [
        0, 7, 7,
        0, 7, 0,
        7, 0, 7,
        0, 0, 0,
        0, 1, 7,
        3, 3, 7
    ]

    attributes = [
        BOLD, BOLD, BOLD,
        BOLD, BOLD, BOLD,
        BOLD, BOLD, BOLD,
        BOLD, BOLD, BOLD,
        BOLD, BOLD, BOLD,
        BOLD, BOLD, BOLD
    ]

    background_colors = [
        0, 0, 0,
        7, 0, 7,
        0, 7, 0,
        7, 7, 7,
        7, 0, 0,
        0, 0, 0
    ]

    palettes = {}
    for i, key in enumerate(keys):
        palette_info = {
            'foreground_color': foreground_colors[i],
            'attribute': attributes[i],
            'background_color': background_colors[i]
        }

        palettes[key] = palette_info

    with open(out_dir / 'palettes.json', 'w') as json_file:
        json.dump(palettes, json_file, indent=2)


def add_palette_to_json(name_: str, foreground_color: int, attribute: int,
                        background_color: int, filepath='../jsons/palettes.json'):
    with open(filepath, 'rw') as file:
        palettes_ = json.load(file)
        info = {
            'foreground_color': foreground_color,
            'attribute': attribute,
            'background_color': background_color
        }

        palettes_[name_] = info

        json.dump(palettes_, file, indent=2)
