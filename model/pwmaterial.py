import re
import json
import pandas as pd
from typing import List, Tuple, Optional


# Material class
class Material:
    def __init__(self, name: str, coordinates: Tuple[float, float], description: Optional[str] = None, tier: Optional[str] = None):
        self.name = name
        self.description = description
        self.tier = tier
        self.coordinates = coordinates
        self.id = self.generate_id(name)

    @staticmethod
    def generate_id(name):
        # snake case, shortened version
        name = name.strip().lower()
        name = re.sub(r'\W+', '_', name)
        # shorten to max 10 chars for ID (optional)
        return name[:10]


def _parse_coord_any(coord) -> Optional[Tuple[float, float]]:
    """
    Accepts [x,y], (x,y), or strings like "x y" or "x,y". Supports comma decimal.
    """
    if isinstance(coord, (list, tuple)) and len(coord) == 2:
        try:
            return float(str(coord[0]).replace(',', '.')), float(str(coord[1]).replace(',', '.'))
        except Exception:
            return None
    if isinstance(coord, str):
        nums = re.findall(r'[-+]?\d+(?:[.,]\d+)?', coord)
        if len(nums) >= 2:
            try:
                return float(nums[0].replace(',', '.')), float(nums[1].replace(',', '.'))
            except Exception:
                return None
    return None


# New: Load materials from JSON structured by category -> tier -> items
# Each item: { name, description, coordinates: [[x,y], ...] }

def parse_data_from_json(jsonfile: str = "support_files/materials.json", category: str = "Materiais") -> List[Material]:
    with open(jsonfile, 'r', encoding='utf-8') as f:
        data = json.load(f)

    mats: List[Material] = []
    cat = data.get(category, {}) if isinstance(data, dict) else {}
    if not isinstance(cat, dict):
        return mats

    for tier, items in cat.items():
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get('name')
            if not name:
                continue
            description = item.get('description')
            coords_list = item.get('coordinates') or []
            for c in coords_list:
                parsed = _parse_coord_any(c)
                if parsed:
                    mats.append(Material(name=name, coordinates=parsed, description=description, tier=tier))
    return mats


# Deprecated: kept only to avoid import errors elsewhere.
# Use parse_data_from_json instead.

def parse_data_from_csv(csvfile: str = "support_files/materials_coords.csv"):
    raise RuntimeError(
        "CSV input is deprecated. Please provide a JSON file and call parse_data_from_json()."
    )
