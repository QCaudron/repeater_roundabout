import argparse
import re
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Union

import pandas as pd
import numpy
import requests

from markdown_files import (
    write_index_md,
    write_map_md,
    write_repeaters_md,
    write_rules_md,
)
from programming_files import (
    write_chirp_csv,
    write_d878_zip,
    write_generic_csv,
    write_icom_csv,
)


def parse_args() -> Union[argparse.Namespace, SimpleNamespace]:
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
    parser.add_argument("--state_id", type=str, default='53')  # WA
    parser.add_argument("--id", type=str, default=None)
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

    lat = re.search(rf"center: \[(\-?\d+\.\d+)\,", source.text).group(1)
    long = re.search(rf"center: \[\-?\d+\.\d+\,\s+(\-?\d+\.\d+)\]", source.text).group(1)
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


def repeater_from_args(args: Union[argparse.Namespace, SimpleNamespace]) -> dict:
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

def generate_repeater_df(args: Union[argparse.Namespace, SimpleNamespace]) -> pd.DataFrame:
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

    # Combine RepeaterBook info with user input
    repeaterbook = repeater_from_repeaterbook(args.state_id, args.id)
    repeaterargs = repeater_from_args(args)
    repeater = pd.DataFrame.from_records([{**repeaterbook, **repeaterargs}])

    # Combine with known repeaters
    if not Path("assets/repeaters.json").exists():
        with open("assets/repeaters.json", "w") as f:
            f.write("{}")
    df = pd.read_json("assets/repeaters.json", dtype=False)

    # Initialize records missing state id fields to WA (53).
    if 'RepeaterBook State ID' not in df.columns:
        df['RepeaterBook State ID'] = numpy.NaN

    def init_state_id(row):
        if pd.notna(row['RepeaterBook State ID']):
            return row['RepeaterBook State ID']
        if pd.isna(row['RepeaterBook ID']):
            return numpy.NaN
        return '53'
    df['RepeaterBook State ID'] = df.apply(init_state_id, axis=1)
    
    df = pd.concat([df, repeater], ignore_index=True)

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
