import json
from datetime import datetime

import pandas as pd
import pytest

from markdown_files import STATUS_IN, STATUS_OUT, STATUS_RESPONSE_NEEDED
from update import merge_repeaters, refresh_repeater, rollover, set_status, update_all_repeaters


def make_site(root):
    """Create a minimal post-contest site layout under root."""
    (root / "assets").mkdir()
    (root / "assets" / "repeaters.json").write_text("[]")
    (root / "results").mkdir()
    (root / "results" / "W7ABC.csv").write_text("log")
    (root / "results" / "W7ABC.md").write_text("page")


def test_rollover_archives_last_contest(tmp_path, monkeypatch):
    """rollover copies repeaters.json and moves result CSVs into an archive named for the previous year."""
    monkeypatch.chdir(tmp_path)
    make_site(tmp_path)

    rollover(datetime(2026, 10, 18))

    assert (tmp_path / "2025" / "repeaters.json").read_text() == "[]"
    assert json.loads((tmp_path / "assets" / "repeaters.json").read_text()) == []
    assert (tmp_path / "2025" / "results" / "W7ABC.csv").read_text() == "log"
    assert not (tmp_path / "results" / "W7ABC.csv").exists()


def test_rollover_refuses_existing_archive(tmp_path, monkeypatch):
    """rollover exits non-zero and changes nothing when the archive directory already exists."""
    monkeypatch.chdir(tmp_path)
    make_site(tmp_path)
    (tmp_path / "2025").mkdir()

    with pytest.raises(SystemExit) as exc:
        rollover(datetime(2026, 10, 18))

    assert exc.value.code != 0
    assert list((tmp_path / "2025").iterdir()) == []
    assert sorted(p.name for p in (tmp_path / "results").iterdir()) == ["W7ABC.csv", "W7ABC.md"]


def test_rollover_resets_statuses(tmp_path, monkeypatch):
    """rollover marks every repeater as needing a response for the new year, while the archive keeps last year's statuses."""
    monkeypatch.chdir(tmp_path)
    make_site(tmp_path)
    repeaters = [{"Callsign": "W7A", "Status": STATUS_IN}, {"Callsign": "W7B", "Status": STATUS_OUT}]
    (tmp_path / "assets" / "repeaters.json").write_text(json.dumps(repeaters))

    rollover(datetime(2026, 10, 18))

    got = [r["Status"] for r in json.loads((tmp_path / "assets" / "repeaters.json").read_text())]
    assert got == [STATUS_RESPONSE_NEEDED, STATUS_RESPONSE_NEEDED]
    archived = [r["Status"] for r in json.loads((tmp_path / "2025" / "repeaters.json").read_text())]
    assert archived == [STATUS_IN, STATUS_OUT]


def repeater_list(*statuses):
    """Build a repeater DataFrame with callsigns W7A, W7B, ... on 146.000 MHz and the given statuses."""
    return pd.DataFrame(
        [{"Callsign": f"W7{chr(65 + i)}", "Output (MHz)": "146.000", "Status": s} for i, s in enumerate(statuses)]
    )


def calls(df):
    """Return the callsigns of df in order."""
    return df["Callsign"].tolist()


def test_set_status_response_needed_to_in_follows_last_in():
    """Confirming a repeater moves it directly after the last confirmed repeater, so published numbers don't change."""
    df = repeater_list(STATUS_IN, STATUS_RESPONSE_NEEDED, STATUS_OUT, STATUS_IN, STATUS_RESPONSE_NEEDED)

    got = set_status(df, "W7E", "146.0", STATUS_IN)

    assert calls(got) == ["W7A", "W7B", "W7C", "W7D", "W7E"]
    got = set_status(repeater_list(STATUS_IN, STATUS_RESPONSE_NEEDED, STATUS_RESPONSE_NEEDED), "w7c", "146.000", STATUS_IN)
    assert calls(got) == ["W7A", "W7C", "W7B"]
    assert got["Status"].tolist() == [STATUS_IN, STATUS_IN, STATUS_RESPONSE_NEEDED]


def test_set_status_first_in_goes_to_top():
    """Confirming the first repeater of the year makes it RR# 1."""
    got = set_status(repeater_list(STATUS_RESPONSE_NEEDED, STATUS_RESPONSE_NEEDED), "W7B", "146.000", STATUS_IN)

    assert calls(got) == ["W7B", "W7A"]


def test_set_status_response_needed_to_out_moves_to_end():
    """Declining a repeater moves it to the end of the list."""
    got = set_status(repeater_list(STATUS_RESPONSE_NEEDED, STATUS_IN, STATUS_RESPONSE_NEEDED), "W7A", "146.000", STATUS_OUT)

    assert calls(got) == ["W7B", "W7C", "W7A"]
    assert got["Status"].tolist() == [STATUS_IN, STATUS_RESPONSE_NEEDED, STATUS_OUT]


def test_set_status_from_decided_status_stays_put():
    """Changing a repeater that is already in or out keeps its position, so no published number shifts."""
    got = set_status(repeater_list(STATUS_IN, STATUS_IN, STATUS_IN), "W7A", "146.000", STATUS_OUT)

    assert calls(got) == ["W7A", "W7B", "W7C"]
    assert got["Status"].tolist() == [STATUS_OUT, STATUS_IN, STATUS_IN]


