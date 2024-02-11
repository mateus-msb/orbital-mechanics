import json, os
from typing import Literal

def get_solar_system_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    json_file_path = os.path.join(parent_dir, "solar_system.json")
    with open(json_file_path, "r") as file:
        solar_system_data = json.load(file)
    return solar_system_data

CentralBody = Literal['Sun','Mercury', 'Venus', 'Earth', 'Moon', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']