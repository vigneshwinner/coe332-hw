import pytest
from datetime import datetime
from worker import parse_date, get_hgnc_ids_in_range

def test_parse_date_valid():
    date_str = "12/7/1989"
    dt = parse_date(date_str)
    assert isinstance(dt, datetime)
    assert dt.year == 1989
    assert dt.month == 12
    assert dt.day == 7

def test_parse_date_with_spaces():
    date_str = " 3/1/2013 "
    dt = parse_date(date_str)
    assert dt.year == 2013
    assert dt.month == 3
    assert dt.day == 1

def test_get_hgnc_ids_in_range(monkeypatch):
    from jobs import rd
    def fake_keys(pattern):
        return [b"gene:HGNC:5", b"gene:HGNC:7", b"gene:HGNC:10"]
    monkeypatch.setattr(rd, "keys", fake_keys)
    ids = get_hgnc_ids_in_range("HGNC:5", "HGNC:10")
    assert set(ids) == {"HGNC:5", "HGNC:7", "HGNC:10"}
