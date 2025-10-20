import argparse
import csv
import math
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import requests

from markdown_files import (
    write_index_md,
    write_map_md,
    write_repeaters_md,
    write_rules_md,
)
from programming_files import (
    write_chirp_csv,
    write_generic_csv,
)


def parse_args() -> argparse.Namespace | SimpleNamespace:
    """
    Parse arguments, either from command-line or from interactive input.

    Returns
    -------
    Union[argparse.Namespace, SimpleNamespace]
        A namespace object containing the arguments.
    """
    # If the script is called with no arguments, get them interactively
    if len(sys.argv) == 1:
        name = input("Group Name: ") or None
        loc = input("Location: ") or None
        state_id = input("RepeaterBook State ID: ") or None
        id = input("RepeaterBook ID: ") or None
        wwara_csv = input("WWARA CSV: ") or None
        prior_json = input("Prior JSON: ") or None
        call = input("Callsign: ") or None
        freq = input("Frequency (MHz): ") or None
        offset = input("Offset (MHz): ") or None
        tone = input("Tone (Hz): ") or None
        mode = input("Mode [FM]: ") or "FM"
        lat = input("Latitude: ") or None
        lon = input("Longitude: ") or None
        long_name = input("Long Name: ") or None
        url = input("Website: ") or None
        exclude = input("Exclude from contest: ") or None

        args = {
            "name": name,
            "loc": loc,
            "state_id": state_id,
            "id": id,
            "wwara_csv": wwara_csv,
            "prior_json": prior_json,
            "call": call,
            "freq": freq,
            "offset": offset,
            "tone": tone,
            "mode": mode,
            "lat": lat,
            "lon": lon,
            "long_name": long_name,
            "url": url,
            "exclude": exclude,
            "regen": False,
            "score": False,
        }

        return SimpleNamespace(**args)

    # Otherwise, parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default=None)
    parser.add_argument("--loc", type=str, default=None)
    parser.add_argument("--state_id", type=str, default="53")  # WA
    parser.add_argument("--id", type=str, default=None)
    parser.add_argument("--wwara_csv", type=str, default=None)
    parser.add_argument("--prior_json", type=str, default=None)
    parser.add_argument("--call", type=str, default=None)
    parser.add_argument("--freq", type=str, default=None)
    parser.add_argument("--offset", type=str, default=None)
    parser.add_argument("--tone", type=str, default=None)
    parser.add_argument("--mode", type=str, default="FM")
    parser.add_argument("--lat", type=float, default=None)
    parser.add_argument("--lon", type=float, default=None)
    parser.add_argument("--long_name", type=str, default=None)
    parser.add_argument("--url", type=str, default=None)
    parser.add_argument("--exclude", action="store_true")
    parser.add_argument("--regen", action="store_true")
    parser.add_argument("--score", action="store_true")
    return parser.parse_args()

def repeaters_from_wwara(csv_file: str, call: str) -> list[dict]:
    if csv_file is None or call is None:
      return []

    with open(csv_file, 'r') as f:
        lines = f.readlines()
    return wwara_find(lines, call)

def wwara_find(lines, call):
    if lines[0].startswith('DATA_SPEC_VERSION'):
        del lines[0]

    # Return records matching CALL.
    repeaters = []
    reader = csv.DictReader(lines)
    for row in reader:
        if row["CALL"] != call:
            continue

        if row["FM_WIDE"] != "Y" and row["FM_NARROW"] != "Y":
            continue

        repeaters.append(wwara_row_to_repeater(row))

    return repeaters

def find_by_call_freq(repeaters: pd.DataFrame, call: str, outp: str) -> list[dict]:
    if repeaters is None or repeaters.empty:
        return []
    recs = repeaters[
        (repeaters["Callsign"] == call) &
        (repeaters["Output (MHz)"] == outp)
    ]
    return [
        {key: r[key] for key in ["Group Name", "Long Name", "Website"]}
        for _, r in recs.iterrows()
    ]

def wwara_row_to_repeater(row: dict) -> dict:
    outp = float(row["OUTPUT_FREQ"])
    inp  = float(row["INPUT_FREQ"])
    offset = inp - outp
    if row["FM_WIDE"].strip() == "Y":
        mode = "FM"
    elif row["FM_NARROW"].strip() == "Y":
        mode = "NBFM[^nbfm]"
    else:
        raise NotImplementedError(f"Could not determine mdoe: {repr(row)}")

    return {
        "Long Name": row["SPONSOR"].strip(),
        "Callsign": row["CALL"].strip(),
        "Location": f"{row["CITY"].strip()}, {row["STATE"].strip()}",
        "Mode": mode,
        "Output (MHz)": '%0.3f' % outp,
        "Offset (MHz)": '%0.1f' % offset,
        "Tone (Hz)": row["CTCSS_IN"].strip(),
        "Coordinates": [float(row["LATITUDE"].strip()), float(row["LONGITUDE"].strip())],
        "Mode": mode,
        "Website": row["URL"].strip(),
    }


