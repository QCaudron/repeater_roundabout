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
        repeaters_file = input("Repeaters file (one 'CALL 146.860- T123.0' per line): ") or None

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
            "repeaters": None,
            "repeaters_file": repeaters_file,
            "regen": False,
            "status": None,
            "score": False,
            "rollover": False,
            "update_all": False,
            "check": False,
            "status_csv": None,
            "repeater_csv": None,
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
    parser.add_argument("--repeaters", type=str, default=None,
                        help="Batch-add repeaters, one per line, e.g. '- WA7SAR 146.860- T123.0'; "
                             "other flags (--name, --wwara_csv, ...) apply to each")
    parser.add_argument("--repeaters_file", type=str, default=None,
                        help="Like --repeaters, but read the lines from a file")
    parser.add_argument("--regen", action="store_true")
    parser.add_argument("--status", choices=[STATUS_IN, STATUS_OUT, STATUS_RESPONSE_NEEDED],
                         help="Set status on the repeater(s) touched by this run "
                              "(single repeater, or every row of --repeater_csv)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--score", action="store_true")
    mode.add_argument("--rollover", action="store_true")
    mode.add_argument("--update_all", action="store_true")
    mode.add_argument("--check", action="store_true",
                      help="Report data inconsistencies in repeaters.json (read-only)")
    mode.add_argument("--status_csv", type=str, default=None,
                       help="Club survey CSV: bulk-update status/callsign/tone/internet-access")
    mode.add_argument("--repeater_csv", type=str, default=None,
                       help="Single-repeater submission CSV: add or edit one repeater per row")
    args = parser.parse_args()
    if args.status and (args.score or args.rollover or args.update_all or args.status_csv or args.check):
        parser.error("--status cannot be combined with --score/--rollover/--update_all/--status_csv/--check")
    return args

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
      return pd.DataFrame(columns=["Output (MHz)"])

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

    location = parse_repeaterbook_location(source.text)
    if location:
        repeater["Location"] = location

    return repeater


def parse_repeaterbook_location(html: str) -> str | None:
    """
    Extract "City, State" from a RepeaterBook details page's
    "City • County • State" line, or None if not present.
    """
    match = re.search(r'MHz.*?<p class="mb-0 text-body-secondary">(.*?)</p>', html, re.DOTALL)
    if not match:
        return None
    parts = [p.strip() for p in match.group(1).split("•")]
    if len(parts) < 2:
        return None
    return f"{parts[0]}, {parts[-1]}"

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
        "Status": args.status,
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

# ponytail: US band-plan defaults only; coordination exceptions need an explicit offset
BAND_OFFSETS = [(50, 54, 1.7), (144, 148, 0.6), (222, 225, 1.6), (420, 450, 5.0), (902, 928, 25.0)]


def default_offset(freq) -> float | None:
    """Standard repeater offset magnitude (MHz) for the band containing freq, or None."""
    try:
        f = float(freq)
    except (TypeError, ValueError):
        return None
    return next((o for lo, hi, o in BAND_OFFSETS if lo <= f < hi), None)


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

    # A bare "+"/"-" (from --repeaters lines) gives only the direction: take the magnitude
    # from the other sources, else the usual offset for the band.
    if args.get("Offset (MHz)") in ("+", "-"):
        known = next((o for o in (wwara.get("Offset (MHz)"), repeaterbook.get("Offset (MHz)"),
                                  prior.get("Offset (MHz)")) if o), None)
        magnitude = abs(float(known)) if known else default_offset(args.get("Output (MHz)"))
        r["Offset (MHz)"] = f"{args['Offset (MHz)']}{magnitude:.1f}" if magnitude else None

    # Prioritize past data for specific fields.
    for f in ["Group Name", "Location", "Long Name", "Website"]:
        r[f] = args.get(f) or prior.get(f) or wwara.get(f) or repeaterbook.get(f)

    # Default to FM when no source specifies a mode.
    r["Mode"] = r.get("Mode") or "FM"

    # A newly added repeater hasn't been confirmed for this year, whatever its prior status,
    # unless the caller explicitly set one (e.g. --status).
    r.pop("Exclude", None)
    r["Status"] = args.get("Status") or STATUS_RESPONSE_NEEDED

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

    # Update existing repeaters in place by callsign+frequency; only add a new
    # row when no existing repeater matches. Status is left as-is on an update
    # so re-running update.py doesn't un-confirm an already-confirmed repeater.
    df = df.reset_index(drop=True)
    new_rows = []
    for _, r in repeaters.iterrows():
        record = strip_empty(r.to_dict())
        call, freq = record.get("Callsign"), record.get("Output (MHz)")
        match = pd.Series(False, index=df.index)
        if call and freq:
            match = (df["Callsign"].str.upper() == call.upper()) & \
                df["Output (MHz)"].map(lambda f: freq_match(freq, f))
        if match.any():
            i = df.index[match][0]
            for col, val in record.items():
                if col != "Status":
                    df.at[i, col] = val
            if args.status:
                df = set_status(df, call, freq, args.status)
        else:
            new_rows.append(record)

    if new_rows:
        df = pd.concat([df, pd.DataFrame.from_records(new_rows)], ignore_index=True)

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


