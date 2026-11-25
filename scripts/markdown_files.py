import base64
import html
import json
import re
import zipfile
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

from programming_files import has_coordinates
from score import score_competition
from uls import base_callsign, ham_locations

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

Please don't hesitate to send us your thoughts and feedback, either by email (<span id="contact-email">enable JavaScript to see our email</span><script>(function(){var addr=["singlethink.net","matt"].reverse().join("@");var a=document.createElement("a");a.href="mailto:"+addr;a.textContent=addr;document.getElementById("contact-email").replaceWith(a);})();</script>) or on our [Discord server](https://discord.com/invite/mqkD4fTjrn).

<br />

## Contact Map

{{ pew_pew_map }}

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
        leaderboard, by_repeater, by_club, stats, contacts = score_competition(df)
        try:
            locations = ham_locations(set(contacts["Logger"]) | set(contacts["Callsign"]))
        except (OSError, zipfile.BadZipFile) as e:  # requests' errors are OSErrors too
            print(f"Skipping the contact map, couldn't look up station locations: {e}")
            locations = {}
        contact_map = pew_pew_map(df, contacts, locations)
        if contact_map:
            write_pew_pew_demo(contact_map)
        index_content = results_index_content  # write the results data to the index
    else:
        for file in Path("results").glob("*.md"):
            file.unlink()
        leaderboard = pd.DataFrame([0])
        by_club, by_repeater, stats, contact_map = "", "", "", ""
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
    index = index.replace("{{ pew_pew_map }}", contact_map)

    with open("index.md", "w") as f:
        f.write(index)


CONTEST_MINUTES = 48 * 60  # the Roundabout runs for 48 hours, Nov 14 00:00 to Nov 15 23:59


def _contact_minutes(contacts: pd.DataFrame) -> pd.Series:
    """Minutes into the contest (from its Nov 14 00:00 start) each contact happened, or 0 if undated."""
    if "Date" not in contacts.columns or "Time" not in contacts.columns:
        return pd.Series(0, index=contacts.index)
    # Logs mix "Nov 14"/"11/14/2026"/"14-Nov"/... dates and "0:00"/"1128"/"12:00 AM" times;
    # all-digit times come in as ints, so stringify and give HHMM a colon before parsing.
    time = contacts["Time"].astype(str).str.strip().str.replace(r"^(\d{1,2})(\d{2})$", r"\1:\2", regex=True)
    parsed = pd.to_datetime(contacts["Date"].astype(str) + " " + time, format="mixed", errors="coerce")
    # Count from Nov 14 of whatever year (if any) the log gave
    minutes = ((parsed.dt.day - 14) * 1440 + parsed.dt.hour * 60 + parsed.dt.minute).where(parsed.dt.month == 11)
    return minutes.fillna(0).clip(0, CONTEST_MINUTES - 1).astype(int)


def pew_pew_data(df: pd.DataFrame, contacts: pd.DataFrame, locations: dict[str, list[float]]) -> dict:
    """
    Build the pew pew map's data: every located station's legs to the repeaters it made contacts through.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    contacts : pd.DataFrame
        Every contact's Logger, contacted Callsign, and RR#, and optionally its Date and Time.
    locations : dict[str, list[float]]
        [lat, lon] of each located station, keyed by base callsign.

    Returns
    -------
    dict
        "repeaters" as [RR#, label, lat, lon], "stations" as [callsign, lat, lon, is participant],
        "links" as [callsign, RR#, number of contacts], "events" as [callsign, RR#, contest minute]
        (one per contact leg, for animating the map), and "contest_minutes" (the contest's length).
    """
    repeaters = {
        int(r["RR#"]): [int(r["RR#"]), f"RR# {r['RR#']} {r['Callsign']} ({r['Output (MHz)']})", *r["Coordinates"]]
        for _, r in df.loc[df["Coordinates"].map(has_coordinates)].iterrows()
    }
    # Logs spell the same station several ways ("K7DRQ ", "K7DRQ/M")
    contacts = contacts.assign(
        Logger=contacts["Logger"].map(base_callsign),
        Callsign=contacts["Callsign"].map(base_callsign),
        Minute=_contact_minutes(contacts),
    )
    events = sorted(
        [station, int(rr), int(minute)]
        for logger, call, rr, minute in contacts[["Logger", "Callsign", "RR#", "Minute"]].itertuples(index=False)
        for station in (logger, call)
        if station in locations and int(rr) in repeaters
    )
    links = Counter((station, rr) for station, rr, _ in events)
    participants = set(contacts["Logger"])
    return {
        "repeaters": [repeaters[rr] for rr in sorted({rr for _, rr in links})],
        "stations": [[s, *locations[s], s in participants] for s in sorted({s for s, _ in links})],
        "links": [[s, rr, n] for (s, rr), n in sorted(links.items())],
        "events": events,
        "contest_minutes": CONTEST_MINUTES,
    }


def pew_pew_map(df: pd.DataFrame, contacts: pd.DataFrame, locations: dict[str, list[float]]) -> str:
    """HTML for the pew pew map of contacts through repeaters, or an empty string if there's nothing to map."""
    data = pew_pew_data(df, contacts, locations)
    if not data["links"]:
        return ""
    # Base64 keeps log-sourced text from breaking out of the <script> or being read as Liquid/Markdown.
    encoded = base64.b64encode(json.dumps(data).encode()).decode()
    with open("assets/templates/pew_pew_map.html") as f:
        return f.read().replace("{{ pew_pew_data }}", encoded)


