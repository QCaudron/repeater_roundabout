import pandas as pd


def parse_markdown_table(text: str) -> pd.DataFrame:
    """
    Parse a markdown table into a pandas DataFrame.
    """

    # Split the table into lines
    table = "|".join(text.split("|")[1:-1]) + "|"

    # Identify the columns
    columns = [x.strip() for x in table.split("\n")[0].split("|")[:-1]]

    # Parse out the rows
    rows = [row.split("|")[1:-1] for row in table.split("\n")[2:]]
    rows = [[x.strip() for x in row] for row in rows]

    return pd.DataFrame(rows, columns=columns)


def format_df_for_chirp(df: pd.DataFrame) -> pd.DataFrame:

    # Only format FM channels; we can't handle DMR or D-Star at the moment
    df = df.loc[df["Mode"] == "FM"]  # only FM repeaters

    # Set the offset direction and value
    df = df.assign(Duplex=df["Offset (MHz)"].str[0])  # + or -, first char of Offset
    df = df.assign(Offset=df["Offset (MHz)"].str[1:].apply(lambda x: f"{float(x):.06f}"))

    # Some columns can be reused
    df["Comment"] = df["Callsign"] + " - " + df["Output (MHz)"]
    df = df.rename(columns={
        "Callsign": "Name",
        "Output (MHz)": "Frequency",
        "Tone (Hz)": "rToneFreq",
    })

    # Set some constant basics that are required for Chirp to read the file
    df["Tone"] = "Tone"
    df["cToneFreq"] = "88.5"
    df["DtcsCode"] = "023"
    df["DtcsPolarity"] = "NN"
    df["TStep"] = "5.00"
    
    # The following columns are null
    for col in ["Skip", "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE"]:
        df[col] = None

    # Most radios don't have a channel 0, so start the index at 1
    df.index = range(1, len(df) + 1)
    df.index.name = "Location"

    # Order columns as Chirp expects
    df = df[[
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
    ]]

    return df


if __name__ == "__main__":

    with open("repeaters.md", "r") as f:
        df = parse_markdown_table(f.read())

    print(df["Mode"].value_counts())
    print(f"Total: {len(df)}")

    df = format_df_for_chirp(df)
    df.to_csv("assets/rr_frequencies.csv")
