# Create and activate a new virtual environment
python3 -m venv pw_map_env
source pw_map_env/bin/activate  # On Windows use: pw_map_env\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install pandas matplotlib pillow streamlit plotly streamlit-plotly-events time