def write_pew_pew_demo(contact_map: str) -> None:
    """Write pew_pew_demo.html, a standalone page to preview the pew pew map in a browser without Jekyll."""
    leaflet = Path("_includes/leaflet.html").read_text()
    body = contact_map.replace("{% include leaflet.html %}", leaflet)
    Path("pew_pew_demo.html").write_text(
        f'<!DOCTYPE html>\n<html>\n<head><meta charset="utf-8"><title>Contact Map</title></head>\n'
        f"<body>\n{body}\n</body>\n</html>\n"
    )


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


def remove_df_footnotes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return dataframe with Mode column footnotes removed.
    """
    return df.assign(Mode=df["Mode"].str.replace(r"\[.+\]", "", regex=True))


def dstar_display_mode(config: dict | None) -> str:
    """
    Return how a DSTAR repeater's Mode should read on a markdown page.

    Parameters
    ----------
    config : dict, optional
        Settings loaded from assets/config.json. If "dstar_mode_label" names a different
        mode, DSTAR repeaters are shown as that label plus "DSTAR", e.g. "NBFM[^nbfm] + DSTAR".
        Otherwise they're shown as plain "DSTAR".
    """
    label = (config or {}).get("dstar_mode_label", "DSTAR")
    return f"{label} + DSTAR" if label != "DSTAR" else "DSTAR"


def write_repeaters_md(df: pd.DataFrame, config: dict | None = None) -> None:
    """
    Write the repeaters.md file.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    config : dict, optional
        Settings loaded from assets/config.json; see dstar_display_mode.
    """
    df = df.assign(Mode=df["Mode"].replace("DSTAR", dstar_display_mode(config)))

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
            .assign(
                **{
                    "Tone (Hz)": df["Tone (Hz)"].apply(lambda v: v if pd.notna(v) else ""),
                    "Internet access": df.apply(internet_access, axis=1),
                }
            )
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
                    "left",
                ],
            )
        )

    # Create a list of short-name-to-long-description mappings
    association_text = ""
    associations = df.groupby("Group Name")[["Long Name", "Website"]].first()
    for short, long, url in associations.to_records():
        link = f"[{text(long) or short}]({text(url)})" if text(url) else text(long) or short
        association_text += f"{short}\n: {link}\n\n"

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


def internet_access(r) -> str:
    """Return the internet access details when the repeater allows internet contacts and gives them, else ""."""
    details = cell(r.get("Internet Access"))
    return details if cell(r.get("Allow Internet Contacts")) == "Yes" else ""


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


def claim_slug(pages: dict, name: str, slug) -> str:
    """Record that group `name` owns page `slug` in `pages`, raising if it has none or another group has it."""
    if not isinstance(slug, str):
        raise ValueError(f"Group {name!r} has no Slug; add it to assets/clubs.csv")
    if slug in pages:
        raise ValueError(f"Groups {pages[slug]!r} and {name!r} would share the page groups/{slug}.md")
    pages[slug] = name
    return slug


def write_group_pages(
    df: pd.DataFrame, forms: dict, clubs: pd.DataFrame | None = None, config: dict | None = None
) -> None:
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
    clubs : pd.DataFrame, optional
        The clubs (Group Name, Long Name, Website, Slug). A club with no repeaters in df gets
        a page saying we don't have any for it yet.
    config : dict, optional
        Settings loaded from assets/config.json; see dstar_display_mode.
    """
    is_dstar = df["Mode"] == "DSTAR"
    df = df.assign(Mode=df["Mode"].replace("DSTAR", dstar_display_mode(config)))
    # Strip footnotes from genuine modes, but keep the DSTAR label's footnote (if any) intact.
    df.loc[~is_dstar, "Mode"] = remove_df_footnotes(df.loc[~is_dstar])["Mode"]

    with open("assets/templates/group.md") as f:
        template = f.read()
    with open("assets/templates/group_empty.md") as f:
        empty_template = f.read()

    pages, output = {}, {}
    for name, group in df.groupby("Group Name", sort=False):
        slug = claim_slug(pages, name, group["Slug"].iloc[0])

        long_name = text(group["Long Name"].iloc[0])
        website = text(group["Website"].iloc[0])

        conflicts = ""
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
                    # Send the real mode, not the display label (which may carry a footnote
                    # marker and/or a "+ DSTAR" suffix for DSTAR repeaters).
                    "Mode": "DSTAR" if is_dstar.loc[r.name] else text(r["Mode"]),
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
            template.replace("{{ title }}", json.dumps(long_name or name))
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

    if clubs is not None:
        for _, club in clubs[~clubs["Group Name"].isin(df["Group Name"])].iterrows():
            name = club["Group Name"]
            slug = claim_slug(pages, name, club["Slug"])
            website = text(club["Website"])
            output[slug] = (
                empty_template.replace("{{ title }}", json.dumps(text(club["Long Name"]) or name))
                .replace("{{ subtitle }}", json.dumps(f"Status of {name} repeaters"))
                .replace("{{ website }}", f"[{cell(website)}]({website})" if website else "")
                .replace("{{ add_form }}", prefill_url(forms["repeater"], {"Group Name": name, "Website": website}))
            )

    # Only replace the old pages once every new page has been built
    groups_dir = Path("groups")
    groups_dir.mkdir(exist_ok=True)
    for file in groups_dir.glob("*.md"):
        file.unlink()
    for slug, page in output.items():
        (groups_dir / f"{slug}.md").write_text(page)
