import os
import tempfile

import pandas as pd

from programming_files import format_df_for_d878, write_generic_csv


def test_format_df_for_d878_with_no_dmr_repeaters():
    """format_df_for_d878 must not crash when there are zero DMR repeaters."""
    df = pd.DataFrame(
        {
            "RR#": [1],
            "Callsign": ["W7ABC"],
            "Mode": ["FM"],
            "Output (MHz)": ["146.0"],
            "Offset (MHz)": ["-0.6"],
            "Tone (Hz)": ["100.0"],
            "Coordinates": [(47.6, -122.3)],
        }
    )

    result = format_df_for_d878(df)

    assert (result["Color Code"] == 1).all()


def test_write_generic_csv():
    """write_generic_csv must not crash when dropping columns."""
    df = pd.DataFrame(
        {
            "RR#": [1],
            "Group Name": ["Group"],
            "Long Name": ["Long Group Name"],
            "Exclude": [False],
            "Coordinates": [(47.6, -122.3)],
        }
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        cwd = os.getcwd()
        os.makedirs(os.path.join(tmp_dir, "assets", "programming_files"))
        os.chdir(tmp_dir)
        try:
            write_generic_csv(df)
        finally:
            os.chdir(cwd)


if __name__ == "__main__":
    test_format_df_for_d878_with_no_dmr_repeaters()
    test_write_generic_csv()
    print("OK")
