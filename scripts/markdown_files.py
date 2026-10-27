import html
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

from programming_files import has_coordinates
from score import score_competition

STATUS_RESPONSE_NEEDED = "response_needed"
STATUS_IN = "in"
STATUS_OUT = "out"
INTERNET_FIELDS = ["Allow Internet Contacts", "Internet Access"]
STATUS_LABELS = {STATUS_RESPONSE_NEEDED: "Response needed", STATUS_IN: "In", STATUS_OUT: "Out"}

ongoing_index_content = """
# Joining the Repeater Roundabout

To get started, check out the [Rules](./rules) page.

Then, check out the list of [{{ n_repeaters }} participating repeaters](./repeaters) from across {{ n_groups }} radio groups that you'll play on during the contest. You can also [view the map](./map) to see where the repeaters are located.

We provide [files to program your radios](./files) with Chirp and other software.

Visit the [logging page](./logging) to log your contacts and submit your logs for scoring.

Join our [Discord chat server](https://discord.com/invite/mqkD4fTjrn) to chat with other participants, arrange skeds, and get help.

"""  # noqa: E501


results_index_content = """
# Results

The contest is over ! Many thanks to those who participated; we hope you had fun. Check back next year for the next Repeater Roundabout !

Here are some stats on the contest, based on the logs received. These numbers are underestimates, because we are missing a good number of logs !

{{ stats }}

Please don't hesitate to send us your thoughts and feedback, either by email at [quentincaudron@gmail.com](mailto:quentincaudron@gmail.com) or on our [Discord server](https://discord.com/invite/mqkD4fTjrn).

<br />

## Leaderboard

Many congratulations to our winner, {{ winning_station }} ! This year, we have **personal results** for each contestant -- simply click on their names to see their score summary and logs.

{{ leaderboard }}

<br />

## Club Standings

These are the total number of activations on the repeaters belonging to each club, including duplicate contacts on the same repeater.

{{ club_standings }}

<br />

## Repeater Standings

This table shows how many contacts were made on each repeater, including duplicates. The Readability score is the average signal report across all reports for that repeater -- it's the number of the CM report, or the R in an RS(T) report.

{{ repeater_standings }}

"""  # noqa: E501


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
    df = df.copy()

    if score_results:
        leaderboard, by_repeater, by_club, stats = score_competition(df)
        index_content = results_index_content  # write the results data to the index
    else:
        for file in Path("results").glob("*.md"):
            file.unlink()
        leaderboard = pd.DataFrame([0])
        by_club, by_repeater, stats = "", "", ""
        index_content = ongoing_index_content  # write the ongoing contest text to the index

    now = datetime.now().strftime("%A %B %d at %H:%M")

    with open("assets/templates/index.md") as f:
        index = f.read()

    # Fill in the number of repeaters and the updated date
    index = index.replace("{{ index_content }}", index_content)
    index = index.replace("{{ date_updated }}", now)
    index = index.replace("{{ n_repeaters }}", str(len(df)))
    index = index.replace("{{ n_groups }}", str(df["Group Name"].nunique()))
    index = index.replace("{{ leaderboard }}", leaderboard.to_markdown())
    index = index.replace("{{ club_standings }}", by_club)
    index = index.replace("{{ repeater_standings }}", by_repeater)
    index = index.replace("{{ winning_station }}", str(leaderboard.iloc[0].get("Callsign")))
    index = index.replace("{{ stats }}", stats)

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
    with open("assets/templates/rules.md") as f:
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

    if df.empty:
        table = "We're confirming repeaters for this year's Repeater Roundabout.  Check back soon!"
    else:
        table = (
            df[table_cols]
            .rename(columns={"Group Name": "Group"})
            .assign(**{"Tone (Hz)": df["Tone (Hz)"].apply(lambda v: v if pd.notna(v) else "")})
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
    with open("assets/templates/repeaters.md") as f:
        maps = f.read()
    maps = maps.replace("{{ table }}", table)
    maps = maps.replace("{{ associations }}", association_text)
    with open("repeaters.md", "w") as f:
        f.write(maps)


def write_map_md(df: pd.DataFrame, threshold: float = 0.003) -> None:
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
    # Repeaters without known coordinates (e.g. imported without lat/long) can't be placed on the map
    df = df.loc[df["Coordinates"].map(has_coordinates)]

    # Hierarchically cluster repeater lat / long pairs; clustering needs at least two
    if len(df) > 1:
        coords = np.array(df["Coordinates"].to_list())
        allocations = fcluster(linkage(pdist(coords), method="complete"), threshold, criterion="distance")
    else:
        allocations = range(len(df))

    # Assign each repeater's info to a cluster
    clusters = defaultdict(list)
    for idx, allocation in enumerate(allocations):
        clusters[allocation].append(df.iloc[idx][["Callsign", "Output (MHz)", "Coordinates", "RR#"]].to_dict())

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
            custom_middle = (
                "\"<div class='icon-label'>...</div>\""
                if len(cluster) > 1
                else f"\"<div class='icon-label'>{repeater['RR#']}</div>\""
            )
            custom = f"L.divIcon({{className: 'custom-icon', html: {custom_middle}, iconSize: [25, 25]}})"
            pins_list.append(f"L.marker({coords_str}, {{icon: {custom} }}).bindPopup('{msg}').addTo(map);")
            # pins_list.append(f"L.marker({coords_str}).bindPopup('{msg}').addTo(map);")

    pins = "\n".join(pins_list)

    # Write the LeafletJS code to map templates
    with open("assets/templates/map.md") as f:
        maps_md = f.read()
    with open("assets/templates/map.html") as f:
        maps_html = f.read()

    maps_md = maps_md.replace("{{ repeater_pins }}", pins)
    maps_html = maps_html.replace("{{ repeater_pins }}", pins)

    with open("map.md", "w") as f:
        f.write(maps_md)
    with open("demo_map.html", "w") as f:
        f.write(maps_html)


def text(value) -> str:
    """Return value as a string, or "" if it is missing."""
    return "" if value is None or (np.isscalar(value) and pd.isna(value)) else str(value)


def cell(value) -> str:
    """Return value escaped for display in a markdown table cell."""
    return html.escape(text(value)).replace("|", "\\|")


def group_slug(name: str) -> str:
    """Return a URL-safe page name for a group: lowercase, with runs of other characters replaced by hyphens."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def prefill_url(form: dict, values: dict) -> str:
    """
    Return a link to a Google Form with answers filled in.

    form has the form's "url" and "fields", mapping a value name to the form's entry ID.
    Values with no entry ID or no content are left out.
    """
    answers = {form["fields"][k]: v for k, v in values.items() if k in form["fields"] and v}
    return form["url"] + "?" + urlencode({"usp": "pp_url", **answers})


def plain_tone(value) -> str:
    """Return a tone value with any trailing markdown footnote marker (e.g. "[^dcs]") removed."""
    return re.sub(r"\[\^\w+\]$", "", text(value))


def repeater_summary(r: pd.Series) -> str:
    """Return a one-line description of a repeater, e.g. "- WW7PSR 146.960- T103.5"."""
    offset, tone = text(r["Offset (MHz)"]), plain_tone(r["Tone (Hz)"])
    sign = "-" if offset.startswith("-") else "+" if offset else ""
    tone = f"T{tone}" if re.fullmatch(r"[\d.]+", tone) else tone
    return " ".join(filter(None, ["-", text(r["Callsign"]), text(r["Output (MHz)"]) + sign, tone]))


def repeaterbook_url(r: pd.Series) -> str:
    """Return the repeater's RepeaterBook page, or "" if it has no RepeaterBook ID."""
    if not text(r.get("RepeaterBook ID")):
        return ""
    state = text(r.get("RepeaterBook State ID")) or "53"  # WA
    return f"https://www.repeaterbook.com/repeaters/details.php?state_id={state}&ID={text(r['RepeaterBook ID'])}"


def write_group_pages(df: pd.DataFrame, forms: dict) -> None:
    """
    Write groups/<group>.md for each group, replacing any existing group pages.

    Each page lists all of the group's repeaters with their contest status, and links to
    the "group" form (to say which repeaters may be used) and the "repeater" form (to
    correct or add a repeater), filled in with what we know.

    Parameters
    ----------
    df : pd.DataFrame
        All repeaters, whatever their status, with RR# assigned.
    forms : dict
        The "group" and "repeater" forms, as accepted by prefill_url.
    """
    with open("assets/templates/group.md") as f:
        template = f.read()

    pages, output = {}, {}
    for name, group in df.groupby("Group Name", sort=False):
        slug = group_slug(name)
        if slug in pages:
            raise ValueError(f"Groups {pages[slug]!r} and {name!r} would share the page groups/{slug}.md")
        pages[slug] = name

        long_names = group["Long Name"].map(text).loc[lambda s: s != ""].unique()
        websites = group["Website"].map(text).loc[lambda s: s != ""].unique()
        website = websites[0] if len(websites) else ""

        conflicts = ""
        for field, values in [("names", long_names), ("websites", websites)]:
            if len(values) > 1:
                conflicts += f"> **Please check:** we have more than one of your group's {field}: "
                conflicts += "; ".join(cell(v) for v in values) + "\n\n"

        no_coords = group.loc[~group["Coordinates"].map(has_coordinates), ["Callsign", "Output (MHz)"]]
        if len(no_coords):
            conflicts += "> **Please check:** we don't have the location (coordinates) of: "
            conflicts += "; ".join(cell(f"{c} {f}") for c, f in no_coords.to_records(index=False))
            conflicts += ". Use the **Update** link to send it; until then it won't appear on the map.\n\n"

        rows = []
        for _, r in group.iterrows():
            correction = prefill_url(
                forms["repeater"],
                {
                    **{k: text(r[k]) for k in ["Callsign", "Output (MHz)", "Offset (MHz)", "Location"]},
                    "Tone (Hz)": plain_tone(r["Tone (Hz)"]),
                    **{k: text(r.get(k)) for k in INTERNET_FIELDS},
                    "Group Name": name,
                    "Website": text(r["Website"]),
                    "RepeaterBook": repeaterbook_url(r),
                    "Coordinates": ", ".join(str(c) for c in r["Coordinates"]) if isinstance(r["Coordinates"], list) else "",
                },
            )
            status = text(r.get("Status")) or STATUS_RESPONSE_NEEDED
            rows.append(
                {
                    "RR#": r["RR#"] if status == STATUS_IN else "",
                    **{k: cell(r[k]) for k in ["Callsign", "Location", "Mode", "Output (MHz)", "Offset (MHz)", "Tone (Hz)"]},
                    **{k: cell(r.get(k)) for k in INTERNET_FIELDS},
                    "Status": STATUS_LABELS[status],
                    "": f"[Update]({correction})",
                }
            )

        page = (
            template.replace("{{ title }}", json.dumps(long_names[0] if len(long_names) else name))
            .replace("{{ subtitle }}", json.dumps(f"Status of {name} repeaters"))
            .replace("{{ website }}", f"[{cell(website)}]({website})" if website else "")
            .replace("{{ conflicts }}", conflicts)
            .replace("{{ table }}", pd.DataFrame(rows).to_markdown(index=False, disable_numparse=True))
            .replace("{{ group_form }}", prefill_url(forms["group"], {
                "Group Name": name,
                "Repeaters": "\n".join(group.apply(repeater_summary, axis=1)),
            }))
            .replace("{{ add_form }}", prefill_url(forms["repeater"], {"Group Name": name, "Website": website}))
        )
        output[slug] = page

    # Only replace the old pages once every new page has been built
    groups_dir = Path("groups")
    groups_dir.mkdir(exist_ok=True)
    for file in groups_dir.glob("*.md"):
        file.unlink()
    for slug, page in output.items():
        (groups_dir / f"{slug}.md").write_text(page)
