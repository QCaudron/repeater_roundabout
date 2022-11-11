from pathlib import Path
from types import SimpleNamespace

import pandas as pd

from update import generate_repeater_df

logs_dir = Path("logs")
logs_files = logs_dir.glob("*.csv")


args = SimpleNamespace(regen=True)


if __name__ == "__main__":

    if not logs_dir.exists():
        raise FileNotFoundError(f"{logs_dir} does not exist.")

    # Load the repeater data
    repeaters = generate_repeater_df(args)
    repeaters.index = repeaters["RR#"]

    # A mapping between RR# and club name
    rrn_to_club = repeaters["Group Name"].to_dict()

    # Calculate club-based multipliers
    club_n_repeaters = repeaters["Group Name"].value_counts().to_dict()

    contest_scores = {}

    for file in logs_files:

        callsign = file.stem
        logs = pd.read_csv(file)

        n_entries = len(logs)

        # Remove any duplicates
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
    contest_scores_df = pd.DataFrame(contest_scores).T.sort_values("Total Score", ascending=False)
    print(contest_scores_df)
    contest_scores_df.to_csv("contest_scores.csv")
