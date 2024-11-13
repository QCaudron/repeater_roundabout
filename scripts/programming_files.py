import math
from typing import Literal
from zipfile import ZipFile

import pandas as pd

BAND_DEFINITIONS = {
    "6m": (50, 54),
    "2m": (144, 148),
    "1.25m": (220, 225),
    "70cm": (420, 450),
    "33cm": (900, 930),
    "23cm": (1240, 1300),
}

BANDS = Literal["6m", "2m", "1.25m", "70cm", "33cm", "23cm"]

DOWNTOWN_SEATTLE = (47.6062, -122.3321)
METRO_DISTANCE = 20


def filter_by_band(df: pd.DataFrame, bands: list[BANDS]) -> pd.DataFrame:
    """
    Filter a DataFrame of repeaters by a given band.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    bands : list of bands {"6m", "2m", "1.25m", "70cm", "33cm", "23cm"}
        Bands to include in the output DataFrame.

    Returns
    -------
    pd.DataFrame
        Repeaters in the given bands.
    """

    band_dfs = []
    for band in bands:
        band_dfs.append(
            df.loc[
                (df["Output (MHz)"].astype(float) > BAND_DEFINITIONS[band][0])
                & (df["Output (MHz)"].astype(float) < BAND_DEFINITIONS[band][1])
            ].copy()
        )

    return pd.concat(band_dfs).sort_index()


def filter_by_mode(df: pd.DataFrame, modes: list[str]) -> pd.DataFrame:
    """
    Filter a DataFrame of repeaters by a given mode.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    modes : list of modes
        Modes to include in the output DataFrame.

    Returns
    -------
    pd.DataFrame
        Repeaters in the given modes.
    """

    return df.loc[df["Mode"].isin(modes)].sort_index().copy()


