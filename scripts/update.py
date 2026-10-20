import argparse
import csv
import json
import math
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import requests

from markdown_files import (
    STATUS_IN,
    STATUS_OUT,
    STATUS_RESPONSE_NEEDED,
    write_group_pages,
    write_index_md,
    write_map_md,
    write_repeaters_md,
    write_rules_md,
)
from programming_files import (
    write_chirp_csv,
    write_generic_csv,
    write_icom_csv,
    write_d878_zip,
)

REPEATERS_JSON = "assets/repeaters.json"
FORMS_JSON = "assets/forms.json"

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
        mode = input("Mode [FM]: ") or None
        lat = input("Latitude: ") or None
        lon = input("Longitude: ") or None
        long_name = input("Long Name: ") or None
        url = input("Website: ") or None
        internet_contacts = input("Allow Internet Contacts: ") or None
        internet_access = input("Internet Access: ") or None

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
            "internet_contacts": internet_contacts,
            "internet_access": internet_access,
            "regen": False,
            "status": None,
            "score": False,
            "rollover": False,
            "update_all": False,
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
    parser.add_argument("--mode", type=str, default=None)
    parser.add_argument("--lat", type=float, default=None)
    parser.add_argument("--lon", type=float, default=None)
    parser.add_argument("--long_name", type=str, default=None)
    parser.add_argument("--url", type=str, default=None)
    parser.add_argument("--internet_contacts", type=str, default=None)
    parser.add_argument("--internet_access", type=str, default=None)
    parser.add_argument("--regen", action="store_true")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--score", action="store_true")
    mode.add_argument("--rollover", action="store_true")
    mode.add_argument("--status", choices=[STATUS_IN, STATUS_OUT, STATUS_RESPONSE_NEEDED])
    mode.add_argument("--update_all", action="store_true")
    return parser.parse_args()

def repeaters_from_wwara(csv_file: str, call: str) -> pd.DataFrame:
    """
    Return all repeaters with a given callsign from WWARA CSV file.

    Parameters
    ----------
    csv_file : str
        Path to a WWARA CSV export file.

    call : str
        Repeater callsign.

    Returns
    -------
    pd.DataFrame
        A dataframe of repeaters matching the call found in the CSV file.
    """
    if csv_file is None or call is None:
      return []

    with open(csv_file, 'r') as f:
        lines = f.readlines()
    return wwara_find(lines, call)

def wwara_find(lines: list[str], call: str) -> pd.DataFrame:
    """
    Return all repeaters with a given callsign from WWARA CSV contents.

    Parameters
    ----------
    lines : list[str]
        Contents of a WWARA CSV export file.

    call : str
        Repeater callsign.

    Returns
    -------
    pd.DataFrame
        A dataframe of repeaters matching the call.
    """
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

    return pd.DataFrame.from_records(repeaters)

