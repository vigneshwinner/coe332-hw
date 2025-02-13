from ml_data_analysis import heaviest_meteorite, calculate_avg_latitude
import pytest

def test_heaviest_meteorite():
    data = [{'name': 'A', 'mass (g)': '10'}, {'name': 'B', 'mass (g)': '20'}, {'name': 'C', 'mass (g)': '30'}]
    assert heaviest_meteorite(data)['name'] == 'C'

def test_calculate_avg_latitude():
    sample_data = [{'reclat': '10'}, {'reclat': '20'}, {'reclat': '30'}]
    assert calculate_avg_latitude(sample_data) == 20.0

def test_empty_list():
    assert calculate_avg_latitude([]) == 0
