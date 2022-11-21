from collections import defaultdict
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

from score import score_competition

index_content = """
# Joining the Repeater Roundabout

To get started, check out the [Rules](./rules) page. 

Then, check out the list of [{{ n_repeaters }} participating repeaters](./repeaters) from across {{ n_groups }} radio groups that you'll play on during the contest. You can also [view the map](./maps) to see where the repeaters are located.

We provide [files to program your radios](./files) with Chirp and other software.

Visit the [logging page](./logging) to log your contacts and submit your logs for scoring.

Join our [Discord chat server](https://discord.gg/Hss7YNRj) to chat with other participants, arrange skeds, and get help.
"""


results_index_content = """
# Leaderboard

Many congratulations to our winner, {{ winning_station }} ! The leaderboard is now closed.

{{ leaderboard }}

# Club Standings

{{ club_standings }}

# Repeater Standings

{{ repeater_standings }}
"""


def write_index_md(df: pd.DataFrame, score_results: bool = False) -> None:
    """
    Write the index.md file.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    score_reults: bool
        Whether the contest is over and we should write the results to the index page.
        If not, we write the normal index page with just some helpful info.
    """

    if score_results:
        leaderboard, by_club, by_repeater = score_competition(df)

    now = datetime.now().strftime("%A %B %d at %H:%M")

    with open("assets/templates/index.md", "r") as f:
        index = f.read()

    # Fill in the number of repeaters and the updated date
    index = index.replace("{{ index_content }}", index_content)
    index = index.replace("{{ date_updated }}", now)
    index = index.replace("{{ n_repeaters }}", str(len(df)))
    index = index.replace("{{ n_groups }}", str(df["Group Name"].nunique()))

    with open("index.md", "w") as f:
        f.write(index)


def write_rules_md(df: pd.DataFrame) -> None:
    """
    Write the rules.md file.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    """

    with open("assets/templates/rules.md", "r") as f:
        rules = f.read()

    # Fill in the number of repeaters and the updated date
    rules = rules.replace("{{ n_repeaters }}", str(len(df)))
    rules = rules.replace("{{ n_groups }}", str(df["Group Name"].nunique()))

    with open("rules.md", "w") as f:
        f.write(rules)


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
    table = (
        df[table_cols]
        .rename(columns={"Group Name": "Group"})
        .to_markdown(
            index=False,
            disable_numparse=True,
            colalign=[
                "left",
                "left",
                "left",
                "left",
                "left",
                "right",
                "right",
                "right",
            ],
        )
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
    allocations = fcluster(linkage(dist, method="complete"), threshold, criterion="distance")

    # Assign each repeater's info to a cluster
    clusters = defaultdict(list)
    for idx, allocation in enumerate(allocations):
        clusters[allocation].append(
            df.iloc[idx][["Callsign", "Output (MHz)", "Coordinates", "RR#"]].to_dict()
        )

    # For each cluster, create a pin on the map as LeafletJS plaintext
    pins_list = []
    for cluster in clusters.values():

        msg = ""
        for repeater in cluster:
            msg += f"RR# {repeater['RR#']} - {repeater['Callsign']} "
            msg += f"({repeater['Output (MHz)']})<br>"

        if len(msg):
            coords = np.mean([repeater["Coordinates"] for repeater in cluster], axis=0)
            coords_str = f"[{coords[0]:.10f}, {coords[1]:.10f}]"
            pins_list.append(f"L.marker({coords_str}).bindPopup('{msg}').addTo(map);")

    pins = "\n".join(pins_list)

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
