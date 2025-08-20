import numpy as np
import matplotlib.pyplot as plt
from model.pwmaterial import parse_data_from_csv


def generate_route(mats, start_coords=None, N=20):
    """
    Generate a nearest-neighbor route of length N from mats starting at
    the closest point to start_coords (if given). Returns (route_coords, route_mats).

    Uses index-based selection to avoid float-equality issues and considers
    full Euclidean distance across both axes.
    """
    if not mats:
        return np.array([]), []

    # Ensure numeric array of shape (n, 2)
    coords = np.array([[float(m.coordinates[0]), float(m.coordinates[1])] for m in mats], dtype=float)

    # Determine starting index
    if start_coords is None:
        curr_idx = 0
    else:
        start_vec = np.array(start_coords, dtype=float)
        dists = np.linalg.norm(coords - start_vec, axis=1)
        curr_idx = int(np.argmin(dists))

    unvisited = list(range(len(mats)))
    route_indices = []

    steps = int(min(N, len(unvisited)))
    for _ in range(steps):
        route_indices.append(curr_idx)
        unvisited.remove(curr_idx)
        if not unvisited:
            break
        # Compute distances from current to all unvisited
        diffs = coords[unvisited] - coords[curr_idx]
        dists = np.linalg.norm(diffs, axis=1)
        next_pos = int(np.argmin(dists))
        curr_idx = unvisited[next_pos]

    route_coords = coords[route_indices]
    route_mats = [mats[i] for i in route_indices]

    return route_coords, route_mats


def plot_route_on_map(route_coords, map_image, offset=50):
    """
    Plot the route on the map image, zooming to the bounding box of route_coords + offset.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(map_image)

    # scatter route
    xs, ys = [], []
    for (x, y) in route_coords:
        xs.append((x + 9.6) * 10)
        ys.append((1113.2 - y) * 10)
    ax.plot(xs, ys, 'o-', color="blue")

    # bounding box + offset
    if xs and ys:
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        ax.set_xlim(min_x - offset, max_x + offset)
        ax.set_ylim(max_y + offset, min_y - offset)  # y is inverted in images

    ax.axis("off")
    plt.tight_layout()
    plt.show()
