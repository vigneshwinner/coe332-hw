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

    #Create an error if all inputs are not numbers
    if not all(isinstance(val, (int, float)) for val in [lat1, lon1, lat2, lon2]):
        raise ValueError("All inputs must be a number")

    #Create a warning if invalid latitudes or longitudes
    if (lat1 < -90 or lat1 > 90) or (lat2 < -90 or lat2 > 90):
        logging.warning("Latitude must be between -90 and 90 degrees")
        return -1
     if (lon1 < -180 or lon1 > 180) or (lon2 < -180 or lon2 > 180):
        logging.warning("Longitude must be between -180 and 180 degrees")
        return -1

    try:
        R = 6371.0  #Radius of Earth (km)
        latitude1, latitude2 = math.radians(lat1), math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = math.sin(dlat/2)**2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(dlon/2)**2
        logging.debug(f"Central Angle is: {a} radians")

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    #Show if error occurs
    except ValueError as e:
        logging.error(f"Error Occured: {e}")
        return -1
