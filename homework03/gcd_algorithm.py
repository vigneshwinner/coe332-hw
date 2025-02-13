import math

def great_circle_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes the great-circle distance between two latitude/longitude points

    Args:
        lat1 (float): Latitude of point 1 (in degrees)
        lon1 (float): Longitude of point 1
        lat2 (float): Latitude of point 2
        lon2 (float): Longitude of point 2

    Returns:
        float: Distance (km)
    """

    #Creates error if inputs are not all numbers
    if None in [lat1, lon1, lat2, lon2]:
        raise ValueError("Latitude and longitude values cannot be empty")

    if not all(isinstance(val, (int, float)) for val in [lat1, lon1, lat2, lon2]):
        raise ValueError("All inputs must be a number")


    R = 6371.0  #Radius of Earth (km)
    latitude1, latitude2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = R * c

    return dist
