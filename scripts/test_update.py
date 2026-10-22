import json
from datetime import datetime
from types import SimpleNamespace

import pandas as pd
import pytest

from markdown_files import STATUS_IN, STATUS_OUT, STATUS_RESPONSE_NEEDED
from update import (
    apply_repeater_csv,
    apply_status_csv,
    drop_missing_coordinates,
    generate_repeater_df,
    looks_like_internet_id,
    merge_repeaters,
    parse_repeater_lines,
    parse_repeaterbook_location,
    refresh_repeater,
    repeaters_from_wwara,
    rollover,
    set_status,
    update_all_repeaters,
    update_fields,
    update_status_and_fields,
    update_status_and_fields_for_callsign,
)


def make_args(**overrides):
    """Build a generate_repeater_df argument namespace with sensible defaults."""
    args = {
        "name": None, "loc": None, "state_id": None, "id": None,
        "wwara_csv": None, "prior_json": None, "call": None, "freq": None,
        "offset": None, "tone": None, "mode": None, "lat": None, "lon": None,
        "long_name": None, "url": None, "internet_contacts": None,
        "internet_access": None, "regen": False, "score": False,
    }
    args.update(overrides)
    return SimpleNamespace(**args)


def make_site(root):
    """Create a minimal post-contest site layout under root."""
    (root / "assets").mkdir()
    (root / "assets" / "repeaters.json").write_text("[]")
    (root / "results").mkdir()
    (root / "results" / "W7ABC.csv").write_text("log")
    (root / "results" / "W7ABC.md").write_text("page")


def test_repeaters_from_wwara_returns_empty_dataframe_without_csv():
    """No --wwara_csv means no WWARA data, but callers expect a DataFrame, not a list."""
    result = repeaters_from_wwara(None, "W7ABC")
    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_drop_missing_coordinates_removes_rows_without_lat_lon(capsys):
    """A repeater confirmed 'in' without a [lat, lon] pair is dropped and reported, not left to crash downstream."""
    df = pd.DataFrame([
        {"Callsign": "W7A", "Output (MHz)": "146.000", "Coordinates": [47.0, -122.0]},
        {"Callsign": "W7B", "Output (MHz)": "146.500", "Coordinates": None},
    ])

    got = drop_missing_coordinates(df)

    assert got["Callsign"].tolist() == ["W7A"]
    assert "W7B 146.500" in capsys.readouterr().err


def test_generate_repeater_df_updates_existing_repeater_in_place(tmp_path, monkeypatch):
    """A matching callsign+frequency updates the existing repeater instead of adding a duplicate."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "repeaters.json").write_text(json.dumps([
        {"Callsign": "W7ABC", "Output (MHz)": "146.9000", "Group Name": "Old Name",
         "Status": STATUS_IN, "RepeaterBook ID": None},
    ]))

    args = make_args(call="W7ABC", freq="146.900", name="New Name")
    df = generate_repeater_df(args)

    assert len(df) == 1
    assert df.iloc[0]["Group Name"] == "New Name"
    assert df.iloc[0]["Status"] == STATUS_IN


def test_generate_repeater_df_adds_new_repeater_when_no_match(tmp_path, monkeypatch):
    """A callsign+frequency with no existing match is appended as a new repeater."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "repeaters.json").write_text(json.dumps([
        {"Callsign": "W7ABC", "Output (MHz)": "146.9000", "Group Name": "Old Name",
         "Status": STATUS_IN, "RepeaterBook ID": None},
    ]))

    args = make_args(call="W7XYZ", freq="147.000", name="New Club")
    df = generate_repeater_df(args)

    assert len(df) == 2
    assert sorted(df["Callsign"]) == ["W7ABC", "W7XYZ"]


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


def test_update_fields_overwrites_matching_repeater():
    """update_fields changes only the given fields on the matching repeater."""
    df = repeater_list(STATUS_IN, STATUS_IN)
    df["Internet Access"] = ["No", "No"]

    got = update_fields(df, "W7A", "146.000", {"Internet Access": "Yes"})

    assert got["Internet Access"].tolist() == ["Yes", "No"]
    assert calls(got) == ["W7A", "W7B"]


def test_update_fields_requires_exactly_one_match():
    """update_fields rejects a callsign/frequency that matches no repeater or more than one."""
    df = repeater_list(STATUS_IN, STATUS_IN)
    df.loc[1, "Callsign"] = "W7A"

    with pytest.raises(ValueError):
        update_fields(df, "W7A", "146.000", {"Internet Access": "Yes"})
    with pytest.raises(ValueError):
        update_fields(df, "W7Z", "146.000", {"Internet Access": "Yes"})


