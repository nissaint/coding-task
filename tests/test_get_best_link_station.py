from link_station import get_best_link_station
import numpy as np
import pytest


@pytest.fixture
def initialize_good_test_inputs():
    link_stations = [[0, 0, 10], [20, 20, 5], [10, 0, 12]]
    reachable_device = (0, 0)  # device position very close to the link stations
    unreachable_device = (100, 100)  # device position very far (unreachable) to the link stations
    devices = [reachable_device, unreachable_device]
    return link_stations, devices


@pytest.fixture
def initialize_bad_test_inputs():
    link_stations_incorrect_datatype = [[0, "0", 10], [20, 20, 5], [10, 0, 12]]
    link_stations_incorrect_length = [[0, 0, 10, 11], [20, 20, 5], [10, 0, 12]]
    device_incorrect_datatype = (0, "0")
    device_incorrect_length = (0, 0, 0)
    return (
        link_stations_incorrect_datatype,
        link_stations_incorrect_length,
        device_incorrect_datatype,
        device_incorrect_length,
    )


class TestGetBestLinkStation:
    def test_should_get_best_reachable_link_station(self, initialize_good_test_inputs):
        # Given
        link_stations, devices = initialize_good_test_inputs
        reachable_device, _ = devices

        # When
        output = get_best_link_station(link_stations=link_stations, device=reachable_device)

        # Then
        expected_best_link_station = link_stations[0]
        expected_best_pos = np.array(expected_best_link_station[:2])
        expected_best_power = float((expected_best_link_station[-1] - 0) ** 2)
        assert isinstance(output, str)
        assert output == (
            f"Best link station for point {reachable_device} is {expected_best_pos} with power {expected_best_power}"
        )

    def test_should_return_unreachable_link_station(self, initialize_good_test_inputs):
        # Given
        link_stations, devices = initialize_good_test_inputs
        _, unreachable_device = devices

        # When
        output = get_best_link_station(link_stations=link_stations, device=unreachable_device)

        # Then
        assert isinstance(output, str)
        assert output == f"No link station within reach for point {unreachable_device}"

    def test_should_return_error_if_invalid_inputs(
        self, initialize_good_test_inputs, initialize_bad_test_inputs
    ):
        # Given
        link_stations, devices = initialize_good_test_inputs
        ls_incorrect_type, ls_incorrect_length, d_incorrect_type, d_incorrect_length = initialize_bad_test_inputs

        # Case 1: invalid link stations datatype
        with pytest.raises(ValueError) as e_info1:
            get_best_link_station(link_stations=ls_incorrect_type, device=devices[0])

        # Case 2: invalid link stations length
        with pytest.raises(ValueError) as e_info2:
            get_best_link_station(link_stations=ls_incorrect_length, device=devices[0])

        # Case 3: invalid device datatype
        with pytest.raises(ValueError) as e_info3:
            get_best_link_station(link_stations=link_stations, device=d_incorrect_type)

        # Case 4: invalid device length
        with pytest.raises(ValueError) as e_info4:
            get_best_link_station(link_stations=link_stations, device=d_incorrect_length)

        # Then
        assert e_info1.value.__str__() == e_info2.value.__str__() == "Link_stations should be a list of lists each containing 3 ints/floats."
        assert e_info3.value.__str__() == e_info4.value.__str__() == "Device should be a tuple/list of 2 ints/floats."
