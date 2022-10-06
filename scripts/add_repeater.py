import argparse
from typing import Tuple

import pandas as pd
import requests

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="Name of the repeater system", type=str, required=True)
    parser.add_argument("--id", help="ID code from repeaterbook.com", type=str, required=True)
    parser.add_argument("--loc", help="A general location", type=str, required=True)
    parser.add_argument("--mode", help="Mode", type=str, default="FM")
    parser.add_argument("--call", help="Callsign", type=str, default=None)
    parser.add_argument("--freq", help="Output frequency", type=str, default=None)
    parser.add_argument("--offset", help="Offset", type=str, default=None)
    parser.add_argument("--tone", help="Tone", type=str, default=None)
    return parser.parse_args()


def parse_repeaterbook(id_code: str) -> Tuple:
    """
    Extract a bunch of repeater information from RepeaterBook.

    Parameters
    ----------
    id_code : str
        The ID code from RepeaterBook.

    Returns
    -------
    Tuple
        A tuple of the form (callsign, frequency, offset, latlong, tone).
    """
    
    url = f"https://www.repeaterbook.com/repeaters/details.php?state_id=53&ID={id_code}"
    source = requests.get(url)

    call = source.text.split("msResult.php?call=")[1].split("&")[0]
    
    freq = source.text.split("Downlink:</td>\n<td>")[1].split("</td>")[0]
    freq = f"{float(freq):.04f}"
    if freq[-1] == "0":
        freq = freq[:-1]

    offset = source.text.split("Offset:</td>\n<td>\n")[1].split(" MHz")[0]
    offset = f"{float(offset):.01f}"
    if offset[0] != "-":
        offset = f"+{offset}"

    latlong = source.text.split("center: ")[1].split("\n")[0][:-1]

    tone = source.text.split("Uplink Tone:</td>\n<td>")[1].split("</td")[0]
    
    try:
        latlong = eval(latlong)
    except SyntaxError:
        pass

    return call, freq, latlong, offset, tone


if __name__ == "__main__":

    args = parse_args()
    parse_repeaterbook(args.id)

    call, freq, latlong, offset, tone = parse_repeaterbook(args.id)

    results = {
        "Group Name": args.name,
        "Callsign": args.call if args.call else call,
        "Location": args.loc,
        "Mode": args.mode,
        "Output (MHz)": args.freq if args.freq else freq, 
        "Offset (MHz)": args.offset if args.offset else offset,
        "Tone (Hz)": args.tone if args.tone else tone,
        "Coordinates": latlong,
    }

    df = pd.read_json("assets/repeaters.json")
    df = df.append(results, ignore_index=True)
    df.to_json("assets/repeaters.json", orient="records", indent=4)

    table = df.drop(
        columns=["Coordinates"]
    ).to_markdown(
        index=False, 
        disable_numparse=True, 
        colalign=["left", "left", "left", "left", "right", "right", "right"]
    )
    with open("assets/repeaters_template.md", "r") as f:
        maps = f.read().replace("{{ table }}", table)
    with open("repeaters.md", "w") as f:
        f.write(maps)