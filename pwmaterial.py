import re
import pandas as pd


# Material class
class Material:
    def __init__(self, name, coord_str):
        self.name = name
        self.coordinates = self.parse_coords(coord_str)
        self.id = self.generate_id(name)

    @staticmethod
    def parse_coords(coord_str):
        try:
            x_str, y_str = coord_str.split(" ")
            return (float(x_str), float(y_str))
        except Exception:
            return None

    @staticmethod
    def generate_id(name):
        # snake case, shortened version
        name = name.strip().lower()
        name = re.sub(r'\W+', '_', name)
        # shorten to max 10 chars for ID (optional)
        return name[:10]
    

# Load data & image
def parse_data_from_csv(csvfile="materials_coords.csv"):
    df = pd.read_csv(csvfile)
    materials = []

    for col in df.columns:
        for coord in df[col].dropna():
            mat = Material(name=col, coord_str=coord)
            if mat.coordinates:
                materials.append(mat)
    return materials
