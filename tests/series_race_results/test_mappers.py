from collections import OrderedDict
import pytest
from assertpy import assert_that
import datetime

from ir_client.series_race_results import mappers
from ir_client.series_race_results.mappers import InvalidSeriesRaceResultsDataException
from ir_client.series_race_results.models import SeriesRaceClassResult, SeriesRaceResult, SeriesRaceResultCollection, SeriesRaceResultsSlot
from ir_client.utils.collections import DefaultOrderedDict, defaultordereddict

response_data_headers = {
    "1": 'start_time',
    "2": "carclassid",
    "4": 'subsessionid',
    "7": "sizeoffield",
    "8": "strengthoffield"
}


def test_map_empty_dict():
    with pytest.raises(InvalidSeriesRaceResultsDataException):
        mappers.map_series_race_results({})


def test_map_no_rows():
    data = {
        'm': response_data_headers,
        'd': []
    }

    actual = mappers.map_series_race_results(data)

    expected = SeriesRaceResultCollection(slots={})

    assert_that(actual).is_equal_to(expected)


def test_map_some_results():
    data = {
        'm': response_data_headers,
        'd': [
            {
                "1": 1689392700000,
                "2": 1,
                "4": 12345678,
                "7": 22,
                "8": 8645
            },
            {
                "1": 1689392700000,
                "2": 2,
                "4": 12345678,
                "7": 20,
                "8": 1936
            },
            {
                "1": 1689392700000,
                "2": 1,
                "4": 23456789,
                "7": 16,
                "8": 4582
            },
            {
                "1": 1689392700000,
                "2": 1,
                "4": 34567890,
                "7": 11,
                "8": 8557
            },
            {
                "1": 1689399900000,
                "2": 1,
                "4": 674355663,
                "7": 12,
                "8": 8567
            }
        ]
    }

    actual = mappers.map_series_race_results(data)

    expected_slot_1_time = datetime.datetime(2023, 7, 15, 3, 45, tzinfo=datetime.timezone.utc)
    expected_slot_1_results = [
        SeriesRaceResult( 
            subsession_id=12345678,
            total_field_size=42,
            split=1,
            classes={
                1: SeriesRaceClassResult(
                    car_class_id=1,
                    field_size=22,
                    strength_of_field=8645
                ),
                2: SeriesRaceClassResult(
                    car_class_id=2,
                    field_size=20,
                    strength_of_field=1936
                ),
            }
        ),
        SeriesRaceResult(
            subsession_id=23456789,
            total_field_size=16,
            split=2,
            classes={
                1: SeriesRaceClassResult(
                    car_class_id=1,
                    field_size=16,
                    strength_of_field=4582
                ),
            }
        ),
        SeriesRaceResult(
            subsession_id=34567890,
            total_field_size=11,
            split=3,
            classes={
                1: SeriesRaceClassResult(
                    car_class_id=1,
                    field_size=11,
                    strength_of_field=8557
                ),
            }
        ),
    ]
    expected_slot_1 = SeriesRaceResultsSlot(results=expected_slot_1_results)
    
    expected_slot_2_time = datetime.datetime(2023, 7, 15, 5, 45, tzinfo=datetime.timezone.utc)
    expected_slot_2_results = [
        SeriesRaceResult( 
            subsession_id=674355663,
            total_field_size=12,
            split=1,
            classes={
                1: SeriesRaceClassResult(
                    car_class_id=1,
                    field_size=12,
                    strength_of_field=8567
                ),
            }
        ),
    ]
    expected_slot_2 = SeriesRaceResultsSlot(results=expected_slot_2_results)
    
    
    expected = SeriesRaceResultCollection(
        slots=OrderedDict({
            expected_slot_1_time: expected_slot_1,
            expected_slot_2_time: expected_slot_2,
        })
    )

    assert_that(actual).is_equal_to(expected)
