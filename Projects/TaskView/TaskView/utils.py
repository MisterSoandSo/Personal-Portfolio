import json
from typing import Tuple
from dataclasses import dataclass, field

def read_json_tasks(json_path):
    """
    Reads a JSON file and returns a list of (task, status) tuples.

    Parameters:
        json_path (str): Path to the JSON file.

    Returns:
        list of tuple: Each tuple contains (task, status) from the JSON objects.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    return [(task["task"], task["status"]) for task in tasks]

@dataclass
class ChecklistStyle:
    theme: str = "dark"  # or "light"
    font_path: str = "DejaVuSansMono.ttf"
    font_size: int = 20
    row_height: int = 36
    padding_x: int = 20
    padding_y: int = 20
    col_padding: int = 40
    bg_color: Tuple[int, int, int] = field(init=False)
    text_color: Tuple[int, int, int] = field(init=False)
    line_color: Tuple[int, int, int] = field(init=False)

    def __post_init__(self):
        if self.theme == "light":
            self.bg_color = (255, 255, 255)       # White background
            self.text_color = (30, 30, 30)        # Dark gray text
            self.line_color = (180, 180, 180)     # Light gray lines
        else:
            self.bg_color = (24, 24, 24)          # Dark background
            self.text_color = (240, 240, 240)     # Light text
            self.line_color = (80, 80, 80)        # Dark lines