def distance_between(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calculate the distance between two points.

    Parameters
    ----------
    p1 : tuple of floats
        Latitude and longitude of the first point.
    p2 : tuple of floats
        Latitude and longitude of the second point.

    Returns
    -------
    float
        Distance between the two points in miles.
    """

    # Convert to radians
    p1 = (math.radians(p1[0]), math.radians(p1[1]))
    p2 = (math.radians(p2[0]), math.radians(p2[1]))

    # Calculate the distance
    dlon = p2[1] - p1[1]
    dlat = p2[0] - p1[0]
    a = (math.sin(dlat / 2)) ** 2 + math.cos(p1[0]) * math.cos(p2[0]) * (math.sin(dlon / 2)) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 3959.0 * c


def format_df_for_chirp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format a DataFrame of repeaters for use in CHIRP.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.

    Returns
    -------
    pd.DataFrame
        The FM repeaters, formatted for CHIRP.
    """

    total_repeaters = len(df)

    # Remove repeaters not in the contest
    df = df.loc[df["Exclude"].isna()]

    # Only format FM channels; we can't handle DMR or D-Star at the moment
    df = filter_by_mode(df, ["FM", "NBFM", "YSF"])  # only FM repeaters
    df.loc[df["Mode"] == "NBFM", "Mode"] = "NFM"  # NBFM -> NFM for Chirp
    df.loc[df["Mode"] == "YSF", "Mode"] = "FM"  # YSF -> FM for Chirp

    print(f"Chirp: {len(df)} compatible repeaters (out of {total_repeaters} known).")

    # Set the offset direction and value
    df = df.assign(Duplex=df["Offset (MHz)"].str[0])  # + or -, first char of Offset
    df = df.assign(Offset=df["Offset (MHz)"].str[1:].apply(lambda x: f"{float(x):.06f}"))

    # Some columns can be reused
    df["Comment"] = df["Callsign"] + " - " + df["Output (MHz)"]
    df = df.rename(
        columns={
            "Callsign": "Name",
            "Output (MHz)": "Frequency",
            "Tone (Hz)": "rToneFreq",
        }
    )

    # Set some constant basics that are required for Chirp to read the file
    df["Tone"] = "Tone"
    df["cToneFreq"] = "88.5"
    df["DtcsCode"] = "023"
    df["DtcsPolarity"] = "NN"
    df["TStep"] = "5.00"

    # DCS tones are different, so go back and fix that
    dcs = df["rToneFreq"].str.startswith("D")
    df.loc[dcs, "Tone"] = "DTCS"
    df.loc[dcs, "DtcsCode"] = df.loc[dcs, "rToneFreq"].str[1:4]
    df.loc[dcs, "rToneFreq"] = "88.5"

    # The following columns are null
    for col in ["Skip", "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE"]:
        df[col] = None

    # Set the RR number as the channel number
    df.index = df["RR#"]
    df.index.name = "Location"
    df = df.sort_index()

    # Order columns as Chirp expects
    df = df[
        [
            "Name",
            "Frequency",
            "Duplex",
            "Offset",
            "Tone",
            "rToneFreq",
            "cToneFreq",
            "DtcsCode",
            "DtcsPolarity",
            "Mode",
            "TStep",
            "Skip",
            "Comment",
            "URCALL",
            "RPT1CALL",
            "RPT2CALL",
            "DVCODE",
        ]
    ]

    return df


def format_df_for_d878(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format a DataFrame of repeaters for use in Anytone D878.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.

    Returns
    -------
    pd.DataFrame
        The repeaters in the 2m and 70cm bands, formatted for Anytone D878.
    """

    total_repeaters = len(df)

    # Remove repeaters not in the contest
    df = df.loc[df["Exclude"].isna()]

    # Select FM, DMR and YSF (in FM compat mode) channels in the 2m or 70cm bands.
    df = filter_by_mode(df, ["FM", "NBFM", "DMR", "YSF"])
    df = filter_by_band(df, ["2m", "70cm"])

    # Set the RR number as the channel number
    df.index = df["RR#"]
    df = df.sort_index()

    # Treat output and offset as numerical values (to sum them later)
    numeric_columns = ["Output (MHz)", "Offset (MHz)"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

    print(f"AnyTone D878: {len(df)} compatible repeaters (out of {total_repeaters} known).")

    df_878 = pd.DataFrame()

    df_878.index.name = "No."
    df_878["Channel Name"] = df["Callsign"]
    df_878["Receive Frequency"] = df["Output (MHz)"]
    df_878["Transmit Frequency"] = df["Output (MHz)"] + df["Offset (MHz)"]

    df_878 = df_878.round(4)

    is_dmr = df["Mode"] == "DMR"
    df_878.loc[is_dmr, "Channel Type"] = "D-Digital"
    df_878.loc[~is_dmr, "Channel Type"] = "A-Analog"
    # Not sure why this seemingly redundant column is in the format?
    df_878.loc[is_dmr, "DMR MODE"] = "1"
    df_878.loc[~is_dmr, "DMR MODE"] = "0"

    # Both DMR and NBFM are "narrow"
    is_widefm = df["Mode"].isin(["FM", "YSF"])
    df_878.loc[is_widefm, "Band Width"] = "25K"
    df_878.loc[~is_widefm, "Band Width"] = "12.5K"

    is_dcs = df["Tone (Hz)"].str.startswith("D")
    # TODO: Use regexp for DCS tone number between D and '[' in string?
    df_878.loc[is_dcs, "CTCSS/DCS Encode"] = "D" + df["Tone (Hz)"].str[1:4] + "N"
    df_878.loc[~is_dcs, "CTCSS/DCS Encode"] = df["Tone (Hz)"]
    df_878.loc[is_dmr, "CTCSS/DCS Encode"] = None

    # Parse Tone string with DMR attributes: e.g., "CC2/TS1 BEARS1 TG/312488"
    dmr_codes = df.loc[is_dmr, "Tone (Hz)"].str.extract(
        r"CC(?P<color>\d+)\/TS(?P<slot>[12]) (?P<contact>\S+) TG\/(?P<id>\d+)"
    )
    df_878.loc[is_dmr, "Contact"] = dmr_codes["contact"]
    df_878.loc[is_dmr, "Contact TG/DMR ID"] = dmr_codes["id"]
    # Bug in CPS software - fails if Color Code column is empty - even for analog channels!
    df_878["Color Code"] = 1
    df_878.loc[is_dmr, "Color Code"] = dmr_codes["color"]
    df_878.loc[is_dmr, "Slot"] = dmr_codes["slot"]

    is_metro = df.apply(
        lambda x: distance_between(x["Coordinates"], DOWNTOWN_SEATTLE) < METRO_DISTANCE,
        axis=1,
    )
    df_878.loc[is_metro, "Scan List"] = "Metro"
    is_north = df.apply(lambda x: x["Coordinates"][0] > DOWNTOWN_SEATTLE[0], axis=1)
    df_878.loc[~is_metro & is_north, "Scan List"] = "North"
    df_878.loc[~is_metro & ~is_north, "Scan List"] = "South"

    return df_878


def format_df_for_icom(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format a DataFrame of repeaters for use in Icom 878 CSV format.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.

    Returns
    -------
    pd.DataFrame
        The Icom-compatible repeaters formatted for the Icom.
        (Tested with Icom-705 - may work for others).
    """

    total_repeaters = len(df)

    # Remove repeaters not in the contest
    df = df.loc[df["Exclude"].isna()]

    # Select FM and YSF (in FM compat mode) channels.
    df = filter_by_mode(df, ["FM", "NBFM", "YSF", "DSTAR"])
    df = filter_by_band(df, ["6m", "2m", "70cm"])

    # Treat output and offset as numerical values
    numeric_columns = ["Output (MHz)", "Offset (MHz)"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

    # Set the RR number as the channel number
    df.index = df["RR#"]
    df = df.sort_index()

    print(f"Icom IC-705: {len(df)} compatible repeaters (out of {total_repeaters} known).")

    df_icom = pd.DataFrame()
    is_dstar = df["Mode"] == "DSTAR"

    df_icom.index.name = "CH No"
    df_icom["Name"] = df["Callsign"]
    df_icom["Mode"] = "FM"
    df_icom.loc[is_dstar, "Mode"] = "DV"
    df_icom["Frequency"] = df["Output (MHz)"]
    df_icom["Dup"] = "DUP+"
    df_icom.loc[df["Offset (MHz)"] < 0, "Dup"] = "DUP-"
    df_icom["Offset"] = df["Offset (MHz)"].abs()
    df_icom.loc[is_dstar, "RPT1 Call Sign"] = df.apply(dstar_callsign, axis=1)
    df_icom.loc[is_dstar, "RPT2 Call Sign"] = df.apply(dstar_callsign_2, axis=1)

    # Icom Filters are (1) 15kHz wide and (2) 10kHz wide.
    df_icom["Filter"] = "1"
    df_icom.loc[df["Mode"] == "NBFM", "Filter"] = "2"
    # DSTAR is 6.25kHz wide - use the 7KHz filter.
    df_icom.loc[is_dstar, "Filter"] = "3"

    df_icom = df_icom.round(4)

    is_dcs = df["Tone (Hz)"].str.startswith("D")
    # TODO: Use regexp for DCS tone number between D and '[' in string?
    df_icom.loc[~is_dcs, "TONE"] = "TONE"
    df_icom.loc[~is_dcs, "Repeater Tone"] = df["Tone (Hz)"] + "Hz"
    df_icom.loc[is_dcs, "TONE"] = "DTCS"
    df_icom.loc[is_dcs, "DTCS Code"] = df["Tone (Hz)"].str[1:4]

    return df_icom


def dstar_callsign_format(callsign: str, module: str) -> str:
    """
    Format a callsign for use in DSTAR.

    Parameters
    ----------
    callsign : str
        The callsign to format.
    module : str
        Module is one of 'A' 1.2 GHz, 'B' 70cm, or 'C' 2m.

    Returns
    -------
    str
        The formatted callsign - 8 characters long with module as the 8th character.
    """
    return f"{callsign:7s}{module}"


def dstar_module_from_frequency(frequency: float) -> str:
    """
    Determine the DSTAR module from a frequency.

    Parameters
    ----------
    frequency : float
        The frequency to check.

    Returns
    -------
    str
        The DSTAR module - one of 'A' 1.2 GHz, 'B' 70cm, or 'C' 2m.
    """

    if frequency < 148.0:
        return "C"
    elif frequency < 450.0:
        return "B"
    else:
        return "A"


def dstar_callsign(row: pd.Series) -> str:
    """
    Generate a DSTAR callsign from the repeater callsign and output frequency.

    Parameters
    ----------
    row : pd.Series
        The row of the DataFrame.

    Returns
    -------
    str
        The properly formatted DSTAR callsign.
    """
    callsign = row["Callsign"]
    frequency = row["Output (MHz)"]
    return dstar_callsign_format(callsign, dstar_module_from_frequency(frequency))


def dstar_callsign_2(row: pd.Series) -> str:
    """
    Generate a DSTAR callsign from the repeater callsign and output frequency
    for RPT2 callsign column.

    Parameters
    ----------
    row : pd.Series
        The row of the DataFrame.

    Returns
    -------
    str
        The properly formatted DSTAR callsign.
    """

    callsign = row["Callsign"]
    return dstar_callsign_format(callsign, "G")


def write_chirp_csv(df: pd.DataFrame) -> None:
    """
    Write the chirp.csv file.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    """
    df = format_df_for_chirp(df)
    df.to_csv("assets/programming_files/rr_frequencies.csv")


def write_icom_csv(df: pd.DataFrame) -> None:
    """
    Write Icom (705 - maybe others) CSV import file.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    """

    df = format_df_for_icom(df)
    df.to_csv("assets/programming_files/icom.csv")


def write_d878_zip(df: pd.DataFrame) -> None:
    """
    Write the Anytone D878 csv file.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    """

    df = format_df_for_d878(df)
    # D878 CPS software requires CR/LF line endings
    df.to_csv("assets/programming_files/d878.csv", lineterminator="\r\n")

    # Generate a scan list for each region
    scan_lists = {region: df.loc[df["Scan List"] == region] for region in df["Scan List"].unique()}
    rows = []
    for region, df_channels in scan_lists.items():
        names = "|".join(df_channels["Channel Name"].tolist())
        rx_freqs = "|".join(df_channels["Receive Frequency"].astype(str).tolist())
        tx_freqs = "|".join(df_channels["Transmit Frequency"].astype(str).tolist())
        rows.append(
            {
                "Scan List Name": region,
                "Scan Channel Member": names,
                "Scan Channel Member RX Frequency": rx_freqs,
                "Scan Channel Member TX Frequency": tx_freqs,
            }
        )
    df_scanlist = pd.DataFrame(rows)
    df_scanlist.index.name = "No."
    df_scanlist.index = df_scanlist.index + 1
    df_scanlist.to_csv("assets/programming_files/d878-scanlist.csv", lineterminator="\r\n")

    # List of used Talk Groups needed (not DRY - but Talk Groups don't import if not present!)
    talk_groups = {
        id: df.loc[df["Contact TG/DMR ID"] == id, "Contact"].iloc[0]
        for id in df["Contact TG/DMR ID"].dropna().unique()
    }
    rows = [{"Radio ID": id, "Name": talk_groups[id]} for id in talk_groups]
    rows.append({"Radio ID": 9998, "Name": "Parrot"})
    rows.append({"Radio ID": 9999, "Name": "Audio Test"})
    df_talkgroups = pd.DataFrame(rows)
    df_talkgroups["Call Type"] = "Group Call"
    df_talkgroups.index.name = "No."
    df_talkgroups.index = df_talkgroups.index + 1
    df_talkgroups.to_csv("assets/programming_files/d878-talk-groups.csv", lineterminator="\r\n")

    with ZipFile("assets/programming_files/d878.zip", "w") as zipf:
        zipf.write("assets/programming_files/d878.csv", arcname="d878.csv")
        zipf.write("assets/programming_files/d878-scanlist.csv", arcname="d878-scanlist.csv")
        zipf.write(
            "assets/programming_files/d878-talk-groups.csv",
            arcname="d878-talk-groups.csv",
        )


def write_generic_csv(df: pd.DataFrame) -> None:
    """
    Write a generic CSV file containing all repeaters.

    Parameters
    ----------
    df : pd.DataFrame
        All of the repeaters.
    """

    df = (
        df.copy()
        .assign(Latitude=df["Coordinates"].apply(lambda x: x[0]))
        .assign(Longitude=df["Coordinates"].apply(lambda x: x[1]))
        .drop(columns=["Group Name", "Coordinates", "Exclude"], axis=1)
        .rename(columns={"Long Name": "Group"})
        .set_index("RR#")
    )

    print(f"Generic CSV: {len(df)} repeaters from {df['Group'].nunique()} groups.")
    df.to_csv("assets/programming_files/all_rr_frequencies.csv")


def band(freq: float) -> str:
    """
    Map between frequency and band name.

    Parameters
    ----------
    freq : float
        The repeater's output frequency.

    Returns
    -------
    str
        The name of the amateur radio band.
    """

    for band_name, edges in BAND_DEFINITIONS.items():
        if edges[0] < freq < edges[1]:
            return band_name

    return "other"
