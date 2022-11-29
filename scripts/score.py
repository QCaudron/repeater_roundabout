import re
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

logs_dir = Path("logs")
logs_files = logs_dir.glob("*.csv")


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


def score_competition(repeaters: pd.DataFrame) -> Tuple[pd.DataFrame, str, str, str]:
    """
    Score the competition and return the results.

    Parameters
    ----------
    repeaters : pd.DataFrame
        All the repeaters.

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

    if not logs_dir.exists():
        raise FileNotFoundError(f"{logs_dir} does not exist.")

    # Load the repeater data
    repeaters.index = repeaters["RR#"]

    # A mapping between RR# and club name
    rrn_to_club = repeaters["Group Name"].to_dict()

    # Calculate club-based multipliers
    club_n_repeaters = repeaters["Group Name"].value_counts().to_dict()

    all_logs = []
    contest_scores = {}

    for file in logs_files:

        callsign = file.stem.split(" ")[0].split(",")[0].split("-")[0]
        logs = pd.read_csv(file, index_col=[0])
        logs["Logger"] = callsign
        n_entries = len(logs)

        # Clean up the log sheet
        logs = logs.astype({"Signal Report": str, "RR#": int})
        all_logs.append(logs.copy())  # save pre-deduped logs for activation counts
        logs = logs.drop_duplicates(subset=["RR#"], keep="first")
        n_duplicates = n_entries - len(logs)
        base_score = len(logs)

        # Add a group name column
        logs["Group Name"] = logs["RR#"].map(rrn_to_club)

        # Determine whether all repeaters from a club were worked
        worked = logs["Group Name"].value_counts().rename("Worked").to_frame()
        worked["Total"] = worked.index.map(club_n_repeaters)
        worked["All Repeaters Worked"] = worked["Worked"] == worked["Total"]
        worked["Bonus Eligible"] = worked["Total"] > 1

        # Calculate bonus points
        worked["Bonus Points"] = (
            worked["All Repeaters Worked"] * worked["Worked"] * worked["Bonus Eligible"]
        )
        bonus_points = worked["Bonus Points"].sum()

        # Save this person's contest scores
        contest_scores[callsign.upper()] = {
            "Entries": n_entries,
            "Duplicates": n_duplicates,
            "Base Score": base_score,
            "Bonus Points": bonus_points,
            "Total Score": base_score + bonus_points,
        }

    # Save the contest scores
    leaderboard = (
        pd.DataFrame(contest_scores)
        .T.sort_values(["Total Score", "Base Score", "Entries"], ascending=False)
        .reset_index(drop=False)
        .rename(columns={"index": "Callsign"})
    )
    leaderboard.index = leaderboard.index + 1
    leaderboard["Callsign"] = leaderboard["Callsign"].apply(
        lambda call: f"[{call}](https://www.qrz.com/db/{call})"
    )

    # Merge all logs with repeater data
    repeater_cols = ["RR#", "Long Name", "Output (MHz)", "Location", "Website"]
    logs_df = (
        pd.concat(all_logs, ignore_index=True)
        .merge(repeaters[repeater_cols], left_on="RR#", right_index=True)
        .drop(columns=["RR#_x", "RR#_y"])
        .rename(columns={"Long Name": "Group", "Output (MHz)": "Frequency"})
        .astype({"Frequency": float})
    )

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
    by_repeater.index = by_repeater.index + 1
    by_repeater["Frequency"] = by_repeater["Frequency"].apply(at_least_three_decimals)

    # Calculate the number of activations per club
    by_club = (
        by_repeater.groupby("Group")["Activations"]
        .sum()
        .to_frame()
        .sort_values(["Activations", "Group"], ascending=[False, True])
        .reset_index(drop=False)  # index contains the club name
    )
    by_club.index = by_club.index + 1

    # Some stats :
    stats = {
        "Number of participants who submitted logs": len(leaderboard),
        "Total number of contacts made": f"{len(logs_df):,}",
        "Number of unique operators contacted": logs_df["Contact's Callsign"].nunique(),
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
