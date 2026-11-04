import re
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pandas as pd

from markdown_files import (
    STATUS_IN,
    STATUS_OUT,
    STATUS_RESPONSE_NEEDED,
    write_group_pages,
    write_map_md,
    write_repeaters_md,
)

FORMS = {
    "group": {
        "url": "https://forms.example/group/viewform",
        "fields": {"Group Name": "entry.1", "Repeaters": "entry.2"},
    },
    "repeater": {
        "url": "https://forms.example/repeater/viewform",
        "fields": {
            "Group Name": "entry.10",
            "Callsign": "entry.11",
            "Output (MHz)": "entry.12",
            "Offset (MHz)": "entry.13",
            "Tone (Hz)": "entry.14",
            "Website": "entry.15",
            "RepeaterBook": "entry.16",
            "Location": "entry.17",
            "Coordinates": "entry.18",
            "Allow Internet Contacts": "entry.19",
            "Internet Access": "entry.20",
            "Mode": "entry.21",
        },
    },
}


def repeater(call, freq, status, **extra):
    """Build one PSRG repeater record with the given callsign, output frequency, and status."""
    return {
        "Callsign": call,
        "Output (MHz)": freq,
        "Offset (MHz)": "-0.6",
        "Tone (Hz)": "103.5",
        "Coordinates": [47.6395, -122.3693],
        "RepeaterBook ID": None,
        "RepeaterBook State ID": None,
        "Group Name": "PSRG",
        "Location": "Seattle",
        "Mode": "FM",
        "Long Name": "Puget Sound Repeater Group",
        "Website": "http://psrg.org",
        "Slug": "psrg",
        "Status": status,
        **extra,
    }


def site(tmp_path, monkeypatch):
    """Create the template directory under tmp_path and chdir there."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets" / "templates").mkdir(parents=True)
    template = (Path(__file__).parent.parent / "assets" / "templates" / "group.md").read_text()
    (tmp_path / "assets" / "templates" / "group.md").write_text(template)
    empty = (Path(__file__).parent.parent / "assets" / "templates" / "group_empty.md").read_text()
    (tmp_path / "assets" / "templates" / "group_empty.md").write_text(empty)


def links(page):
    """Return the query parameters of every markdown link target in page, keyed by URL path."""
    found = {}
    for url in re.findall(r"\]\((https://forms\.example/[^)]*)\)", page):
        parts = urlsplit(url)
        found.setdefault(parts.path, []).append({k: v[0] for k, v in parse_qs(parts.query).items()})
    return found


def test_write_group_pages_one_page_per_group(tmp_path, monkeypatch):
    """Each group gets a page named for its URL-safe group name, and stale group pages are removed."""
    site(tmp_path, monkeypatch)
    (tmp_path / "groups").mkdir()
    (tmp_path / "groups" / "gone.md").write_text("stale")
    df = pd.DataFrame([repeater("WW7PSR", "146.960", STATUS_IN), repeater("K7X", "147.000", STATUS_IN, **{"Group Name": "Shoreline ACS", "Slug": "shoreline-acs"})])
    df["RR#"] = df.index + 1

    write_group_pages(df, FORMS)

    got = sorted(p.name for p in (tmp_path / "groups").iterdir())
    assert got == ["psrg.md", "shoreline-acs.md"]


def test_write_group_pages_empty_page_for_club_without_repeaters(tmp_path, monkeypatch):
    """A club in clubs.csv with no repeaters gets a page saying so, with a link to tell us about one."""
    site(tmp_path, monkeypatch)
    df = pd.DataFrame([repeater("WW7PSR", "146.960", STATUS_IN)])
    df["RR#"] = 1
    clubs = pd.DataFrame(
        {
            "Group Name": ["PSRG", "YCRA"],
            "Long Name": ["Puget Sound Repeater Group", "Yakima County Radio Amateurs"],
            "Website": ["http://psrg.org", None],
            "Slug": ["psrg", "ycra"],
        }
    )

    write_group_pages(df, FORMS, clubs)

    page = (tmp_path / "groups" / "ycra.md").read_text()
    assert "Yakima County Radio Amateurs" in page
    assert "don't have any repeaters" in page
    assert links(page)["/repeater/viewform"][0]["entry.10"] == "YCRA"
    assert "don't have any repeaters" not in (tmp_path / "groups" / "psrg.md").read_text()


def test_write_group_pages_content(tmp_path, monkeypatch):
    """A group page shows the club details once, every repeater with its status, and RR# only for confirmed repeaters."""
    site(tmp_path, monkeypatch)
    df = pd.DataFrame(
        [
            repeater("WW7PSR", "146.960", STATUS_IN),
            repeater("WW7PSR", "52.870", STATUS_RESPONSE_NEEDED, **{"Offset (MHz)": "-1.7"}),
            repeater("WW7PSR", "443.000", STATUS_OUT, **{"Offset (MHz)": "+5.0", "Tone (Hz)": "D036"}),
        ]
    )
    df["RR#"] = df.index + 1

    write_group_pages(df, FORMS)
    page = (tmp_path / "groups" / "psrg.md").read_text()

    assert page.count("Puget Sound Repeater Group") == 1
    rows = [line for line in page.splitlines() if "WW7PSR" in line and line.startswith("|")]
    assert len(rows) == 3
    assert rows[0].split("|")[1].strip() == "1"
    assert rows[1].split("|")[1].strip() == ""
    assert "Response needed" in rows[1]
    assert "Out" in rows[2]


