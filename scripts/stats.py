from types import SimpleNamespace

import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import pdist, squareform
from shapely.geometry import Polygon

from programming_files import BAND_DEFINITIONS
from update import generate_repeater_df

args = SimpleNamespace(regen=True)


def band(freq: float) -> str:
    """
    Map between frequency and band name.

    Parameters
    ----------
    freq : float
        The repeater's output frequency.

    Returns
    -------
    str
        The name of the amateur radio band.
    """

    for band_name, edges in BAND_DEFINITIONS.items():
        if edges[0] < freq < edges[1]:
            return band_name

    return "other"


if __name__ == "__main__":

    statistics = {}

    # Generate the complete repeater dataframe with a band column
    df = generate_repeater_df(args)
    df["Band"] = df["Output (MHz)"].astype(float).apply(band)

    # How many repeaters are in each band ?
    statistics["Band stats"] = df["Band"].value_counts()

    # Find the center of mass of the repeater locations
    repeater_coords = np.array(df["Coordinates"].tolist())
    center_of_mass = repeater_coords.mean(0)
    statistics["Center of mass"] = center_of_mass

    # Find the convex hull of the repeater locations
    hull = ConvexHull(repeater_coords)
    hull_x, hull_y = (
        repeater_coords[hull.vertices, 0],
        repeater_coords[hull.vertices, 1],
    )

    # Grab the spatial extent's centroid
    poly = Polygon(zip(hull_y, hull_x))  # note the order
    xx, yy = poly.exterior.coords.xy
    centroid = poly.centroid
    statistics["Centroid"] = [centroid.y, centroid.x]

    # Transform the lat / long coordinates into a spatial frame
    gdf = gpd.GeoDataFrame(geometry=[poly]).set_crs(epsg=4326).to_crs("EPSG:5070")
    statistics["Area (square miles)"] = gdf.area[0] * 0.386102 / 1e6  # area in square miles
    statistics["Area (% of state)"] = statistics["Area (square miles)"] / 71362 * 100

    # Generate a plot of the convex hull
    plt.figure(figsize=(7, 12))
    plt.scatter([center_of_mass[1]], [center_of_mass[0]], marker="x", color="red")
    plt.scatter([centroid.x], [centroid.y], marker="o", color="blue")
    plt.plot(xx, yy, color="black")
    plt.savefig("hull.pdf")
    plt.close()

    # Load the clustered repeater locations from the map, rather than the individual
    # repeater locations; several exist in exactly the same location
    with open("map.md", "r") as f:
        locations = f.readlines()
    locations = [line for line in locations if line.strip().startswith("L.marker")]
    coords = np.array(
        [np.fromstring(line.split("[")[1].split("]")[0], sep=", ") for line in locations]
    )

    # Transform to spatial frame of reference and compute the distance matrix
    trans = (
        gpd.GeoDataFrame(geometry=gpd.points_from_xy(coords[:, 1], coords[:, 0]))
        .set_crs("EPSG:4326")
        .to_crs("EPSG:5070")
    )
    dist = squareform(pdist([[i.x, i.y] for i in trans["geometry"].tolist()]))

    # Compute an approximate TSP solution
    graph = nx.from_numpy_matrix(dist)
    path = nx.approximation.traveling_salesman_problem(graph, cycle=False)

    # Plot the TSP solution and calculate its path length
    path_distance = 0
    plt.figure(figsize=(7, 12))
    for i, j in zip(path[:-1], path[1:]):
        path_distance += dist[i, j]
        plt.plot([coords[i, 1], coords[j, 1]], [coords[i, 0], coords[j, 0]], "k-")

    plt.savefig("tsp.pdf")
    plt.close()
    statistics["TSP distance"] = path_distance / 1000 * 0.621371  # in miles

    # Print some metrics
    for key, val in statistics.items():
        print(f"{key} : {val}\n")
    # print(
    #     f"Area : {footprint_area:.0f} square miles ({footprint_area / 71362:.1%} of the State)."
    # )
    # print(f"TSP distance : {d / :1f} miles")
