import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import random
from model.pwmaterial import parse_data_from_csv
from route_generator import generate_route


def xy_to_pixel(x, y):
    pixelX = (x + 9.6) * 10
    pixelY = (1113.2 - y) * 10
    return pixelX, pixelY


# Load data & image
@st.cache_data
def load_data():
    materials = parse_data_from_csv("support_files/materials_coords.csv")
    map_img = Image.open("support_files/map.jpg")
    return materials, map_img


def map_fig(map_image):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(map_image)
    return fig, ax


materials, map_img = load_data()

# Streamlit UI
st.title("Material Route Viewer")

# Sidebar filters
unique_names = sorted(list(set(mat.name for mat in materials)))
selected_names = st.sidebar.multiselect(
    "Select Materials to Display (all tiers):",
    unique_names,
    default=unique_names
)

# Route parameters
st.sidebar.subheader("Route Parameters")
n_mats = st.sidebar.number_input("Number of Materials", value=20, min_value=2, max_value=50)

# Start coordinates (optional)
st.sidebar.subheader("Start Coordinates")
start_x = st.sidebar.number_input("Start X", value=None, step=1.0)
start_y = st.sidebar.number_input("Start Y", value=None, step=1.0)

# Arrow toggle
show_arrows = st.sidebar.checkbox("Show Route Arrows", value=True)

# Zoom toggle
zoom = st.sidebar.checkbox("Zoom Route View", value=True)

# Filter materials
filtered_materials = [m for m in materials if m.name in selected_names]

# Determine start material and coordinates
if start_x is None or start_y is None:
    start_mat = random.choice(filtered_materials)
    start_coords = start_mat.coordinates
else:
    start_coords = (start_x, start_y)
    start_mat = None  # no highlight if user sets manually

# Markers for different materials
markers = ['X', 'o', 's', '^', 'v', 'P', '*', 'D', '<', '>']
marker_map = {name: markers[i % len(markers)] for i, name in enumerate(unique_names)}


# Plotting function
def plot_route(route_mats, map_image, show_arrows=False, zoom=True):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'cyan', 'magenta']
    color_map = {name: colors[i % len(colors)] for i, name in enumerate(unique_names)}
    fig, ax = map_fig(map_image=map_image)

    # Plot materials with optional labels
    for mat in route_mats:
        px, py = xy_to_pixel(*mat.coordinates)
        size = 12 if mat == start_mat else 8
        ax.scatter(px, py, c=color_map[mat.name], marker=marker_map[mat.name],
                   s=size, label=mat.name)

    # Arrows between consecutive mats including last → first
    if show_arrows and len(route_mats) > 1:
        for i in range(len(route_mats)):
            curr_mat = route_mats[i]
            next_mat = route_mats[(i + 1) % len(route_mats)]
            x1, y1 = xy_to_pixel(*curr_mat.coordinates)
            x2, y2 = xy_to_pixel(*next_mat.coordinates)
            ax.annotate(
                '',
                xy=(x2, y2), xycoords='data',
                xytext=(x1, y1), textcoords='data',
                arrowprops=dict(arrowstyle="->", color="black", lw=1),
            )

    # Legend in markdown format
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))

    if len(unique) <= 4:
        ncol = 1
    else:
        ncol = int(np.ceil(len(unique) / 4))  # 4 rows

    ax.legend(
        unique.values(),
        unique.keys(),
        fontsize='small',
        loc='upper right',
        ncol=ncol,
        frameon=True
    )

    # Zoom to route bounding box
    if zoom and route_mats:
        xs, ys = zip(*[xy_to_pixel(*m.coordinates) for m in route_mats])
        offset = 100
        ax.set_xlim(min(xs) - offset, max(xs) + offset)
        ax.set_ylim(max(ys) + 2*offset, min(ys) - offset)

    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig)


# Generate route
route_coords, route_mats = generate_route(
    mats=filtered_materials,
    start_coords=start_coords,
    N=n_mats
)

# Plot
plot_route(route_mats, map_img, show_arrows=show_arrows, zoom=zoom)