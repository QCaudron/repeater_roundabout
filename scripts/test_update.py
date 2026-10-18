from datetime import datetime

import pytest

from update import rollover


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
    assert (tmp_path / "assets" / "repeaters.json").read_text() == "[]"
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