def check_consistency(df: pd.DataFrame) -> list[str]:
    """
    Return a message for each inconsistency in the repeater list:

    - no Group Name, or Group Names differing only in case/whitespace
    - a group where some repeaters are in/out but others still need a response
    - duplicate callsign + output frequency
    - missing offset or mode, or an offset that isn't the band's standard
    - an "in" repeater listed after a "response needed" one (RR# is list position)
    - a Status that isn't in, out or response_needed

    A missing Status counts as response needed.
    """
    problems = []
    name = df["Group Name"].map(lambda n: n.strip() if isinstance(n, str) else "")
    status = df["Status"].fillna(STATUS_RESPONSE_NEEDED)
    label = df["Callsign"].astype(str) + " " + df["Output (MHz)"].astype(str)

    for lbl in label[name == ""]:
        problems.append(f"{lbl}: no Group Name")

    named = name != ""
    variants = df.loc[named, "Group Name"].groupby(name[named].str.casefold()).agg(lambda s: sorted(set(s)))
    for names in variants:
        if len(names) > 1:
            problems.append(f"Group Names differ only by case/whitespace: {names}")

    for g, rows in df[name != ""].groupby(name):
        s = status.loc[rows.index]
        pending = rows.loc[s == STATUS_RESPONSE_NEEDED, "Callsign"]
        if len(pending) and len(pending) < len(rows):
            decided = ", ".join(sorted(rows.loc[s != STATUS_RESPONSE_NEEDED, "Callsign"]))
            problems.append(f"{g}: response_needed for {', '.join(sorted(pending))}; decided: {decided}")

    freq = pd.to_numeric(df["Output (MHz)"], errors="coerce")
    key = df["Callsign"].astype(str).str.upper() + " " + freq.astype(str)
    for k in key[key.duplicated(keep=False)].unique():
        problems.append(f"duplicate repeater: {k}")

    for i, row in df.iterrows():
        if not str(row.get("Mode") or "").strip():
            problems.append(f"{label[i]}: no mode")
        offset = pd.to_numeric(row.get("Offset (MHz)"), errors="coerce")
        if pd.isna(offset):
            problems.append(f"{label[i]}: no offset")
        elif (expected := default_offset(row["Output (MHz)"])) is not None and abs(offset) != expected:
            problems.append(f"{label[i]}: odd offset {row['Offset (MHz)']} (band standard is {expected})")

    seen_pending = False
    for i, st in status.items():
        seen_pending |= st == STATUS_RESPONSE_NEEDED
        if st == STATUS_IN and seen_pending:
            problems.append(f"{label[i]}: out of order, 'in' listed after a repeater that needs a response")
        if st not in (STATUS_IN, STATUS_OUT, STATUS_RESPONSE_NEEDED):
            problems.append(f"{label[i]}: invalid status {st!r}")
    return problems


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


def update_status_and_fields_for_callsign(
    df: pd.DataFrame, call: str, freq: str | None, status: str, fields: dict
) -> pd.DataFrame:
    """
    Like update_status_and_fields, but if freq is None, updates every repeater with that callsign.

    Raises ValueError if no repeater matches.
    """
    if freq:
        return update_status_and_fields(df, call, freq, status, fields)
    freqs = df.loc[df["Callsign"].str.upper() == call.upper(), "Output (MHz)"].tolist()
    if not freqs:
        raise ValueError(f"No repeaters match callsign {call}")
    for f in freqs:
        df = update_status_and_fields(df, call, f, status, fields)
    return df


def find_col(fieldnames: list[str], *keywords: str) -> str:
    """
    Return the first fieldname matching all keywords (case-insensitive). A keyword
    prefixed with "^" must match the start of the fieldname; otherwise it may appear
    anywhere.

    Raises KeyError if no fieldname matches.
    """
    for name in fieldnames:
        low = name.lower()
        if all(low.startswith(k[1:].lower()) if k.startswith("^") else k.lower() in low for k in keywords):
            return name
    raise KeyError(f"no column matching {keywords!r} among {fieldnames!r}")


