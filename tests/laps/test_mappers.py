import pytest
from assertpy import assert_that

from ir_client.laps import mappers
from ir_client.laps.mappers import InvalidLapDataException
from ir_client.laps.models import Laps, Lap, LapEvent
from ir_client.utils.enum_utils import IntEnumSet


def test_map_laps_empty_dict():
    with pytest.raises(InvalidLapDataException):
        mappers.map_laps({})


def test_map_laps_no_lap_data():
    data = {
        'lapData': []
    }
    expected = Laps(laps=[])
    actual = mappers.map_laps(data)
    assert_that(actual).is_equal_to(expected)


def test_map_laps_single_lap():
    data = {
        'lapData': [
            {
                "ses_time": 2024500,
                "custid": 199325,
                "flags": 0,
                "lap_num": 0
            }
        ]
    }
    expected = Laps(laps=[
        Lap(
            number=0,
            driver_id=199325,
            session_time_eol=2024500,
            lap_events=IntEnumSet(LapEvent, 0)
        )
    ])
    actual = mappers.map_laps(data)
    assert_that(actual.laps[0].lap_events).is_equal_to(expected.laps[0].lap_events)
    assert_that(actual).is_equal_to(expected)
