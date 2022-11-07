from zipfile import ZipFile

import pandas as pd


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

    # Only format FM channels; we can't handle DMR or D-Star at the moment
    df = df.loc[df["Mode"].isin(["FM", "NBFM", "Fusion"])].copy()  # only FM repeaters
    df.loc[df["Mode"] == "NBFM", "Mode"] = "NFM"  # NBFM -> NFM for Chirp
    df.loc[df["Mode"] == "Fusion", "Mode"] = "FM"  # Fusion -> FM for Chirp

    print(f"Chirp: {len(df)} compatible repeaters (out of {total_repeaters}).")

    # Set the offset direction and value
    df = df.assign(Duplex=df["Offset (MHz)"].str[0])  # + or -, first char of Offset
    df = df.assign(
        Offset=df["Offset (MHz)"].str[1:].apply(lambda x: f"{float(x):.06f}")
    )

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

    # Select FM, DMR and Fusion (in FM compat mode) channels.
    df = df.loc[df["Mode"].isin(["FM", "NBFM", "DMR", "Fusion"])].copy()

    # Restrict to available bands
    numeric_columns = ["Output (MHz)", "Offset (MHz)"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
    df_2m = df.loc[(df["Output (MHz)"] > 144.0) & (df["Output (MHz)"] < 148.0)]
    df_70cm = df.loc[(df["Output (MHz)"] > 430.0) & (df["Output (MHz)"] < 450.0)]

    # Set the RR number as the channel number
    df = pd.concat([df_2m, df_70cm])
    df.index = df["RR#"]
    df = df.sort_index()

    print(f"AnyTone D878: {len(df)} compatible repeaters (out of {total_repeaters}).")

    df_878 = pd.DataFrame()

    df_878.index.name = "No."
    df_878["Channel Name"] = df["Callsign"]
    df_878["Receive Frequency"] = df["Output (MHz)"]
    df_878["Transmit Frequency"] = df["Output (MHz)"] + df["Offset (MHz)"]

    df_878 = df_878.round(3)

    is_dmr = df["Mode"] == "DMR"
    df_878.loc[is_dmr, "Channel Type"] = "D-Digital"
    df_878.loc[~is_dmr, "Channel Type"] = "A-Analog"
    # Not sure why this seemingly redundant column is in the format?
    df_878.loc[is_dmr, "DMR MODE"] = "1"
    df_878.loc[~is_dmr, "DMR MODE"] = "0"

    # Both DMR and NBFM are "narrow"
    is_widefm = df["Mode"].isin(["FM", "Fusion"])
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

    # TODO: Need to programatically generate a "scan list" csv file in order to be able
    # to scan all the frequencies in the Roundabout.  For now - a dummy file added to
    # ./assets.
    df_878["Scan List"] = "Roundabout"

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
        The Icom-compativle repeaters formatted for the Icom.
        (Tested with Icom-705 - may work for others).
    """

    total_repeaters = len(df)

    # Select FM and Fusion (in FM compat mode) channels.
    df = df.loc[df["Mode"].isin(["FM", "NBFM", "Fusion"])].copy()

    # Restrict to available bands
    numeric_columns = ["Output (MHz)", "Offset (MHz)"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
    df_6m = df.loc[(df["Output (MHz)"] > 50.0) & (df["Output (MHz)"] < 54.0)]
    df_2m = df.loc[(df["Output (MHz)"] > 144.0) & (df["Output (MHz)"] < 148.0)]
    df_125cm = df.loc[(df["Output (MHz)"] > 222.0) & (df["Output (MHz)"] < 225.0)]
    df_70cm = df.loc[(df["Output (MHz)"] > 430.0) & (df["Output (MHz)"] < 450.0)]

    # Set the RR number as the channel number
    df = pd.concat([df_6m, df_2m, df_125cm, df_70cm])
    df.index = df["RR#"]
    df = df.sort_index()

    print(f"Icom IC-705: {len(df)} compatible repeaters (out of {total_repeaters}).")

    df_icom = pd.DataFrame()

    df_icom.index.name = "CH No"
    df_icom["Name"] = df["Callsign"]
    df_icom["Mode"] = "FM"
    df_icom["Frequency"] = df["Output (MHz)"]
    df_icom["Dup"] = "DUP+"
    df_icom.loc[df["Offset (MHz)"] < 0, "Dup"] = "DUP-"
    df_icom["Offset"] = df["Offset (MHz)"].abs()

    # Icom Filters are (1) 15kHz wide and (2) 10kHz wide.
    df_icom["Filter"] = "1"
    df_icom.loc[df["Mode"] == "NBFM", "Filter"] = "2"

    df_icom = df_icom.round(3)

    is_dcs = df["Tone (Hz)"].str.startswith("D")
    # TODO: Use regexp for DCS tone number between D and '[' in string?
    df_icom.loc[~is_dcs, "TONE"] = "TONE"
    df_icom.loc[~is_dcs, "Repeater Tone"] = df["Tone (Hz)"] + "Hz"
    df_icom.loc[is_dcs, "TONE"] = "DTCS"
    df_icom.loc[is_dcs, "DTCS Code"] = df["Tone (Hz)"].str[1:4]

    return df_icom


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

    # TODO : generate scanlist and talk groups files here

    with ZipFile("assets/programming_files/d878.zip", "w") as zipf:
        zipf.write("assets/programming_files/d878.csv", arcname="d878.csv")
        zipf.write(
            "assets/programming_files/d878-scanlist.csv", arcname="d878-scanlist.csv"
        )
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

    df.index = df["RR#"]
    df.index.name = "Channel"
    df = df.sort_index()

    (
        df.drop(["Group Name", "Website", "RR#", "Coordinates"], axis=1)
        .rename(columns={"Long Name": "Group"})
        .to_csv("assets/programming_files/all_rr_frequencies.csv")
    )
