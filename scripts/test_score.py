import pandas as pd

from score import club_link


def test_club_link():
    assert club_link("Club", "https://x.org") == "[Club](https://x.org)"
    assert club_link("Club", float("nan")) == "Club"
    assert club_link("Club", None) == "Club"
    assert club_link("Club", "") == "Club"
    assert club_link(pd.NA, "https://x.org") == ""
    assert club_link(float("nan"), float("nan")) == ""