def looks_like_internet_id(s: str | None) -> bool:
    """
    Returns True if s looks like an actual Allstar/EchoLink/YSF/D-Star identifier
    (a node number, or an EchoLink-style "CALL-L") rather than a stray answer
    like "No" or "N/A".
    """
    if not s:
        return False
    s = s.strip()
    if not s or s.lower() in {"no", "n/a", "na", "none", "-"}:
        return False
    return bool(re.search(r"\d{3,}", s)) or bool(re.fullmatch(r"[A-Za-z0-9]{3,8}-[A-Za-z]", s))


REPEATER_LINE_RE = re.compile(
    r"(?P<call>[A-Za-z][A-Za-z0-9]{2,6})\s+(?P<freq>\d{2,4}\.\d{1,4})\s*(?P<sign>[+-])?\s*"
    r"(?:T\s*(?P<tone>\d{2,3}(?:\.\d)?)|(?P<dcs>D\d{2,3}[NI]?))?"
)


def parse_repeater_lines(text: str) -> list[dict]:
    """
    Loose-parse a free-form "Repeaters" cell (one repeater per line, e.g.
    "- WA7SAR 146.860- T123.0") into a list of {"Callsign", "Output (MHz)", "Tone (Hz)"}
    dicts. Lines that don't look like a repeater are skipped.
    """
    repeaters = []
    for line in (text or "").splitlines():
        m = REPEATER_LINE_RE.search(line)
        if not m:
            continue
        tone = m.group("tone") or m.group("dcs")
        repeaters.append({
            "Callsign": m.group("call").upper(),
            "Output (MHz)": m.group("freq"),
            "Tone (Hz)": tone,
            "Offset Sign": m.group("sign"),
        })
    return repeaters


def apply_status_csv(df: pd.DataFrame, csv_file: str) -> tuple[pd.DataFrame, list[str]]:
    """
    Bulk-update repeater status (in/out), callsign, tone, and internet-access fields from
    a club participation survey CSV: one row per club, with a free-form "Repeaters" cell
    listing the repeaters the club is responding for.

    Each listed repeater is matched within its club's existing repeaters by frequency
    (callsigns can drift, so frequency is the stable key). Repeaters that don't match
    exactly one existing entry are reported as errors and left unchanged.

    Returns the updated DataFrame and a list of error messages.
    """
    df = df.reset_index(drop=True)
    errors = []
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        group_col = find_col(reader.fieldnames, "club")
        answer_col = find_col(reader.fieldnames, "can repeater roundabout")
        repeaters_col = find_col(reader.fieldnames, "^repeaters")
        allow_col = find_col(reader.fieldnames, "allow contacts")
        info_col = find_col(reader.fieldnames, "echolink", "info")

        for row in reader:
            group = (row.get(group_col) or "").strip()
            status = STATUS_IN if (row.get(answer_col) or "").strip().lower().startswith("y") else STATUS_OUT
            allow = (row.get(allow_col) or "").strip()
            info = (row.get(info_col) or "").strip()
            # Overwrite, rather than strip_empty, so a club clearing their Allstar/Echolink
            # info (or answering "No") actually clears the stored value.
            common_fields = {
                "Allow Internet Contacts": allow,
                "Internet Access": info if looks_like_internet_id(info) else "",
            }

            for parsed in parse_repeater_lines(row.get(repeaters_col)):
                call, freq, tone = parsed["Callsign"], parsed["Output (MHz)"], parsed["Tone (Hz)"]
                match = (df["Group Name"].str.casefold() == group.casefold()) & \
                    df["Output (MHz)"].map(lambda f: freq_match(freq, f))
                if match.sum() != 1:
                    errors.append(f"{group} {call} {freq}: expected one matching repeater, found {match.sum()}")
                    continue

                i = df.index[match][0]
                old_call = df.at[i, "Callsign"]
                fields = dict(common_fields)
                if call and call != old_call:
                    fields["Callsign"] = call
                if tone is not None and tone != df.at[i, "Tone (Hz)"]:
                    fields["Tone (Hz)"] = tone

                df = set_status(df, old_call, freq, status)
                for col in fields:
                    ensure_col(df, col, default="")
                df = update_fields(df, old_call, freq, fields)

    return df, errors


