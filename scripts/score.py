import re
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

from programming_files import band


def at_least_three_decimals(frequency: float) -> str:
    """
    Turn a frequency into a string with at least three decimal places.
    147.96 -> "147.960"
    444.5625 -> "444.5625"

    Parameters
    ----------
    frequency : float
        The frequency as a float.

    Returns
    -------
    str
        The frequency as a string, with at least three decimal places
        including trailing zeros.
    """

    frequency_str = f"{frequency:.4f}"
    if frequency_str.endswith("0"):
        return frequency_str[:-1]
    return frequency_str


def signal_report_to_readability(report: str) -> Optional[int]:
    """
    A rough interpretation of signal reports into numerical values.

    For circuit merit reports, we just return the number of the report.
    For RST reports, we return the Readability component.

    Parameters
    ----------
    report : str
        A user's signal report, such as "CM4" or "59".

    Returns
    -------
    Optional[int]
        The readability of a signal report, or None if it couldn't be interpreted.
    """

    report = report.upper().strip().replace("?", "")

    # Will match CM4, CM5+, CM3.5, CM4.5+
    is_cm = re.fullmatch(
        r"""
            ^
            (?:CM)?  # starts with "CM"
            [- ]?  # optional hyphen ( "CM-4" ) or space ( "CM 4" )
            ([1-5])  # followed by a number from 1 to 5 -- this is what we return
            \+?  # optionally followed by a plus sign ( CM5+ )
            (?:.\d)?  # optionally followed by a decimal and a number ( CM4.5 )
            $
        """,
        report,
        flags=re.VERBOSE,
    )

    # Will match 59, 59+, 4-9, 3x5, 5-9+
    is_rst = re.fullmatch(
        r"""
            ^
            ([1-5])  # a number from 1 to 5 -- this is what we return
            [-xX/]?  # optionally followed by an x, a dash, or a slash ( 5x9, 4-9, 3/5 )
            (?:\ by\ )?  # optionally followed by " by " ( 5 by 9 )
            [1-9]  # followed by a number from 1 to 9, which we throw away
            \+?  # optionally followed by a plus sign ( 59+ )
            $
        """,
        report,
        flags=re.VERBOSE,
    )

    if is_cm:
        return int(is_cm.group(1))
    if is_rst:
        return int(is_rst.group(1))

    print(f"Unable to parse '{report}'.")
    return None  # if no match, return None


def write_personal_results_md(logs: pd.DataFrame, summary: dict, callsign: str) -> None:

    # Read the template
    with open("assets/templates/personal_results.md", "r") as f:
        template = f.read()

    # Clean up the logs for table formatting
    logs = logs.drop(columns=["Logger"]).rename(
        columns={"Signal Report": "Report", "Group Name": "Group", "Bandhog": "Band Hog"}
    )
    logs = logs[["Group", "Contact", "Report", "Band", "QRP", "Club Connaisseur", "Band Hog", "QSO Score"]]
    for col in ["QRP", "Club Connaisseur", "Band Hog"]:
        logs[col] = logs[col].apply(lambda x: "X" if x else "")

    # Format the summary table
    total_score = summary["Total Score"]
    summary_df = pd.DataFrame(
        index=summary.keys(),
        data=summary.values(),
        columns=[total_score],
    ).drop("Total Score")
    summary_df.index = summary_df.index.rename("Total Score")

    # Fill it in
    colalign = ["right", "left", "right", "center", "right", "center", "center", "center"]
    template = (
        template.replace("{{ callsign }}", f"[{callsign}](https://www.qrz.com/db/{callsign})")
        .replace("{{ summary }}", summary_df.to_markdown(colalign=["left", "right"]))
        .replace("{{ logs }}", logs.to_markdown(colalign=colalign))
    )

    # Write it
    results_dir = Path("results")
    if not results_dir.exists():
        results_dir.mkdir()
    with open(results_dir / f"{callsign}.md", "w") as f:
        f.write(template)


