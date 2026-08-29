import pandas as pd

from programming_files import format_df_for_d878


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


if __name__ == "__main__":
    test_format_df_for_d878_with_no_dmr_repeaters()
    print("OK")
