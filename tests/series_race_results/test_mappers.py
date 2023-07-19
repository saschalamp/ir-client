from collections import OrderedDict
import pytest
from assertpy import assert_that
import datetime

from ir_client.series_race_results import mappers
from ir_client.series_race_results.mappers import InvalidSeriesRaceResultsDataException
from ir_client.series_race_results.models import SeriesRaceResult, SeriesRaceResultCollection, SeriesRaceResultsSlot
from ir_client.utils.collections import DefaultOrderedDict, defaultordereddict

response_data_headers = {
    1: 'start_time',
    4: 'subsessionid'
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
                1: 1689392700000,
                4: 12345678
            },
            {
                1: 1689392700000,
                4: 12345678
            },
            {
                1: 1689392700000,
                4: 23456789
            },
            {
                1: 1689392700000,
                4: 34567890
            }
        ]
    }

    actual = mappers.map_series_race_results(data)

    expected_slot_1_time = datetime.datetime(2023, 7, 15, 3, 45, tzinfo=datetime.timezone.utc)
    expected_slot_1_results = [
        SeriesRaceResult( 
            subsession_id=12345678
        ),
        SeriesRaceResult(
            subsession_id=23456789
        ),
        SeriesRaceResult(
            subsession_id=34567890
        ),
    ]
    expected_slot_1 = SeriesRaceResultsSlot(results=expected_slot_1_results)
    expected = SeriesRaceResultCollection(
        slots=OrderedDict({
            expected_slot_1_time: expected_slot_1
        })
    )

    assert_that(actual).is_equal_to(expected)
