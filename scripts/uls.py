"""
Look up hams' licensed locations in the FCC ULS amateur database.

Each callsign's mailing ZIP code comes from the ULS weekly bulk file, and is placed at the
Census Bureau's centroid for that ZIP code (ZCTA). Locations are cached in data/ham_locations.json,
including misses, so the ~200MB ULS file is only scanned for new callsigns. Delete data/ to refresh.
"""

import io
import json
import re
import zipfile
from collections.abc import Iterable
from pathlib import Path

import requests

ULS_URL = "https://data.fcc.gov/download/pub/uls/complete/l_amat.zip"
ZCTA_URL = "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2024_Gazetteer/2024_Gaz_zcta_national.zip"
DATA_DIR = Path("data")

US_CALLSIGN = re.compile(r"[AKNW][A-Z]?\d[A-Z]{1,3}")

# EN.dat (entity) record fields, per the FCC ULS public access file definitions
EN_USI, EN_CALL, EN_ZIP = 1, 4, 18


def base_callsign(call: str) -> str | None:
    """Return the US callsign without any portable suffix (KI6KTE/M -> KI6KTE), or None if it isn't one."""
    base = str(call).strip().upper().split("/")[0]
    return base if US_CALLSIGN.fullmatch(base) else None


def download(url: str, dest: Path) -> Path:
    """Download url to dest unless it's already there."""
    if not dest.exists():
        print(f"Downloading {url}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        part = dest.with_suffix(".part")
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(part, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
        part.rename(dest)
    return dest


def uls_zip_codes(calls: set[str], uls_zip: Path) -> dict[str, str]:
    """Map each callsign found in the ULS bulk file to the 5-digit ZIP code of its newest license."""
    newest = {}
    with zipfile.ZipFile(uls_zip) as z, z.open("EN.dat") as f:
        for line in io.TextIOWrapper(f, encoding="latin-1"):
            fields = line.split("|")
            if len(fields) <= EN_ZIP or fields[EN_CALL] not in calls:
                continue
            usi = int(fields[EN_USI])
            # A reassigned (e.g. vanity) callsign keeps its old licenses; the newest one is current.
            if usi > newest.get(fields[EN_CALL], (-1, ""))[0]:
                newest[fields[EN_CALL]] = (usi, fields[EN_ZIP][:5])
    return {call: zip_code for call, (_, zip_code) in newest.items()}


def zcta_centroids(zcta_zip: Path) -> dict[str, list[float]]:
    """Map each ZIP code tabulation area to its [lat, lon] internal point."""
    with zipfile.ZipFile(zcta_zip) as z, z.open(z.namelist()[0]) as f:
        rows = io.TextIOWrapper(f, encoding="utf-8").read().splitlines()[1:]
    return {r[0]: [float(r[5]), float(r[6])] for r in (row.split("\t") for row in rows)}


def ham_locations(calls: Iterable[str]) -> dict[str, list[float]]:
    """Map the base callsign (see base_callsign) of each of calls with a known US license location to [lat, lon]."""
    cache_file = DATA_DIR / "ham_locations.json"
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    calls = {base_callsign(call) for call in calls} - {None}

    missing = calls - cache.keys()
    if missing:
        zip_codes = uls_zip_codes(missing, download(ULS_URL, DATA_DIR / "l_amat.zip"))
        centroids = zcta_centroids(download(ZCTA_URL, DATA_DIR / "zcta.zip"))
        for base in missing:
            cache[base] = centroids.get(zip_codes.get(base))
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(cache, indent=1, sort_keys=True))

    return {call: cache[call] for call in calls if cache[call]}
