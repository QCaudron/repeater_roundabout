import json
import zipfile

import pytest

import uls


def _en(usi: int, call: str, zip_code: str) -> str:
    fields = ["EN", str(usi), "", "", call, "L"] + [""] * 24
    fields[15:19] = ["1 MAIN ST", "SEATTLE", "WA", zip_code]
    return "|".join(fields) + "\r\n"


def _fixtures(tmp_path):
    with zipfile.ZipFile(tmp_path / "l_amat.zip", "w") as z:
        z.writestr("EN.dat", _en(5, "KI6KTE", "981011234") + _en(9, "KI6KTE", "98402") + _en(3, "K7DRQ", "99999"))
    with zipfile.ZipFile(tmp_path / "zcta.zip", "w") as z:
        z.writestr(
            "zcta.txt",
            "GEOID\tALAND\tAWATER\tALAND_SQMI\tAWATER_SQMI\tINTPTLAT\tINTPTLONG   \n"
            "98101\t1\t1\t1\t1\t47.61\t-122.33   \n"
            "98402\t1\t1\t1\t1\t47.25\t-122.44   \n",
        )


def test_uls_zip_codes_takes_newest_license(tmp_path):
    _fixtures(tmp_path)
    assert uls.uls_zip_codes({"KI6KTE", "K7DRQ", "N0PE"}, tmp_path / "l_amat.zip") == {
        "KI6KTE": "98402",
        "K7DRQ": "99999",
    }


def test_zcta_centroids(tmp_path):
    _fixtures(tmp_path)
    assert uls.zcta_centroids(tmp_path / "zcta.zip") == {"98101": [47.61, -122.33], "98402": [47.25, -122.44]}


def test_ham_locations_looks_up_and_caches(tmp_path, monkeypatch):
    _fixtures(tmp_path)
    monkeypatch.setattr(uls, "DATA_DIR", tmp_path)
    files = {uls.ULS_URL: tmp_path / "l_amat.zip", uls.ZCTA_URL: tmp_path / "zcta.zip"}
    monkeypatch.setattr(uls, "download", lambda url, dest: files[url])

    # Portable suffixes are stripped; non-US calls are skipped; unknown ZIPs/calls get no location
    locations = uls.ham_locations(["KI6KTE/M", "K7DRQ", "N0PE", "VE7ABC"])
    assert locations == {"KI6KTE": [47.25, -122.44]}
    assert json.loads((tmp_path / "ham_locations.json").read_text()) == {
        "KI6KTE": [47.25, -122.44],
        "K7DRQ": None,
        "N0PE": None,
    }

    # Cached calls don't touch the network or the ULS file again
    def no_download(url, dest):
        raise AssertionError("should use cache")

    monkeypatch.setattr(uls, "download", no_download)
    assert uls.ham_locations(["KI6KTE", "N0PE"]) == {"KI6KTE": [47.25, -122.44]}


@pytest.mark.parametrize("call", ["KI6KTE", "W1AW", "AA7RM", "K7DRQ/P", "kk7zbx"])
def test_base_callsign_accepts_us_calls(call):
    assert uls.base_callsign(call) == call.upper().split("/")[0]


@pytest.mark.parametrize("call", ["VE7ABC", "</script>", "", "12345"])
def test_base_callsign_rejects_others(call):
    assert uls.base_callsign(call) is None