def wwara_row_to_repeater(row: dict) -> dict:
    """
    Convert a single WWARA CSV row to a repeater record.

    Parameters
    ----------
    row : dict
        A single CSV row from a WWARA exportfile.

    Returns
    -------
    dict
        A repeater record.
    """
    outp = float(row["OUTPUT_FREQ"])
    inp  = float(row["INPUT_FREQ"])
    offset = inp - outp
    if row["FM_WIDE"].strip() == "Y":
        mode = "FM"
    elif row["FM_NARROW"].strip() == "Y":
        mode = "NBFM[^nbfm]"
    else:
        raise NotImplementedError(f"Could not determine mode: {repr(row)}")

    return {
        "Long Name": row["SPONSOR"].strip(),
        "Callsign": row["CALL"].strip(),
        "Location": f"{row["CITY"].strip()}, {row["STATE"].strip()}",
        "Mode": mode,
        "Output (MHz)": '%0.4f' % outp,
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
    start = r".*?</th>.*?<td>(?:\s*(?:\<!--.*?-->|<span[^>]*>))*\s*"

    call_match = re.search(r"callResult.php\?call=(\w{4,6})", source.text)
    if not call_match:
        print(f"Could not find call in {url}", file=sys.stderr)
        return {}

    call = call_match.group(1)

    freq_match = re.search(rf"Downlink{start}(\d+\.\d+)", source.text, re.DOTALL)
    if not freq_match:
        print(f"Could not find downlink in {url}", file=sys.stderr)
        return {}

    freq = freq_match.group(1)
    freq = f"{float(freq):.04f}"
    if freq[-1] == "0":
        freq = freq[:-1]

    offset_match = re.search(rf"Offset{start}([+-]\d+\.\d+)", source.text, re.DOTALL)
    if not offset_match:
        print(f"Could not find offset in{url}", file=sys.stderr)
        return {}

    offset = offset_match.group(1)
    offset = f"{float(offset):.01f}"
    if offset[0] != "-":
        offset = f"+{offset}"

    lat_match = re.search(r"L\.circle\(\s*\[(-?\d+\.\d+)\s*,", source.text)
    if not lat_match:
        print(f"Could not find lat in{url}", file=sys.stderr)
        return {}

    lat = lat_match.group(1)
    long_match = re.search(r"L\.circle\([^,]+,\s*(-?\d+\.\d+)", source.text)
    if not long_match:
        print(f"Could not find long in{url}", file=sys.stderr)
        return {}

    long = long_match.group(1)
    latlong = [float(lat), float(long)]

    tone_match = re.search(rf"Uplink Tone{start}(\d+\.\d+)", source.text, re.DOTALL)
    if tone_match:
        tone = tone_match.group(1)
    else:
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

def strip_empty(d: dict) -> dict:
    """
    Removes all empty or NA values from dict.
    """
    return {key: val for key, val in d.items() if val and (not np.isscalar(val) or pd.notna(val))}

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
        A dict containing repeater information.
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
        "Allow Internet Contacts": args.internet_contacts,
        "Internet Access": args.internet_access,
    }

    # Remove any empty values
    repeater = strip_empty(repeater)
    return repeater

def freq_match(a, b) -> bool:
    """
    Returns true if two frequency values in MHz differ by less than than 1 kHz.

    Parameters
    ----------
    a, b : anything that can be converted to float.
        The frequencies to compare.

    Returns
    -------
    bool
        True if the frequencies are the same.
    """
    return math.isclose(float(a), float(b), abs_tol=0.001)

def filter_freq(df: pd.DataFrame, freq: float) -> pd.DataFrame:
    """
    Returns a DataFrame with only records matching the given frequency.

    Parameters
    ----------
    df : pd.DataFrame
        Repeater records to filter.

    freq : float
        The frequency to match.

    Returns
    -------
    pd.DataFrame
        Records from df matching freq.
    """
    return df.loc[df["Output (MHz)"].map(lambda f: freq_match(freq, f))]

def first_dict(df: pd.DataFrame) -> dict:
    """
    A convenience function to return the first record (if any) as a dictionary.
    If the DataFrame is empty, return {}.  Logically, it is [].get(0, {}) for DataFrames.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of records.

    Returns
    -------
    dict
        A record from the first row of the DataFrame, or {} if the DataFrame is empty.
    """
    if df is None or df.empty:
        return {}
    return df.iloc[0].to_dict()

def merge_repeaters(repeaterbook: dict = {}, args: dict = {}, wwara: dict = {}, prior: dict = {}) -> dict:
    """
    Merges repeater information from multiple sources. If a field is specified by more than
    one source, the first source to specify the value in order of decreasing prioirty will
    be used.  For most fileds, the priority order is: args, wwara, repeaterbook, prior.  For
    Group Name, Long Name, Location, and Website fields, the priority order is:
    args, prior, wwara, repeaterbook.

    Parameters
    ----------
    repeaterbook : dict
        A repeater record from RepeaterBook.

    args : dict
        A repeater record from command line arguments.

    wwara : dict
        A repeater record from WWARA.

    prior : dict
        A repeater record from Repeater Roundabout repeaters.json file.

    Returns
    -------
    dict
        A merged repeater record.
    """
    # Remove all empty values.
    repeaterbook = strip_empty(repeaterbook)
    args = strip_empty(args)
    wwara = strip_empty(wwara)
    prior = strip_empty(prior)

    r = {**prior, **repeaterbook, **wwara, **args}

    # Prioritize past data for specific fields.
    for f in ["Group Name", "Location", "Long Name", "Website"]:
        r[f] = args.get(f) or prior.get(f) or wwara.get(f) or repeaterbook.get(f)

    # Default to FM when no source specifies a mode.
    r["Mode"] = r.get("Mode") or "FM"

    # A newly added repeater hasn't been confirmed for this year, whatever its prior status
    r.pop("Exclude", None)
    r["Status"] = STATUS_RESPONSE_NEEDED

    return r

