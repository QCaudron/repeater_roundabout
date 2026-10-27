import os
import tempfile

import pandas as pd

from programming_files import format_df_for_d878, format_df_for_icom, write_d878_zip, write_generic_csv


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


def test_formatters_cope_with_missing_coordinates(tmp_path, monkeypatch):
    """A repeater without coordinates still gets a channel and a CSV row, with a blank location."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets" / "programming_files").mkdir(parents=True)
    df = pd.DataFrame(
        {
            "RR#": [1],
            "Callsign": ["W7ABC"],
            "Mode": ["FM"],
            "Output (MHz)": ["146.0"],
            "Offset (MHz)": ["-0.6"],
            "Tone (Hz)": ["100.0"],
            "Coordinates": [None],
            "Group Name": ["G"],
            "Long Name": ["Group"],
            "Status": ["in"],
        }
    )

    assert len(format_df_for_d878(df)) == 1
    write_generic_csv(df)
    assert (tmp_path / "assets" / "programming_files" / "all_rr_frequencies.csv").exists()


def test_formatters_with_no_compatible_repeaters():
    """The D878 and Icom formatters return empty channel lists rather than crashing when no repeater suits the radio."""
    df = pd.DataFrame(
        {
            "RR#": [1],
            "Callsign": ["W7ABC"],
            "Mode": ["FM"],
            "Output (MHz)": ["224.0"],
            "Offset (MHz)": ["-1.6"],
            "Tone (Hz)": ["100.0"],
            "Coordinates": [(47.6, -122.3)],
        }
    )

    assert len(format_df_for_d878(df)) == 0
    assert len(format_df_for_icom(df)) == 0


def test_write_d878_zip_with_no_compatible_repeaters(tmp_path, monkeypatch):
    """write_d878_zip writes a channel-less zip rather than crashing when no repeater suits the D878."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets" / "programming_files").mkdir(parents=True)
    df = pd.DataFrame(
        {
            "RR#": [1],
            "Callsign": ["W7ABC"],
            "Mode": ["FM"],
            "Output (MHz)": ["224.0"],
            "Offset (MHz)": ["-1.6"],
            "Tone (Hz)": ["100.0"],
            "Coordinates": [(47.6, -122.3)],
        }
    )

    write_d878_zip(df)

    assert (tmp_path / "assets" / "programming_files" / "d878.zip").exists()


def test_write_generic_csv():
    """write_generic_csv must not crash when dropping columns."""
    df = pd.DataFrame(
        {
            "RR#": [1],
            "Group Name": ["Group"],
            "Long Name": ["Long Group Name"],
            "Status": ["in"],
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
    test_formatters_with_no_compatible_repeaters()
    test_write_generic_csv()
    print("OK")