def test_update_status_and_fields_sets_status_and_other_fields():
    """update_status_and_fields changes status and other fields on the matching repeater."""
    df = repeater_list(STATUS_RESPONSE_NEEDED)
    df["Internet Access"] = ["No"]

    got = update_status_and_fields(df, "W7A", "146.000", STATUS_IN, {"Internet Access": "Yes"})

    assert got["Status"].tolist() == [STATUS_IN]
    assert got["Internet Access"].tolist() == ["Yes"]


def test_update_status_and_fields_ignores_match_keys_in_fields():
    """Callsign/frequency used to find the repeater are never written back from the raw user input."""
    df = repeater_list(STATUS_RESPONSE_NEEDED)

    got = update_status_and_fields(
        df, "w7a", "146.0", STATUS_IN, {"Callsign": "w7a", "Output (MHz)": "146.0"}
    )

    assert got["Callsign"].tolist() == ["W7A"]
    assert got["Output (MHz)"].tolist() == ["146.000"]


def test_update_status_and_fields_for_callsign_updates_all_matches():
    """With no frequency given, every repeater with the callsign is updated."""
    df = pd.DataFrame([
        {"Callsign": "W7A", "Output (MHz)": "146.000", "Status": STATUS_RESPONSE_NEEDED},
        {"Callsign": "W7A", "Output (MHz)": "147.000", "Status": STATUS_RESPONSE_NEEDED},
        {"Callsign": "W7B", "Output (MHz)": "148.000", "Status": STATUS_RESPONSE_NEEDED},
    ])

    got = update_status_and_fields_for_callsign(df, "w7a", None, STATUS_IN, {})

    assert got["Status"].tolist() == [STATUS_IN, STATUS_IN, STATUS_RESPONSE_NEEDED]


def test_update_status_and_fields_for_callsign_with_freq_updates_one():
    """A given frequency still narrows the match to a single repeater, as before."""
    df = pd.DataFrame([
        {"Callsign": "W7A", "Output (MHz)": "146.000", "Status": STATUS_RESPONSE_NEEDED},
        {"Callsign": "W7A", "Output (MHz)": "147.000", "Status": STATUS_RESPONSE_NEEDED},
    ])

    got = update_status_and_fields_for_callsign(df, "W7A", "146.000", STATUS_IN, {})

    assert got["Status"].tolist() == [STATUS_IN, STATUS_RESPONSE_NEEDED]


def test_update_status_and_fields_for_callsign_requires_a_match():
    """An unknown callsign with no frequency raises instead of silently doing nothing."""
    df = pd.DataFrame([{"Callsign": "W7A", "Output (MHz)": "146.000", "Status": STATUS_RESPONSE_NEEDED}])

    with pytest.raises(ValueError):
        update_status_and_fields_for_callsign(df, "W7Z", None, STATUS_IN, {})


def test_merge_repeaters_starts_as_response_needed():
    """A repeater imported from last year's file needs a fresh response, whatever its status was then."""
    got = merge_repeaters(prior={"Callsign": "W7A", "Status": STATUS_IN, "Exclude": True})

    assert got["Status"] == STATUS_RESPONSE_NEEDED
    assert "Exclude" not in got


def test_merge_repeaters_defaults_mode_to_fm():
    """A repeater with no mode from any source defaults to FM."""
    got = merge_repeaters(args={"Callsign": "W7A"})

    assert got["Mode"] == "FM"


def test_merge_repeaters_keeps_wwara_mode():
    """args no longer forces FM over a mode supplied by another source."""
    got = merge_repeaters(args={"Callsign": "W7A"}, wwara={"Mode": "NBFM[^nbfm]"})

    assert got["Mode"] == "NBFM[^nbfm]"


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


def test_parse_repeater_lines_ctcss_and_dcs():
    """parse_repeater_lines extracts callsign, frequency, and tone (CTCSS or DCS) from each line."""
    text = "- WA7SAR 146.860- T123.0\n- WA7SAR 147.080+ T123.0\n- N7ABC 444.600+ D023N"

    got = parse_repeater_lines(text)

    assert got == [
        {"Callsign": "WA7SAR", "Output (MHz)": "146.860", "Tone (Hz)": "123.0"},
        {"Callsign": "WA7SAR", "Output (MHz)": "147.080", "Tone (Hz)": "123.0"},
        {"Callsign": "N7ABC", "Output (MHz)": "444.600", "Tone (Hz)": "D023N"},
    ]


def test_parse_repeater_lines_toneless_and_blank():
    """A toneless repeater parses with Tone (Hz) None; blank lines are skipped."""
    got = parse_repeater_lines("- W7XYZ 146.520\n\n")

    assert got == [{"Callsign": "W7XYZ", "Output (MHz)": "146.520", "Tone (Hz)": None}]