def refresh_repeater(repeaterbook: dict = {}, wwara: dict = {}, prior: dict = {}) -> dict:
    """
    Like merge_repeaters, but for refreshing an already-known repeater: Status and Exclude
    are left as they were in `prior`, since re-fetching source data shouldn't affect contest
    participation state.
    """
    # An explicit empty tone from RepeaterBook means "confirmed toneless", not "no data";
    # strip_empty would otherwise drop it and leave a stale prior tone in place.
    repeaterbook_toneless = repeaterbook.get("Tone (Hz)") == ""

    repeaterbook = strip_empty(repeaterbook)
    wwara = strip_empty(wwara)
    prior = strip_empty(prior)

    r = {**prior, **repeaterbook, **wwara}
    if repeaterbook_toneless and "Tone (Hz)" not in wwara:
        r["Tone (Hz)"] = ""
    for f in ["Group Name", "Location", "Long Name", "Website"]:
        r[f] = prior.get(f) or wwara.get(f) or repeaterbook.get(f)
    return r


def update_all_repeaters(df: pd.DataFrame, wwara_csv: str | None) -> tuple[pd.DataFrame, list[str]]:
    """
    Refresh every repeater in df from RepeaterBook (using its recorded state/ID) and, if
    wwara_csv is given, from WWARA (matched by callsign and frequency). Repeaters with
    neither a RepeaterBook ID nor a WWARA match are left unchanged.

    Returns the updated DataFrame and a list of error messages, one per repeater that
    failed to refresh; those repeaters are left unchanged in the result.
    """
    errors = []
    rows = []
    wwara_lines = None
    if wwara_csv:
        with open(wwara_csv) as f:
            wwara_lines = f.readlines()

    for _, row in df.iterrows():
        prior = row.to_dict()
        call = prior.get("Callsign")
        freq = prior.get("Output (MHz)")
        label = f"{call or '?'} {freq or ''}".strip()
        try:
            repeaterbook = {}
            state_id, rb_id = prior.get("RepeaterBook State ID"), prior.get("RepeaterBook ID")
            if pd.notna(state_id) and pd.notna(rb_id):
                repeaterbook = repeater_from_repeaterbook(str(state_id), str(rb_id))
                if not repeaterbook:
                    raise RuntimeError(f"RepeaterBook lookup failed for state_id={state_id} id={rb_id}")

            wwaras = pd.DataFrame()
            if wwara_lines and call:
                wwaras = wwara_find(wwara_lines, call)
                ensure_col(wwaras, "Output (MHz)")
                if freq and not wwaras.empty:
                    wwaras = filter_freq(wwaras, freq)

            rows.append(refresh_repeater(repeaterbook=repeaterbook, wwara=first_dict(wwaras), prior=prior))
        except Exception as e:
            errors.append(f"{label}: {e}")
            rows.append(prior)

    return pd.DataFrame.from_records(rows), errors