def repeater_from_repeaterbook(state_id_code: str, id_code: str) -> dict:
    """
    Extract a bunch of repeater information from RepeaterBook.

    Parameters
    ----------
    state_id_code : str
        The State ID code from RepeaterBook.

    id_code : str
        The ID code from RepeaterBook.

    Returns
    -------
    Dict
        A dict containing repeater information.
    """
    # If no ID is provided, don't get any info from RepeaterBook
    if state_id_code is None or id_code is None:
        return {}

    # Otherwise, grab repeater info
    url = f"https://www.repeaterbook.com/repeaters/details.php?state_id={state_id_code}&ID={id_code}"
    source = requests.get(url)

    # Extract various pieces of information
    start = r"\:\<\/td\>\s+\<td\>(?:\s*(?:\<!--.*?--\>|\<span[^\>]*\>))*\s*"
    end = r"(?:\s*\</span\>)*\s*\<\/td\>"

    call = re.search(r"callResult.php\?call=(\w{4,6})", source.text).group(1)

    freq = re.search(rf"Downlink{start}(\d+\.\d+){end}", source.text).group(1)
    freq = f"{float(freq):.04f}"
    if freq[-1] == "0":
        freq = freq[:-1]

    offset = re.search(rf"Offset{start}([\+\-]\d+\.\d+)\s*MHz{end}", source.text).group(1)
    offset = f"{float(offset):.01f}"
    if offset[0] != "-":
        offset = f"+{offset}"

    lat = re.search(r"center: \[(\-?\d+\.\d+)\,", source.text).group(1)
    long = re.search(r"center: \[\-?\d+\.\d+\,\s+(\-?\d+\.\d+)\]", source.text).group(1)
    latlong = [float(lat), float(long)]

    try:
        tone = re.search(rf"Uplink Tone{start}(\d+\.\d+){end}", source.text).group(1)
    except AttributeError:
        tone = ""

    repeater = {
        "Callsign": call,
        "Output (MHz)": freq,
        "Offset (MHz)": offset,
        "Tone (Hz)": tone,
        "Coordinates": latlong,
        "RepeaterBook State ID": state_id_code,
        "RepeaterBook ID": id_code,
    }

    return repeater


def repeater_from_args(args: argparse.Namespace | SimpleNamespace) -> dict:
    """
    Clean up user input and return a dictionary of repeater information.

    Parameters
    ----------
    args : Union[argparse.Namespace, SimpleNamespace]
        Arguments from the command line or user input.

    Returns
    -------
    Dict
        A dict containing repeat information.
    """
    repeater = {
        "Group Name": args.name,
        "Callsign": args.call,
        "Location": args.loc,
        "Mode": args.mode,
        "Output (MHz)": args.freq,
        "Offset (MHz)": args.offset,
        "Tone (Hz)": args.tone,
        "Coordinates": [float(args.lat), float(args.lon)] if args.lat and args.lon else None,
        "Long Name": args.long_name,
        "Website": args.url,
        "Exclude": args.exclude,
    }

    # Remove any empty values
    repeater = {key: val for key, val in repeater.items() if val}
    return repeater


def generate_repeater_df(
    args: argparse.Namespace | SimpleNamespace,
) -> pd.DataFrame:
    """
    Create a DataFrame of repeaters from known repeaters combined with user input.

    Parameters
    ----------
    args : Union[argparse.Namespace, SimpleNamespace]
        User input from the command line or interactive input.

    Returns
    -------
    pd.DataFrame
        A dataframe of known repeaters from assets/repeaters.json
        combined with a new repeater taken from user input.
    """
    if args.regen or args.score:
        df = pd.read_json("assets/repeaters.json", dtype=False)
        df.to_json("assets/repeaters.json", orient="records", indent=4)
        df["RR#"] = df.index + 1
        return df

    if args.prior_json:
        prior_repeaters = pd.read_json(args.prior_json, dtype=False)

    # Combine RepeaterBook and WWARA info with user input
    wwaras = repeaters_from_wwara(args.wwara_csv, args.call)
    if args.freq:
        freq = float(freq)
        wwaras = [r for r in wwaras if math.isclose(float(r["Output (MHz)"]), freq, abs_tol=0.001)][0:1]
    if not wwaras:
        # Ensure we provide at least one record to combine with RepeaterBook and CLI args.
        wwaras = [{}]

    def prior_year(repeaters, r):
        rpts = find_by_call_freq(repeaters, r["Callsign"], r["Output (MHz)"])
        return rpts[0] if rpts else {}

    repeaterbook = repeater_from_repeaterbook(args.state_id, args.id)
    repeaterargs = repeater_from_args(args)
    repeaters = pd.DataFrame.from_records(
        [{**repeaterbook, **r, **prior_year(prior_repeaters, r), **repeaterargs} for r in wwaras])

    # Combine with known repeaters
    if not Path("assets/repeaters.json").exists():
        with open("assets/repeaters.json", "w") as f:
            f.write("{}")
    df = pd.read_json("assets/repeaters.json", dtype=False)

    # Initialize records missing state id fields to WA (53).
    if "RepeaterBook State ID" not in df.columns:
        df["RepeaterBook State ID"] = None

    def init_state_id(row):
        if pd.notna(row["RepeaterBook State ID"]):
            return row["RepeaterBook State ID"]
        if pd.isna(row["RepeaterBook ID"]):
            return None
        return "53"

    df["RepeaterBook State ID"] = df.apply(init_state_id, axis=1)

    df = pd.concat([df, repeaters], ignore_index=True)

    # Save a new known repeaters file
    df = df.reset_index(drop=True)
    df.to_json("assets/repeaters.json", orient="records", indent=4)

    # Assign a Repeater Roundabout number to each repeater
    # This shouldn't be in the .json because it's not a repeater attribute
    # and would cause issues grouping or reordering repeaters
    df["RR#"] = df.index + 1

    return df


def remove_df_footnotes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return dataframe with Mode column footnotes removed.
    """
    return df.assign(Mode=df["Mode"].str.replace(r"\[.+\]", "", regex=True))


if __name__ == "__main__":
    args = parse_args()

    df = generate_repeater_df(args)
    write_index_md(df, args.score)
    write_repeaters_md(df)
    write_rules_md(df)
    write_map_md(df)

    df = remove_df_footnotes(df)
    write_chirp_csv(df)
    # write_icom_csv(df)
    # write_d878_zip(df)
    write_generic_csv(df)