def test_parse_repeaterbook_location_extracts_city_and_state():
    """parse_repeaterbook_location pulls "City, State" out of the City • County • State line."""
    html = """
    <p class="mb-1 text-body-secondary fw-normal">
                      <i class="bi bi-broadcast-pin" aria-hidden="true"></i>
                                            <span class="ms-1">
                        147.06000                                                  (+)
                                                MHz
                      </span>
                                              <span class="ms-1">85.4</span>
                                          </p>

    <p class="mb-0 text-body-secondary">
                        Ellensburg                                                 • Kittitas County                         • Washington                      </p>
    """

    assert parse_repeaterbook_location(html) == "Ellensburg, Washington"


def test_parse_repeaterbook_location_missing_returns_none():
    """parse_repeaterbook_location returns None when the page has no location line."""
    assert parse_repeaterbook_location("<p>nothing here</p>") is None


def test_looks_like_internet_id():
    """Node numbers and EchoLink-style callsign-node ids pass; "No"/blank/junk don't."""
    assert looks_like_internet_id("47909")
    assert looks_like_internet_id("WA7SAR-L")
    assert not looks_like_internet_id("No")
    assert not looks_like_internet_id("")
    assert not looks_like_internet_id(None)
    assert not looks_like_internet_id("N/A")


def test_apply_status_csv_updates_status_callsign_and_tone(tmp_path):
    """A survey row flips status for every listed repeater and corrects a drifted callsign/tone."""
    df = pd.DataFrame.from_records([
        {"Callsign": "WA7OLD", "Output (MHz)": "146.860", "Tone (Hz)": "100.0",
         "Group Name": "YCRA", "Status": STATUS_RESPONSE_NEEDED},
    ])
    csv_file = tmp_path / "status.csv"
    csv_file.write_text(
        "Timestamp,Your Email,Club / Repeater Group,"
        "Can Repeater Roundabout participants make contacts on your repeaters?,"
        '"Repeaters (if only some are available, delete any we should avoid)",'
        "Allow contacts via Allstar/Echolink/YSF/D-Star (if applicable)?,"
        "Allstar/Echolink info (if applicable)\n"
        '10/19/2026,kb7hdx@gmail.com,YCRA,Yes,"- WA7SAR 146.860- T123.0",No,\n'
    )

    got, errors = apply_status_csv(df, str(csv_file))

    assert errors == []
    assert got.loc[0, "Status"] == STATUS_IN
    assert got.loc[0, "Callsign"] == "WA7SAR"
    assert got.loc[0, "Tone (Hz)"] == "123.0"
    assert got.loc[0, "Allow Internet Contacts"] == "No"
    assert got.loc[0, "Internet Access"] == ""


def test_apply_status_csv_reports_unmatched_repeater(tmp_path):
    """A listed repeater that doesn't match exactly one existing repeater in its group is an error."""
    df = pd.DataFrame.from_records([
        {"Callsign": "WA7SAR", "Output (MHz)": "146.860", "Tone (Hz)": "123.0",
         "Group Name": "YCRA", "Status": STATUS_RESPONSE_NEEDED},
    ])
    csv_file = tmp_path / "status.csv"
    csv_file.write_text(
        "Club / Repeater Group,Can Repeater Roundabout participants make contacts on your repeaters?,"
        "Repeaters,Allow contacts via Allstar/Echolink/YSF/D-Star (if applicable)?,Allstar/Echolink info\n"
        '"YCRA","Yes","- WA7SAR 999.999 T123.0","No",\n'
    )

    got, errors = apply_status_csv(df, str(csv_file))

    assert len(errors) == 1
    assert got.loc[0, "Status"] == STATUS_RESPONSE_NEEDED


def test_apply_repeater_csv_edits_existing_repeater(tmp_path):
    """A row matching an existing callsign/frequency updates it in place rather than adding a new one."""
    df = pd.DataFrame.from_records([
        {"Callsign": "W7DX", "Output (MHz)": "147.0000", "Offset (MHz)": "-0.6", "Tone (Hz)": "100.0",
         "Group Name": "WWDXC", "Status": STATUS_IN, "Location": "", "Coordinates": None},
    ])
    csv_file = tmp_path / "repeater.csv"
    csv_file.write_text(
        "Timestamp,Your Email,Club / Group Name,Repeater Callsign,Output Frequency (MHz),Offset (MHz),"
        "Tone (Hz or Dnnn for DCS),Club / Group Website,Link to repeater on RepeaterBook,"
        "Allow contacts via Allstar/Echolink/YSF/D-Star (if applicable)?,Allstar/Echolink info (if applicable),"
        '"Approximate Location (e.g. Capitol Hill, Seattle, WA)","Approximate Coordinates (e.g. 47.6395, -122.3693)"\n'
        "10/19/2026,rfanfant@hotmail.com,WWDXC,W7DX,147,-0.6,103.5,https://www.wwdxc.org/,,"
        "Yes,,Redmond,\"47.67459, -122.05393\"\n"
    )

    got, errors = apply_repeater_csv(df, str(csv_file))

    assert errors == []
    assert len(got) == 1
    assert got.loc[0, "Tone (Hz)"] == "103.5"
    assert got.loc[0, "Status"] == STATUS_IN  # existing status untouched
    assert got.loc[0, "Location"] == "Redmond"
    assert got.loc[0, "Coordinates"] == [47.67459, -122.05393]