def ensure_col(df: pd.DataFrame, name: str, default=np.nan) -> pd.DataFrame:
    """
    A convenience function to ensure a dataframe has a given column.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to modify.

    name : str
        The column name.

    default : any
        An optional default value to assign to the column (np.nan if not specified).

    Returns
    -------
    pd.DataFrame
        The input DataFrame with the named column added, if one was not already present.
    """
    if name not in df.columns:
        df[name] = default

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
        df = pd.read_json(REPEATERS_JSON, dtype=False)
        df.to_json(REPEATERS_JSON, orient="records", indent=4)
        df["RR#"] = df.index + 1
        return df

    call = args.call
    freq = float(args.freq) if args.freq else None

    repeaterbook = repeater_from_repeaterbook(args.state_id, args.id)
    if repeaterbook:
        if call and call != repeaterbook["Callsign"]:
            raise f"Callsign mismatch: args={args.call}, repeaterbook={repeaterbook["Callsign"]}"
        if not call:
            call = repeaterbook["Callsign"]

        if freq and not freq_match(freq, float(repeaterbook["Output (MHz)"])):
            raise f"Frequency mismatch: args={args.freq}, repeaterbook={repeaterbook["Output (MHz)"]}"
        if not freq:
            freq = float(repeaterbook["Output (MHz)"])

    if not call:
        raise "Could not determine callsign!"

    priors = pd.DataFrame(columns=["Output (MHz)"])
    if args.prior_json:
        priors = pd.read_json(args.prior_json, dtype=False)
        priors = priors[priors["Callsign"] == call]
    if freq and not priors.empty:
        priors = filter_freq(priors, freq)

    wwaras = repeaters_from_wwara(args.wwara_csv, call)
    ensure_col(wwaras, "Output (MHz)")
    if freq and not wwaras.empty:
        wwaras = filter_freq(wwaras, freq)

    repeaterargs = repeater_from_args(args)

    if freq:
        frequencies = [float(freq)]
    else:
        frequencies = list(set([
            float(f) for f in priors["Output (MHz)"].to_list() +
                 wwaras["Output (MHz)"].to_list() +
                 [repeaterargs.get("Output (MHz)")] +
                 [repeaterbook.get("Output (MHz)")]
            if f
        ]))
    frequencies.sort()

    # Combine RepeaterBook and WWARA info with user input.
    repeaters = pd.DataFrame.from_records(
        [
            merge_repeaters(repeaterbook=repeaterbook,
                            args=repeaterargs,
                            wwara=first_dict(filter_freq(wwaras, f)),
                            prior=first_dict(filter_freq(priors, f)))
            for f in frequencies
        ])

    # Combine with known repeaters
    if not Path(REPEATERS_JSON).exists():
        with open(REPEATERS_JSON, "w") as f:
            f.write("{}")
    df = pd.read_json(REPEATERS_JSON, dtype=False)

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
    df.to_json(REPEATERS_JSON, orient="records", indent=4)

    # Assign a Repeater Roundabout number to each repeater
    # This shouldn't be in the .json because it's not a repeater attribute
    # and would cause issues grouping or reordering repeaters
    df["RR#"] = df.index + 1

    return df


DATE_FILES = ["assets/templates/index.md", "assets/templates/rules.md", "logging.md"]


def rollover(now: datetime | None = None) -> None:
    """
    Archive last year's contest into a directory named for that year.

    Copies assets/repeaters.json to <year>/repeaters.json and moves results/*.csv to
    <year>/results/, where <year> is the year before `now` (default: the current time).
    Exits non-zero without changing anything if <year>/ already exists.
    """
    year = (now or datetime.now()).year - 1
    archive = Path(str(year))
    if archive.exists():
        sys.exit(f"{archive}/ already exists; refusing to overwrite an existing archive.")

    repeaters = Path(REPEATERS_JSON).read_bytes()  # fail before creating the archive
    (archive / "results").mkdir(parents=True)
    (archive / "repeaters.json").write_bytes(repeaters)
    for file in Path("results").glob("*.csv"):
        shutil.move(file, archive / "results" / file.name)

    # Every repeater must be confirmed again for the new contest
    df = pd.read_json(REPEATERS_JSON, dtype=False)
    df["Status"] = STATUS_RESPONSE_NEEDED
    df.to_json(REPEATERS_JSON, orient="records", indent=4)


def find_repeater(df: pd.DataFrame, call: str, freq: str | None) -> int:
    """
    Return the index of the repeater matching call (and freq, if given).

    Raises ValueError unless exactly one repeater matches.
    """
    match = df["Callsign"].str.upper() == call.upper()
    if freq:
        match &= df["Output (MHz)"].map(lambda f: freq_match(freq, f))
    if match.sum() != 1:
        raise ValueError(f"Expected one repeater matching {call} {freq or ''}, found {match.sum()}")
    return df.index[match][0]


def update_fields(df: pd.DataFrame, call: str, freq: str | None, fields: dict) -> pd.DataFrame:
    """
    Return df with the repeater matching call (and freq, if given) overwritten with fields.

    Raises ValueError unless exactly one repeater matches.
    """
    df = df.reset_index(drop=True)
    i = find_repeater(df, call, freq)
    for col, val in fields.items():
        df.at[i, col] = val
    return df