def test_write_group_pages_prefills_forms(tmp_path, monkeypatch):
    """The group form is prefilled with the group's repeaters and each correction link with that repeater's details."""
    site(tmp_path, monkeypatch)
    df = pd.DataFrame(
        [
            repeater("WW7PSR", "52.870", STATUS_RESPONSE_NEEDED, **{"Offset (MHz)": "-1.7"}),
            repeater(
                "WW7PSR",
                "146.960",
                STATUS_IN,
                **{
                    "RepeaterBook ID": "62",
                    "RepeaterBook State ID": "53",
                    "Allow Internet Contacts": "Yes",
                    "Internet Access": "Allstar node 1234",
                },
            ),
        ]
    )
    df["RR#"] = df.index + 1

    write_group_pages(df, FORMS)
    found = links((tmp_path / "groups" / "psrg.md").read_text())

    group = found["/group/viewform"][0]
    assert group["entry.1"] == "PSRG"
    assert group["entry.2"] == "- WW7PSR 52.870- T103.5\n- WW7PSR 146.960- T103.5"
    corrections = [q for q in found["/repeater/viewform"] if "entry.11" in q]
    assert len(corrections) == 2
    got = corrections[1]
    want = {
        "usp": "pp_url",
        "entry.10": "PSRG",
        "entry.11": "WW7PSR",
        "entry.12": "146.960",
        "entry.13": "-0.6",
        "entry.14": "103.5",
        "entry.15": "http://psrg.org",
        "entry.16": "https://www.repeaterbook.com/repeaters/details.php?state_id=53&ID=62",
        "entry.17": "Seattle",
        "entry.18": "47.6395, -122.3693",
        "entry.19": "Yes",
        "entry.20": "Allstar node 1234",
        "entry.21": "FM",
    }
    assert got == want
    add = [q for q in found["/repeater/viewform"] if "entry.11" not in q]
    assert add == [{"usp": "pp_url", "entry.10": "PSRG", "entry.15": "http://psrg.org"}]


def test_write_group_pages_strips_dcs_footnote_from_prefilled_tone(tmp_path, monkeypatch):
    """The DCS footnote marker on a tone is for display only and must not leak into prefilled form fields."""
    site(tmp_path, monkeypatch)
    df = pd.DataFrame([repeater("WW7PSR", "443.000", STATUS_IN, **{"Tone (Hz)": "D036[^dcs]"})])
    df["RR#"] = df.index + 1

    write_group_pages(df, FORMS)
    found = links((tmp_path / "groups" / "psrg.md").read_text())

    assert found["/group/viewform"][0]["entry.2"] == "- WW7PSR 443.000- D036"
    correction = next(q for q in found["/repeater/viewform"] if "entry.11" in q)
    assert correction["entry.14"] == "D036"


def test_write_group_pages_uses_stored_slug_not_group_name(tmp_path, monkeypatch):
    """Renaming a group must not move its published page: the page name comes from the club's Slug."""
    site(tmp_path, monkeypatch)
    df = pd.DataFrame([repeater("W7A", "146.960", STATUS_IN, **{"Group Name": "Renamed PSRG"})])
    df["RR#"] = df.index + 1

    write_group_pages(df, FORMS)

    assert [p.name for p in (tmp_path / "groups").iterdir()] == ["psrg.md"]


def test_write_group_pages_flags_missing_coordinates(tmp_path, monkeypatch):
    """A repeater without coordinates is listed on the group page so the trustee can supply them."""
    site(tmp_path, monkeypatch)
    df = pd.DataFrame([repeater("W7A", "146.960", STATUS_IN), repeater("W7B", "147.000", STATUS_IN, Coordinates=None)])
    df["RR#"] = df.index + 1

    write_group_pages(df, FORMS)
    page = (tmp_path / "groups" / "psrg.md").read_text()

    assert "location (coordinates)" in page and "W7B 147.000" in page
    assert "W7A 146.960" not in page


def test_write_group_pages_escapes_html(tmp_path, monkeypatch):
    """Repeater fields containing HTML or table delimiters are escaped rather than rendered."""
    site(tmp_path, monkeypatch)
    df = pd.DataFrame([repeater("W7A", "146.960", STATUS_IN, Location="<script>x</script> | y")])
    df["RR#"] = df.index + 1

    write_group_pages(df, FORMS)
    page = (tmp_path / "groups" / "psrg.md").read_text()

    assert "<script>" not in page
    assert "&lt;script&gt;x&lt;/script&gt; \\| y" in page


