from pathlib import Path

import pandas as pd

from score import club_link, score_competition, signal_report_to_readability


def test_club_link():
    assert club_link("Club", "https://x.org") == "[Club](https://x.org)"
    assert club_link("Club", float("nan")) == "Club"
    assert club_link("Club", None) == "Club"
    assert club_link("Club", "") == "Club"
    assert club_link(pd.NA, "https://x.org") == ""
    assert club_link(float("nan"), float("nan")) == ""


def test_signal_report_to_readability_tolerates_nan():
    """A non-string (e.g. NaN, from a pandas column holding unparseable reports) should not crash."""
    assert signal_report_to_readability(float("nan")) is None
    assert signal_report_to_readability(pd.NA) is None


def test_signal_report_to_readability_strips_stray_characters():
    """A stray typo'd character (e.g. a backtick) shouldn't prevent an otherwise-valid report from parsing."""
    assert signal_report_to_readability("CM5`") == 5
    assert signal_report_to_readability("5'9") == 5
    assert signal_report_to_readability("!59") == 5


def _repeaters_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "RR#": [1, 2, 25, 29],
            "Output (MHz)": [146.52, 440.0, 146.96, 146.96],
            "Group Name": ["Club A", "Club B", "Club C", "Club C"],
            "Long Name": ["Club A Full Name", "Club B Full Name", "Club C Full Name", "Club C Full Name"],
            "Location": ["Here", "There", "Here too", "Here too"],
            "Website": ["", "", "", ""],
        }
    )


def _write_template(assets_dir: Path) -> None:
    template_dir = assets_dir / "templates"
    template_dir.mkdir(parents=True)
    (template_dir / "personal_results.md").write_text(
        "{{ callsign_url }} {{ callsign }}\n{{ summary }}\n{{ logs }}\n"
    )
    (assets_dir.parent / "results").mkdir()


def test_score_competition_skips_log_with_unrecognized_columns(tmp_path, monkeypatch, capsys):
    """A log file missing the required columns entirely should be reported, not crash the run."""
    monkeypatch.chdir(tmp_path)
    _write_template(tmp_path / "assets")

    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "GOOD - Good Caller.csv").write_text(
        "Date,Time,Contact's Callsign,Signal Report,RR#,QRP\n2026-01-01,1200,KJ7EXM,59,1,\n"
    )
    # No recognizable callsign/report columns at all.
    (logs_dir / "BAD - Bad Caller.csv").write_text("Date,Time,Foo,Bar,RR#,QRP\n2026-01-01,1200,x,y,1,\n")

    leaderboard, *_ = score_competition(_repeaters_df(), logs_dir=str(logs_dir))

    assert "GOODCALLER" not in leaderboard["Callsign"].str.cat()  # sanity: callsign comes from filename stem
    assert leaderboard["Callsign"].str.contains("GOOD").any()
    assert not leaderboard["Callsign"].str.contains("BAD").any()

    captured = capsys.readouterr()
    assert "BAD - Bad Caller.csv" in captured.out


def test_score_competition_tolerates_header_case_and_whitespace(tmp_path, monkeypatch):
    """Headers that differ only by case/whitespace from the expected ones should still be scored."""
    monkeypatch.chdir(tmp_path)
    _write_template(tmp_path / "assets")

    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "WEIRD - Weird Caller.csv").write_text(
        "DATE,TIME,CALLSIGN,SIGNAL REPORT ,RR#,QRP\n2026-01-01,1200,KJ7EXM,5,1,\n"
    )

    leaderboard, *_ = score_competition(_repeaters_df(), logs_dir=str(logs_dir))

    assert leaderboard["Callsign"].str.contains("WEIRD").any()


def test_score_competition_reports_unparseable_signal_report_without_crashing(tmp_path, monkeypatch, capsys):
    """An invalid (but non-empty) signal report should be reported, not crash the run."""
    monkeypatch.chdir(tmp_path)
    _write_template(tmp_path / "assets")

    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "GOOD - Good Caller.csv").write_text(
        "Date,Time,Contact's Callsign,Signal Report,RR#,QRP\n"
        "2026-01-01,1200,KJ7EXM,59,1,\n"
        "2026-01-01,1201,N7ITU,not-a-report,2,\n"
    )

    leaderboard, *_ = score_competition(_repeaters_df(), logs_dir=str(logs_dir))

    assert leaderboard["Callsign"].str.contains("GOOD").any()
    captured = capsys.readouterr()
    assert "line 3" in captured.out
    assert "2026-01-01,1201,N7ITU,not-a-report,2," in captured.out


def test_score_competition_returns_contacts(tmp_path, monkeypatch):
    """The scored contacts (logger, contacted station, repeater) are returned for the pew pew map."""
    monkeypatch.chdir(tmp_path)
    _write_template(tmp_path / "assets")
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "KI6KTE - Matt.csv").write_text(
        "Date,Time,Contact's Callsign,Signal Report,RR#,QRP\n"
        "2026-01-01,1200,kj7exm,59,1,\n"
        "2026-01-01,1201,N7ITU,59,2,\n"
    )

    *_, contacts = score_competition(_repeaters_df(), logs_dir=str(logs_dir))

    assert contacts.to_numpy().tolist() == [["KI6KTE", "KJ7EXM", 1], ["KI6KTE", "N7ITU", 2]]


def test_score_competition_contacts_use_merged_repeater_numbers(tmp_path, monkeypatch):
    """Contacts logged against a duplicate repeater (e.g. RR# 29) should come back merged into RR# 25,
    matching by_repeater/the leaderboard, so the pew pew map doesn't draw a separate node for the dupe."""
    monkeypatch.chdir(tmp_path)
    _write_template(tmp_path / "assets")
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "KI6KTE - Matt.csv").write_text(
        "Date,Time,Contact's Callsign,Signal Report,RR#,QRP\n2026-01-01,1200,KJ7EXM,59,29,\n"
    )

    *_, contacts = score_competition(_repeaters_df(), logs_dir=str(logs_dir))

    assert contacts.to_numpy().tolist() == [["KI6KTE", "KJ7EXM", 25]]
