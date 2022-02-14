from typing import List, Union, Tuple
import numpy as np


def get_best_link_station(
    link_stations: List[List[Union[int, float]]],
    device: Tuple[Union[int, float], Union[int, float]],
) -> str:
    """
    Find the best link station (i.e. with most power) from a given list of link stations and a device.

    Parameters
    ----------
    link_stations : 2D list
        A list containing link station configs [x, y, r] where x,y denotes the position and r is the reach.
        e.g. [[0, 0, 10], [20, 20, 5], [10, 0, 12]]
    device : tuple
        A tuple (x,y) indicating the position of the device.

    Returns
    -------
    best_link_station: str
        The best link station for a given device position.
    """
    # validate device input
    if not (len(device) == 2 and all(isinstance(d, (int, float)) for d in device)):
        raise ValueError("Device should be a tuple/list of 2 ints/floats.")

    # validate link_stations input
    if not all(
        len(station) == 3 and all(isinstance(elem, (int, float)) for elem in station) for station in link_stations
    ):
        raise ValueError("Link_stations should be a list of lists each containing 3 ints/floats.")

    # Calculate best link station with the most power
    best_link_station = f"No link station within reach for point {device}"
    max_power = 0
    for link_station in link_stations:
        link_station_position = np.array(link_station[:2])
        link_station_reach = link_station[-1]
        l2_distance = np.linalg.norm(device - link_station_position)

        if l2_distance > link_station_reach:
            continue

        power = (link_station_reach - l2_distance)**2
        if max_power < power:
            max_power = power
            best_link_station = f"Best link station for point {device} is {link_station_position} with power {max_power}"

    return best_link_station
