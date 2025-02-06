from gcd_algorithm import great_circle_distance

def test_great_circle_distance():
    assert round(great_circle_distance(0, 0, 2, 1), 2) == 248.63 #Used online Great Circle Calculator