def test_set_status_missing_status_counts_as_response_needed():
    """A repeater with no recorded status is treated as needing a response."""
    df = repeater_list(STATUS_IN, STATUS_IN, STATUS_IN)
    df.loc[2, "Status"] = None

    got = set_status(df, "W7C", "146.000", STATUS_OUT)

    assert got["Status"].tolist() == [STATUS_IN, STATUS_IN, STATUS_OUT]


def test_set_status_requires_exactly_one_match():
    """set_status rejects a callsign/frequency that matches no repeater or more than one."""
    df = repeater_list(STATUS_IN, STATUS_IN)
    df.loc[1, "Callsign"] = "W7A"

    with pytest.raises(ValueError):
        set_status(df, "W7A", "146.000", STATUS_OUT)
    with pytest.raises(ValueError):
        set_status(df, "W7Z", "146.000", STATUS_OUT)


def test_merge_repeaters_starts_as_response_needed():
    """A repeater imported from last year's file needs a fresh response, whatever its status was then."""
    got = merge_repeaters(prior={"Callsign": "W7A", "Status": STATUS_IN, "Exclude": True})

    assert got["Status"] == STATUS_RESPONSE_NEEDED
    assert "Exclude" not in got


def test_refresh_repeater_keeps_status_and_exclude():
    """Unlike merge_repeaters, refreshing an already-known repeater must not touch its contest status."""
    prior = {"Callsign": "W7A", "Status": STATUS_IN, "Exclude": True, "Output (MHz)": "146.000"}
    got = refresh_repeater(repeaterbook={"Tone (Hz)": "100.0"}, prior=prior)

    assert got["Status"] == STATUS_IN
    assert got["Exclude"] is True
    assert got["Tone (Hz)"] == "100.0"


def test_refresh_repeater_clears_stale_tone_when_repeaterbook_confirms_toneless():
    """An explicit empty tone from RepeaterBook means toneless, not missing, and should overwrite a stale tone."""
    got = refresh_repeater(
        repeaterbook={"Tone (Hz)": "", "Output (MHz)": "146.0000"},
        prior={"Tone (Hz)": "88.5", "Output (MHz)": "146.0000"},
    )

    assert got["Tone (Hz)"] == ""


def test_refresh_repeater_prefers_wwara_then_repeaterbook_then_prior():
    """Source data refreshes stale fields; RepeaterBook/WWARA data is treated as more current than prior."""
    got = refresh_repeater(
        repeaterbook={"Tone (Hz)": "100.0", "Output (MHz)": "146.0000"},
        wwara={"Tone (Hz)": "103.5"},
        prior={"Tone (Hz)": "88.5", "Output (MHz)": "146.0000", "Group Name": "Old Name"},
    )

    assert got["Tone (Hz)"] == "103.5"
    assert got["Group Name"] == "Old Name"  # prior wins for name-ish fields


def test_update_all_repeaters_refreshes_from_repeaterbook(monkeypatch):
    """Each repeater with a recorded RepeaterBook ID is refreshed from RepeaterBook, status untouched."""
    import update

    def fake_lookup(state_id, rb_id):
        return {"Tone (Hz)": "103.5", "Callsign": "W7A", "Output (MHz)": "146.0000"}

    monkeypatch.setattr(update, "repeater_from_repeaterbook", fake_lookup)

    df = pd.DataFrame.from_records([{
        "Callsign": "W7A",
        "Output (MHz)": "146.0000",
        "Tone (Hz)": "88.5",
        "Status": STATUS_IN,
        "RepeaterBook State ID": "53",
        "RepeaterBook ID": "1234",
    }])

    got, errors = update_all_repeaters(df, wwara_csv=None)

    assert errors == []
    assert got.loc[0, "Tone (Hz)"] == "103.5"
    assert got.loc[0, "Status"] == STATUS_IN


def test_update_all_repeaters_skips_repeaters_without_source_ids():
    """A manually-entered repeater with no RepeaterBook ID or WWARA csv is left untouched."""
    df = pd.DataFrame.from_records([{"Callsign": "W7A", "Output (MHz)": "146.0000", "Status": STATUS_IN}])

    got, errors = update_all_repeaters(df, wwara_csv=None)

    assert errors == []
    assert got.loc[0, "Status"] == STATUS_IN
    assert got.loc[0, "Output (MHz)"] == "146.0000"


def test_update_all_repeaters_aggregates_errors_and_continues(monkeypatch):
    """A failing repeater is reported as an error but doesn't stop the rest from updating."""
    import update

    def fake_lookup(state_id, rb_id):
        if rb_id == "bad":
            raise RuntimeError("boom")
        return {"Tone (Hz)": "103.5", "Callsign": "W7B", "Output (MHz)": "146.5000"}

    monkeypatch.setattr(update, "repeater_from_repeaterbook", fake_lookup)

    df = pd.DataFrame.from_records([
        {"Callsign": "W7A", "Output (MHz)": "146.0000", "Status": STATUS_IN,
         "RepeaterBook State ID": "53", "RepeaterBook ID": "bad"},
        {"Callsign": "W7B", "Output (MHz)": "146.5000", "Status": STATUS_IN,
         "RepeaterBook State ID": "53", "RepeaterBook ID": "5678"},
    ])

    got, errors = update_all_repeaters(df, wwara_csv=None)

    assert len(errors) == 1
    assert "W7A" in errors[0]
    assert got.loc[0, "Tone (Hz)"] != "103.5"  # left unchanged after the failure
    assert got.loc[1, "Tone (Hz)"] == "103.5"  # second repeater still updated