def test_apply_repeater_csv_does_not_change_group_name_of_existing_repeater(tmp_path):
    """Editing an existing repeater never overwrites its Group Name from the CSV."""
    df = pd.DataFrame.from_records([
        {"Callsign": "W7DX", "Output (MHz)": "147.0000", "Offset (MHz)": "-0.6", "Tone (Hz)": "100.0",
         "Group Name": "WWDXC", "Status": STATUS_IN},
    ])
    csv_file = tmp_path / "repeater.csv"
    csv_file.write_text(
        "Club / Group Name,Repeater Callsign,Output Frequency (MHz),Offset (MHz),"
        "Tone (Hz or Dnnn for DCS),Club / Group Website,Link to repeater on RepeaterBook,"
        "Allow contacts via Allstar/Echolink/YSF/D-Star (if applicable)?,Allstar/Echolink info (if applicable),"
        '"Approximate Location (e.g. Capitol Hill, Seattle, WA)","Approximate Coordinates (e.g. 47.6395, -122.3693)"\n'
        "Some Other Club,W7DX,147,-0.6,103.5,https://www.wwdxc.org/,,No,,Redmond,\n"
    )

    got, errors = apply_repeater_csv(df, str(csv_file))

    assert errors == []
    assert got.loc[0, "Group Name"] == "WWDXC"


def test_apply_repeater_csv_clears_internet_access_when_answer_is_no(tmp_path):
    """Editing an existing repeater to answer "No" clears a previously-set Internet Access value."""
    df = pd.DataFrame.from_records([
        {"Callsign": "W7DX", "Output (MHz)": "147.0000", "Offset (MHz)": "-0.6", "Tone (Hz)": "100.0",
         "Group Name": "WWDXC", "Status": STATUS_IN,
         "Allow Internet Contacts": "Yes", "Internet Access": "47909"},
    ])
    csv_file = tmp_path / "repeater.csv"
    csv_file.write_text(
        "Club / Group Name,Repeater Callsign,Output Frequency (MHz),Offset (MHz),"
        "Tone (Hz or Dnnn for DCS),Club / Group Website,Link to repeater on RepeaterBook,"
        "Allow contacts via Allstar/Echolink/YSF/D-Star (if applicable)?,Allstar/Echolink info (if applicable),"
        '"Approximate Location (e.g. Capitol Hill, Seattle, WA)","Approximate Coordinates (e.g. 47.6395, -122.3693)"\n'
        "WWDXC,W7DX,147,-0.6,103.5,https://www.wwdxc.org/,,No,,Redmond,\n"
    )

    got, errors = apply_repeater_csv(df, str(csv_file))

    assert errors == []
    assert got.loc[0, "Allow Internet Contacts"] == "No"
    assert got.loc[0, "Internet Access"] == ""


def test_apply_repeater_csv_adds_new_repeater(tmp_path):
    """A row with no matching callsign/frequency is added as a new repeater needing a response."""
    df = pd.DataFrame.from_records([
        {"Callsign": "W7DX", "Output (MHz)": "147.0000", "Group Name": "WWDXC", "Status": STATUS_IN},
    ])
    csv_file = tmp_path / "repeater.csv"
    csv_file.write_text(
        "Club / Group Name,Repeater Callsign,Output Frequency (MHz),Offset (MHz),"
        "Tone (Hz or Dnnn for DCS),Club / Group Website,Link to repeater on RepeaterBook,"
        "Allow contacts via Allstar/Echolink/YSF/D-Star (if applicable)?,Allstar/Echolink info (if applicable),"
        '"Approximate Location (e.g. Capitol Hill, Seattle, WA)","Approximate Coordinates (e.g. 47.6395, -122.3693)"\n'
        "WWDXC,W7NEW,440.000,5.0,DCS123,https://www.wwdxc.org/,,No,,Somewhere,\n"
    )

    got, errors = apply_repeater_csv(df, str(csv_file))

    assert errors == []
    assert len(got) == 2
    new = got.loc[got["Callsign"] == "W7NEW"].iloc[0]
    assert new["Output (MHz)"] == "440.0000"
    assert new["Offset (MHz)"] == "+5.0"
    assert new["Status"] == STATUS_RESPONSE_NEEDED
    assert new["Mode"] == "FM"
