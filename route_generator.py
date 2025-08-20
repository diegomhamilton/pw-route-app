import numpy as np
import matplotlib.pyplot as plt
from model.pwmaterial import parse_data_from_csv


def generate_route(mats, start_coords=None, N=20):
    """
    Generate a route of length N from mats starting at start_coord (if given).
    Returns (route_coords, route_mats).
    """
    coordinates = np.array([m.coordinates for m in mats])

    # pick start point
    if start_coords is None:
        curr_mat = coordinates[0]
    else:
        # find closest coordinate to given start_coord
        dists = np.linalg.norm(coordinates - np.array(start_coords), axis=1)
        curr_mat = coordinates[np.argmin(dists)]

    remaining_coordinates = coordinates.copy()
    route_coords = []

    while N > 0 and len(remaining_coordinates) > 0:
        route_coords.append(curr_mat)

        # remove current from remaining
        mask = ~np.all(remaining_coordinates == curr_mat, axis=1)
        remaining_coordinates = remaining_coordinates[mask]

        if len(remaining_coordinates) == 0:
            break

        # choose next closest
        dists = np.linalg.norm(remaining_coordinates - curr_mat, axis=1)
        next_idx = np.argmin(dists)
        curr_mat = remaining_coordinates[next_idx]

        N -= 1

    # Get mats in the same order as route_coords
    route_mats = [
        m for rc in route_coords for m in mats if np.array_equal(m.coordinates, rc)
    ]

    return np.array(route_coords), route_mats


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
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    ax.set_xlim(min_x - offset, max_x + offset)
    ax.set_ylim(max_y + offset, min_y - offset)  # y is inverted in images

    ax.axis("off")
    plt.tight_layout()
    plt.show()