def batch_args(args: argparse.Namespace | SimpleNamespace) -> list[SimpleNamespace]:
    """
    Expand --repeaters / --repeaters_file into one args namespace per listed repeater,
    each inheriting the other flags with call, freq, tone, and offset direction filled in.
    """
    text = args.repeaters or ""
    if args.repeaters_file:
        text += "\n" + Path(args.repeaters_file).read_text()
    return [
        SimpleNamespace(**{**vars(args), "call": r["Callsign"], "freq": r["Output (MHz)"], "tone": r["Tone (Hz)"],
                           "offset": r["Offset Sign"],
                           # Earlier steps set regen to reload the df; that would skip adding this repeater.
                           "regen": False, "score": False})
        for r in parse_repeater_lines(text)
    ]


def parse_repeaterbook_link(url: str) -> tuple[str | None, str | None]:
    """Extract (state_id, id) from a RepeaterBook details URL, or (None, None) if absent."""
    state_match = re.search(r"state_id=(\d+)", url or "")
    id_match = re.search(r"[?&]ID=(\d+)", url or "", re.IGNORECASE)
    return (state_match.group(1) if state_match else None, id_match.group(1) if id_match else None)


def format_offset(offset: str) -> str:
    """Format an offset in MHz the way the rest of the data does: "+0.6" or "-0.6"."""
    val = f"{float(offset):.4f}".rstrip("0")
    val += "0" if val.endswith(".") else ""
    return val if val.startswith("-") else f"+{val}"


def strip_unit(s: str, unit: str) -> str:
    """Drop a trailing unit suffix (any case, optional space), e.g. "103.5 Hz" -> "103.5"."""
    return re.sub(rf"\s*{unit}$", "", s.strip(), flags=re.IGNORECASE)


def parse_csv_offset(offset: str, freq: str | None) -> str | None:
    """
    Parse a submitted offset: "+"/"-" mean the band's standard offset in that direction;
    otherwise a number in MHz, or in kHz with a "kHz" suffix.
    """
    offset = offset.strip()
    if not offset:
        return None
    if offset in ("+", "-"):
        std = default_offset(freq)
        if std is None:
            raise ValueError(f"no standard offset for {freq} MHz; give the offset explicitly")
        return format_offset(f"{offset}{std}")
    if offset.lower().endswith("khz"):
        return format_offset(str(float(strip_unit(offset, "khz")) / 1000))
    return format_offset(strip_unit(offset, "mhz"))


def repeater_from_csv_row(row: dict, cols: dict) -> dict:
    """Build a repeater field dict from one row of the single-repeater submission CSV."""
    freq = strip_unit(row.get(cols["freq"]) or "", "mhz")
    coords = (row.get(cols["coords"]) or "").strip()
    info = (row.get(cols["info"]) or "").strip()

    lat_lon = None
    if coords:
        lat, lon = [p.strip() for p in coords.split(",", 1)]
        lat_lon = [float(lat), float(lon)]

    state_id, rb_id = parse_repeaterbook_link((row.get(cols["rb_link"]) or "").strip())

    repeater = {
        "Group Name": (row.get(cols["group"]) or "").strip(),
        "Callsign": (row.get(cols["call"]) or "").strip().upper(),
        "Output (MHz)": f"{float(freq):.4f}" if freq else None,
        "Offset (MHz)": parse_csv_offset(row.get(cols["offset"]) or "", freq),
        "Tone (Hz)": strip_unit(row.get(cols["tone"]) or "", "hz"),
        "Website": (row.get(cols["website"]) or "").strip(),
        "Location": (row.get(cols["location"]) or "").strip(),
        "Coordinates": lat_lon,
        "RepeaterBook State ID": state_id,
        "RepeaterBook ID": rb_id,
    }
    # Overwrite, rather than strip_empty, so a club clearing their Allstar/Echolink info
    # (or answering "No") actually clears the stored value instead of being dropped by
    # strip_empty below and leaving the old value in place.
    repeater = strip_empty(repeater)
    repeater["Allow Internet Contacts"] = (row.get(cols["allow"]) or "").strip()
    repeater["Internet Access"] = info if looks_like_internet_id(info) else ""
    return repeater


