import pytest
import math
from datetime import datetime, timezone, timedelta
from iss_tracker import compute_speed, find_closest_epoch, compute_average_speed

def test_compute_speed():
    """Tests if compute_speed correctly calculates vector magnitude."""
    assert math.isclose(compute_speed((1, 2, 2)), 3.0, rel_tol=1e-3)
    assert math.isclose(compute_speed((3, 4, 0)), 5.0, rel_tol=1e-3)
    assert math.isclose(compute_speed((6, 8, 0)), 10.0, rel_tol=1e-3)

def test_find_closest_epoch():
    """Tests if find_closest_epoch returns the closest time."""
    now = datetime.now(timezone.utc)  # Capture once

    sample_data = [
        {"epoch": now - timedelta(minutes=2), "position": (100, 200, 300), "velocity": (1, 2, 2)},
        {"epoch": now + timedelta(minutes=2), "position": (150, 250, 350), "velocity": (3, 4, 0)}
    ]

    closest = find_closest_epoch(sample_data, now)
    expected_epoch = min(sample_data, key=lambda d: (abs(d["epoch"] - now), d["epoch"]))["epoch"]

    assert closest["epoch"] == expected_epoch

def test_compute_average_speed():
    """Tests if compute_average_speed calculates the correct mean speed."""
    sample_data = [
        {"velocity": (3, 4, 0)},  # Speed = 5.0 km/s
        {"velocity": (0, 5, 12)}  # Speed = 13.0 km/s
    ]

    avg_speed = compute_average_speed(sample_data)
    expected_avg_speed = (5.0 + 13.0) / 2  # 9.0 km/s

    assert math.isclose(avg_speed, expected_avg_speed, rel_tol=1e-3)