def score_competition(
    repeaters: pd.DataFrame, logs_dir: str = "logs"
) -> Tuple[pd.DataFrame, str, str, str]:
    """
    Score the competition and return the results.

    Parameters
    ----------
    repeaters : pd.DataFrame
        All the repeaters.
    logs_dir : str
        The directory containing the logs.

    Returns
    -------
    pd.DataFrame
        The participant leaderboard.
    str
        A markdown-formatted table representation of the club leaderboard.
    str
        A markdown-formatted table representation of the repeater leaderboard.
    str
        A markdown-formatted bullet list of some statistics about the contest.
    """

    logs_dir = Path(logs_dir)
    if not logs_dir.exists():
        raise FileNotFoundError(f"{logs_dir} does not exist.")
    logs_files = logs_dir.glob("*.csv")

    # Load the repeater data
    repeaters.index = repeaters["RR#"]
    repeaters["Band"] = repeaters["Output (MHz)"].astype(float).apply(band)

    # A mapping between RR# and club name
    rrn_to_club = repeaters["Group Name"].to_dict()

    # Calculate club-based multipliers
    club_n_repeaters = repeaters["Group Name"].value_counts().to_dict()

    all_logs = []
    contest_scores = {}

    for file in logs_files:
        callsign = file.stem.split(" ")[0].split(",")[0].split("-")[0].upper()
        logs = pd.read_csv(file, index_col=None)
        logs = logs.dropna(subset=["Contact's Callsign", "Signal Report", "RR#"])
        logs["QRP"] = logs["QRP"].notna() * logs["QRP"].astype(bool)
        logs["Logger"] = callsign
        logs["Ordering"] = range(len(logs))
        logs["Contact's Callsign"] = logs["Contact's Callsign"].str.upper()
        logs["Signal Report"] = logs["Signal Report"].astype(str).apply(signal_report_to_readability)
        n_entries = len(logs)

        # Clean up the log sheet
        logs = logs.astype({"Signal Report": str, "RR#": int})

        # Add a band column
        logs = logs.merge(
            repeaters[["RR#", "Band"]],
            left_on="RR#",
            right_index=True,
            how="left",
            suffixes=(None, "_"),
        ).drop(columns="RR#_")

        # Add a group name column
        logs["Group Name"] = logs["RR#"].map(rrn_to_club)

        # Determine whether all repeaters from a club were worked
        club_repeaters_worked = logs.groupby("Group Name")["RR#"].nunique()
        logs["Club Connaisseur"] = logs["Group Name"].apply(
            lambda x: (club_repeaters_worked[x] == club_n_repeaters[x]) and (club_n_repeaters[x] >= 2)
        )

        # Label any duplicates, trying to keep higher-scoring entries as the non-duplicate
        logs = logs.sort_values("QRP")
        logs["Duplicate"] = logs.duplicated(subset=["RR#", "Contact's Callsign"], keep="last")
        n_duplicates = logs["Duplicate"].sum()
        logs = logs.sort_values("Ordering")
        logs = logs.loc[~logs["Duplicate"]].drop(columns=["Ordering", "Duplicate"])

        # Determine if 30+ 2m or 70cm repeaters were worked
        bandhog = {
            "2m": logs.loc[logs["Band"] == "2m", "RR#"].nunique() >= 30,
            "70cm": logs.loc[logs["Band"] == "70cm", "RR#"].nunique() >= 30,
        }
        logs["Bandhog"] = logs["Band"].apply(lambda x: bandhog.get(x, False))

        # Full house
        full_house = bool(logs["RR#"].nunique() >= 80)
        logs["Full House"] = full_house

        # Calculate QSO score
        logs["QSO Score"] = (
            logs["QRP"].apply(lambda x: 2 if x else 1)
            * logs["Club Connaisseur"].apply(lambda x: 2 if x else 1)
            * logs["Bandhog"].apply(lambda x: 2 if x else 1)
            * logs["Full House"].apply(lambda x: 2 if x else 1)
        )

        # Summarise the logs
        summary = {
            "Total Score": logs["QSO Score"].sum(),
            "Total Contacts": n_entries,
            "QRP Contacts": logs["QRP"].sum(),
            "Club Connaisseur Contacts": logs["Club Connaisseur"].sum(),
            "Band Hog Contacts": logs["Bandhog"].sum(),
            "Duplicate Contacts": n_duplicates,
            "Full House": "X" if full_house else "",
        }

        # Clean up the logs
        logs = (
            logs.drop(columns=["Full House"])
            .rename(columns={"Contact's Callsign": "Contact"})
            .set_index("RR#", drop=True)
        )

        # Save this person's contest scores
        all_logs.append(logs.copy())
        contest_scores[callsign.upper()] = summary

        # Write a Markdown file for the participant
        write_personal_results_md(logs, summary, callsign)

    # Save the contest scores
    leaderboard = (
        pd.DataFrame(contest_scores)
        .T.sort_values(["Total Score", "Total Contacts"], ascending=False)
        .reset_index(drop=False)
        .rename(
            columns={
                "index": "Callsign",
                "QRP Contacts": "QRP",
                "Band Hog Contacts": "Band Hog",
                "Club Connaisseur Contacts": "Club Connaisseur",
            }
        )
    )
    leaderboard["Callsign"] = leaderboard["Callsign"].apply(
        lambda call: f"[{call}](/results/{call})"
    )
    leaderboard = leaderboard[
        [
            "Callsign",
            "Total Score",
            "Total Contacts",
            "QRP",
            "Band Hog",
            "Club Connaisseur",
            "Full House",
        ]
    ]
    leaderboard["Full House"] = leaderboard["Full House"].apply(lambda x: "X" if x else "")

    # Set a new index with leaderboard positions, but accounting for ties
    leaderboard.index = leaderboard["Total Score"].rank(method='min', ascending=False).astype(int)

    # Merge all logs with repeater data
    repeater_cols = ["RR#", "Long Name", "Output (MHz)", "Location", "Website"]
    logs_df = (
        pd.concat(all_logs, ignore_index=False)
        .reset_index()
        .merge(repeaters[repeater_cols], left_on="RR#", right_index=True)
        .drop(columns=["RR#_x", "RR#_y"])
        .rename(columns={"Long Name": "Group", "Output (MHz)": "Frequency"})
        .astype({"Frequency": float})
    )
    logs_df = logs_df.drop(columns=[col for col in logs_df.columns if "Unnamed: " in col])

    # Attempt to clean up signal reports
    logs_df["Readability"] = logs_df["Signal Report"].apply(signal_report_to_readability)
    if logs_df["Readability"].isna().any():
        errors_in = ", ".join(logs_df.loc[logs_df["Readability"].isna(), "Logger"].unique())
        print(f"Errors in signal reports : {errors_in}")

    # Bring URLs into club names
    logs_df["Group"] = logs_df.apply(lambda row: f"[{row['Group']}]({row['Website']})", axis=1)
    logs_df = logs_df.drop(columns=["Website"])

    # Calculate the number of activations per repeater
    agg_cols = {
        "Group": "first",
        "Frequency": "first",
        "Time": "count",
        "Readability": "mean",
    }
    by_repeater = (
        logs_df.groupby("RR#")
        .agg(agg_cols)
        .rename(columns={"Time": "Activations"})
        .sort_values(["Activations", "Group", "Frequency"], ascending=[False, True, True])
        .reset_index(drop=True)
        .round({"Readability": 2})
    )
    by_repeater.index = by_repeater["Activations"].rank(method='min', ascending=False).astype(int)
    by_repeater["Frequency"] = by_repeater["Frequency"].apply(at_least_three_decimals)

    # Calculate the number of activations per club
    by_club = (
        by_repeater.groupby("Group")["Activations"]
        .sum()
        .to_frame()
        .sort_values(["Activations", "Group"], ascending=[False, True])
        .reset_index(drop=False)  # index contains the club name
    )
    by_club.index = by_club["Activations"].rank(method='min', ascending=False).astype(int)

    # Some stats :
    total_contacts = sum([scores["Total Contacts"] for scores in contest_scores.values()])
    stats = {
        "Number of participants who submitted logs": len(leaderboard),
        "Total number of contacts made": f"{total_contacts:,}",
        "Number of unique operators contacted": logs_df["Contact"].nunique(),
        "Number of repeaters activated": len(by_repeater),
    }
    stats_msg = "\n".join(f"- {key} : {val}" for key, val in stats.items())
    print(stats_msg)

    return (
        leaderboard,
        by_repeater.to_markdown(
            disable_numparse=True, colalign=["right", "left", "right", "right", "right"]
        ),
        by_club.to_markdown(colalign=["right", "left", "right"]),
        stats_msg,
    )