def apply_repeater_csv(
    df: pd.DataFrame, csv_file: str, status: str | None = None
) -> tuple[pd.DataFrame, list[str]]:
    """
    Add or edit repeaters from a single-repeater submission CSV (one row per repeater,
    with full details: callsign, frequency, offset, tone, location, etc).

    A row matching an existing repeater's callsign and frequency updates it in place;
    otherwise a new repeater is added. If status is given, every row (matched or new)
    is set to that status; otherwise a matched row's status is left as-is and a new
    row's status is set to response-needed.

    Returns the updated DataFrame and a list of error messages (one per row that could
    not be parsed; such rows are left unapplied).
    """
    df = df.reset_index(drop=True)
    errors = []
    new_rows = []
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        cols = {
            "group": find_col(reader.fieldnames, "club"),
            "call": find_col(reader.fieldnames, "repeater callsign"),
            "freq": find_col(reader.fieldnames, "output frequency"),
            "offset": find_col(reader.fieldnames, "offset"),
            "tone": find_col(reader.fieldnames, "tone"),
            "website": find_col(reader.fieldnames, "website"),
            "rb_link": find_col(reader.fieldnames, "repeaterbook"),
            "allow": find_col(reader.fieldnames, "allow contacts"),
            "info": find_col(reader.fieldnames, "echolink", "info"),
            "location": find_col(reader.fieldnames, "location"),
            "coords": find_col(reader.fieldnames, "coordinates"),
        }

        for row in reader:
            try:
                repeater = repeater_from_csv_row(row, cols)
                call, freq = repeater.get("Callsign"), repeater.get("Output (MHz)")
                if not call or not freq:
                    raise ValueError("missing callsign or output frequency")

                match = (df["Callsign"].str.upper() == call) & df["Output (MHz)"].map(lambda f: freq_match(freq, f))
                if match.sum() > 1:
                    raise ValueError(f"multiple existing repeaters match {call} {freq}")
                elif match.sum() == 1:
                    i = df.index[match][0]
                    fields = {k: v for k, v in repeater.items() if k not in ("Callsign", "Output (MHz)", "Group Name")}
                    if fields:
                        df = update_fields(df, call, freq, fields)
                    if status:
                        df = set_status(df, call, freq, status)
                else:
                    repeater["Mode"] = repeater.get("Mode") or "FM"
                    repeater["Status"] = status or STATUS_RESPONSE_NEEDED
                    new_rows.append(strip_empty(repeater))
            except Exception as e:
                errors.append(f"{row}: {e}")

    if new_rows:
        df = pd.concat([df, pd.DataFrame.from_records(new_rows)], ignore_index=True)
    return df.reset_index(drop=True), errors


def remove_df_footnotes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return dataframe with Mode column footnotes removed.
    """
    return df.assign(Mode=df["Mode"].str.replace(r"\[.+\]", "", regex=True))


if __name__ == "__main__":
    args = parse_args()
    if args.check:
        problems = check_consistency(pd.read_json(REPEATERS_JSON, dtype=False))
        print("\n".join(problems) or "No inconsistencies found.")
        sys.exit(1 if problems else 0)
    if args.rollover:
        rollover()
        args.regen = True
    if args.status and not args.repeater_csv:
        repeaters = pd.read_json(REPEATERS_JSON, dtype=False)
        # Only attempt the update if the callsign is already known; otherwise this is a
        # brand-new repeater and generate_repeater_df below will add it with this status.
        # Checking existence directly (rather than swallowing ValueError whenever
        # --wwara_csv/--id happen to be set) keeps a genuine typo'd callsign from being
        # silently dropped when those flags are also present.
        if args.call and (repeaters["Callsign"].str.upper() == args.call.upper()).any():
            try:
                repeaters = update_status_and_fields_for_callsign(
                    repeaters, args.call, args.freq, args.status, repeater_from_args(args)
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
    if args.status_csv:
        repeaters = pd.read_json(REPEATERS_JSON, dtype=False)
        repeaters, errors = apply_status_csv(repeaters, args.status_csv)
        repeaters.to_json(REPEATERS_JSON, orient="records", indent=4)
        if errors:
            print(f"{len(errors)} repeater(s) failed to update:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
        args.regen = True
    if args.repeater_csv:
        repeaters = pd.read_json(REPEATERS_JSON, dtype=False)
        repeaters, errors = apply_repeater_csv(repeaters, args.repeater_csv, status=args.status)
        repeaters.to_json(REPEATERS_JSON, orient="records", indent=4)
        if errors:
            print(f"{len(errors)} row(s) failed to apply:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
        args.regen = True

    batch = batch_args(args)
    if (args.repeaters or args.repeaters_file) and not batch:
        sys.exit("--repeaters/--repeaters_file contained no parseable repeater lines")
    if batch:
        # Each call persists to REPEATERS_JSON, so the last df includes every repeater.
        for a in batch:
            df = generate_repeater_df(a)
    else:
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