def set_status(df: pd.DataFrame, call: str, freq: str | None, status: str) -> pd.DataFrame:
    """
    Return df with the status of the repeater matching call (and freq, if given) changed.

    A repeater's position is its RR#, so moves are limited to repeaters whose numbers
    haven't been published: one going from response needed to in moves to just after
    the last repeater that's in, and one going from response needed to out moves to the
    end. Any other change leaves it where it is. A missing status counts as response needed.

    Raises ValueError unless exactly one repeater matches.
    """
    df = df.reset_index(drop=True)
    i = find_repeater(df, call, freq)
    old = df.at[i, "Status"] if pd.notna(df.at[i, "Status"]) else STATUS_RESPONSE_NEEDED
    df.at[i, "Status"] = status
    if old != STATUS_RESPONSE_NEEDED or status == STATUS_RESPONSE_NEEDED:
        return df

    row, rest = df.loc[[i]], df.drop(index=i).reset_index(drop=True)
    if status == STATUS_OUT:
        at = len(rest)
    else:
        confirmed = rest.index[rest["Status"] == STATUS_IN]
        at = confirmed[-1] + 1 if len(confirmed) else 0
    return pd.concat([rest.iloc[:at], row, rest.iloc[at:]], ignore_index=True)


def update_status_and_fields(
    df: pd.DataFrame, call: str, freq: str | None, status: str, fields: dict
) -> pd.DataFrame:
    """
    Set a repeater's status and, if given, its other fields in one call.

    call and freq are only used to locate the repeater; any Callsign/Output (MHz)
    in `fields` is ignored so the match keys the user typed don't clobber the
    stored values. Raises ValueError unless exactly one repeater matches.
    """
    df = set_status(df, call, freq, status)
    fields = {k: v for k, v in fields.items() if k not in ("Callsign", "Output (MHz)")}
    if fields:
        df = update_fields(df, call, freq, fields)
    return df


def remove_df_footnotes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return dataframe with Mode column footnotes removed.
    """
    return df.assign(Mode=df["Mode"].str.replace(r"\[.+\]", "", regex=True))


if __name__ == "__main__":
    args = parse_args()
    if args.rollover:
        rollover()
        args.regen = True
    if args.status:
        repeaters = pd.read_json(REPEATERS_JSON, dtype=False)
        try:
            repeaters = update_status_and_fields(
                repeaters, args.call or "", args.freq, args.status, repeater_from_args(args)
            )
        except ValueError as e:
            sys.exit(str(e))
        repeaters.to_json(REPEATERS_JSON, orient="records", indent=4)
        args.regen = True
    if args.update_all:
        repeaters = pd.read_json(REPEATERS_JSON, dtype=False)
        repeaters, errors = update_all_repeaters(repeaters, args.wwara_csv)
        repeaters.to_json(REPEATERS_JSON, orient="records", indent=4)
        if errors:
            print(f"{len(errors)} repeater(s) failed to update:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
        args.regen = True

    df = generate_repeater_df(args)
    ensure_col(df, "Status", STATUS_RESPONSE_NEEDED)
    df["Status"] = df["Status"].fillna(STATUS_RESPONSE_NEEDED)
    with open(FORMS_JSON) as f:
        write_group_pages(remove_df_footnotes(df), json.load(f))

    # Only publish repeaters confirmed for this contest
    df = df.loc[df["Status"] == STATUS_IN]

    # Set tone to the empty string for toneless repeaters.  Downstream
    # code assumes tone is always a string.
    no_tone = df["Tone (Hz)"].isna() | (df["Tone (Hz)"] == "")
    df.loc[no_tone, "Tone (Hz)"] = ""

    write_index_md(df, args.score)
    write_repeaters_md(df)
    write_rules_md(df)
    write_map_md(df)

    df = remove_df_footnotes(df)
    write_chirp_csv(df)
    write_icom_csv(df)
    write_d878_zip(df)
    write_generic_csv(df)

    if args.rollover:
        print("Rolled over. Now update the contest dates by hand in: " + ", ".join(DATE_FILES))
