from collections import defaultdict
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist


def write_index_md(df: pd.DataFrame) -> None:
    """
    Write the index.md file.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    """

    now = datetime.now().strftime("%A %B %d at %H:%M")

    with open("assets/templates/index.md", "r") as f:
        index = f.read()

    # Fill in the number of repeaters and the updated date
    index = index.replace("{{ n_repeaters }}", str(len(df)))
    index = index.replace("{{ date_updated }}", now)
    index = index.replace("{{ n_groups }}", str(df["Group Name"].nunique()))

    with open("index.md", "w") as f:
        f.write(index)


def write_repeaters_md(df: pd.DataFrame) -> None:
    """
    Write the repeaters.md file.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    """

    # Create the main markdown table
    table_cols = [
        "RR#",
        "Group Name",
        "Callsign",
        "Location",
        "Mode",
        "Output (MHz)",
        "Offset (MHz)",
        "Tone (Hz)",
    ]
    table = df[table_cols].to_markdown(
        index=False,
        disable_numparse=True,
        colalign=["left", "left", "left", "left", "left", "right", "right", "right"],
    )

    # Create a list of short-name-to-long-description mappings
    association_text = ""
    associations = df.groupby("Group Name")[["Long Name", "Website"]].first()
    for short, long, url in associations.to_records():
        association_text += f"{short}\n: [{long}]({url})\n\n"

    # Write the markdown file from template
    with open("assets/templates/repeaters.md", "r") as f:
        maps = f.read()
    maps = maps.replace("{{ table }}", table)
    maps = maps.replace("{{ associations }}", association_text)
    with open("repeaters.md", "w") as f:
        f.write(maps)


def write_map_md(df: pd.DataFrame, threshold: float = 0.03) -> None:
    """
    Write the map.md file.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    threshold : float, optional
        Repeaters are combined into a single pin if less
        than this distance apart, by default 0.03.
    """

    # Hierarchically cluster repeater lat / long pairs
    coords = np.array(df["Coordinates"].to_list())
    dist = pdist(coords)
    allocations = fcluster(
        linkage(dist, method="complete"), threshold, criterion="distance"
    )

    # Assign each repeater's info to a cluster
    clusters = defaultdict(list)
    for idx, allocation in enumerate(allocations):
        clusters[allocation].append(
            df.iloc[idx][["Callsign", "Output (MHz)", "Coordinates"]].to_dict()
        )

    # For each cluster, create a pin on the map as LeafletJS plaintext
    pins = []
    for cluster in clusters.values():

        msg = ""
        for repeater in cluster:
            msg += f"{repeater['Callsign']} {repeater['Output (MHz)']}<br>"

        if len(msg):
            coords = np.mean([repeater["Coordinates"] for repeater in cluster], axis=0)
            coords = f"[{coords[0]:.10f}, {coords[1]:.10f}]"
            pins.append(f"L.marker({coords}).bindPopup('{msg}').addTo(map);")

    pins = "\n".join(pins)

    # Write the LeafletJS code to map templates
    with open("assets/templates/map.md", "r") as f:
        maps_md = f.read()
    with open("assets/templates/map.html", "r") as f:
        maps_html = f.read()

    maps_md = maps_md.replace("{{ repeater_pins }}", pins)
    maps_html = maps_html.replace("{{ repeater_pins }}", pins)

    with open("map.md", "w") as f:
        f.write(maps_md)
    with open("demo_map.html", "w") as f:
        f.write(maps_html)
