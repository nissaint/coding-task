from loguru import logger
from link_station import get_best_link_station


if __name__ == "__main__":
    link_stations = [[0, 0, 10], [20, 20, 5], [10, 0, 12]]
    device_points = [(0, 0), (100, 100), (15, 10), (18, 18)]

    try:
        for device_point in device_points:
            print(get_best_link_station(link_stations=link_stations, device=device_point))
    except ValueError as e:
        logger.error(e)