def test_write_map_md_with_no_repeaters(tmp_path, monkeypatch):
    """write_map_md rewrites the map with no pins when no repeaters are published, instead of leaving a stale map."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets" / "templates").mkdir(parents=True)
    (tmp_path / "assets" / "templates" / "map.md").write_text("pins: {{ repeater_pins }}")
    (tmp_path / "assets" / "templates" / "map.html").write_text("{{ repeater_pins }}")
    (tmp_path / "map.md").write_text("stale")

    write_map_md(pd.DataFrame(columns=["Callsign", "Output (MHz)", "Coordinates", "RR#"]))

    assert (tmp_path / "map.md").read_text() == "pins: "


def test_write_map_md_skips_repeater_with_missing_coordinates(tmp_path, monkeypatch):
    """A confirmed repeater with no Coordinates (e.g. imported without lat/long) shouldn't crash the map build."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets" / "templates").mkdir(parents=True)
    (tmp_path / "assets" / "templates" / "map.md").write_text("pins: {{ repeater_pins }}")
    (tmp_path / "assets" / "templates" / "map.html").write_text("{{ repeater_pins }}")

    df = pd.DataFrame([
        {"Callsign": "WW7PSR", "Output (MHz)": "146.960", "Coordinates": [47.6395, -122.3693], "RR#": 1},
        {"Callsign": "WA7SAR", "Output (MHz)": "145.2700", "Coordinates": None, "RR#": 2},
    ])

    write_map_md(df)

    pins = (tmp_path / "map.md").read_text()
    assert "RR# 1" in pins
    assert "RR# 2" not in pins


def test_write_repeaters_md_with_no_repeaters(tmp_path, monkeypatch):
    """write_repeaters_md shows a holding message instead of crashing when nothing is confirmed yet."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets" / "templates").mkdir(parents=True)
    (tmp_path / "assets" / "templates" / "repeaters.md").write_text("{{ table }}\n{{ associations }}")

    write_repeaters_md(
        pd.DataFrame(
            columns=[
                "RR#",
                "Group Name",
                "Callsign",
                "Location",
                "Mode",
                "Output (MHz)",
                "Offset (MHz)",
                "Tone (Hz)",
                "Long Name",
                "Website",
            ]
        )
    )

    page = (tmp_path / "repeaters.md").read_text()
    assert "We're confirming repeaters for this year's Repeater Roundabout.  Check back soon!" in page


def test_write_group_pages_shows_internet_access(tmp_path, monkeypatch):
    """A group page shows whether each repeater allows internet contacts and how to reach it online."""
    site(tmp_path, monkeypatch)
    df = pd.DataFrame(
        [repeater("W7A", "146.960", STATUS_IN, **{"Allow Internet Contacts": "No", "Internet Access": "Echolink W7A-R"})]
    )
    df["RR#"] = df.index + 1

    write_group_pages(df, FORMS)
    row = next(line for line in (tmp_path / "groups" / "psrg.md").read_text().splitlines() if line.startswith("| 1 "))

    assert "| No " in row
    assert "Echolink W7A-R" in row


def test_write_repeaters_md_omits_link_for_club_without_website(tmp_path, monkeypatch):
    """A club with no website is listed by name, not as a link to 'nan'."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets" / "templates").mkdir(parents=True)
    (tmp_path / "assets" / "templates" / "repeaters.md").write_text("{{ table }}\n{{ associations }}")
    df = pd.DataFrame([repeater("W7A", "146.960", STATUS_IN, Website=float("nan"))])
    df["RR#"] = df.index + 1

    write_repeaters_md(df)

    page = (tmp_path / "repeaters.md").read_text()
    assert "PSRG\n: Puget Sound Repeater Group\n" in page
    assert "nan" not in page


def test_write_repeaters_md_shows_internet_access(tmp_path, monkeypatch):
    """The repeaters page has an Internet access column: the details alone when internet contacts are allowed, plain Yes without details, or blank/No."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets" / "templates").mkdir(parents=True)
    (tmp_path / "assets" / "templates" / "repeaters.md").write_text("{{ table }}\n{{ associations }}")
    df = pd.DataFrame(
        [
            repeater("W7A", "146.960", STATUS_IN, **{"Allow Internet Contacts": "Yes", "Internet Access": "Echolink 1234"}),
            repeater("W7B", "147.000", STATUS_IN, **{"Allow Internet Contacts": "Yes", "Internet Access": None}),
            repeater("W7C", "147.020", STATUS_IN, **{"Allow Internet Contacts": "No", "Internet Access": "Echolink 99"}),
            repeater("W7D", "147.040", STATUS_IN),
        ]
    )
    df["RR#"] = df.index + 1

    write_repeaters_md(df)

    page = (tmp_path / "repeaters.md").read_text()
    rows = {r.split("|")[3].strip(): r for r in page.splitlines() if r.startswith("| ")}
    assert "Internet access" in page
    assert rows["W7A"].split("|")[-2].strip() == "Echolink 1234"
    assert rows["W7B"].split("|")[-2].strip() == "Yes"
    assert rows["W7C"].split("|")[-2].strip() == "No"
    assert rows["W7D"].split("|")[-2].strip() == ""
