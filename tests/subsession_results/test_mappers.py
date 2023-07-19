from datetime import datetime, timezone

import pytest
from assertpy import assert_that

from ir_client.subsession_results import mappers
from ir_client.subsession_results.mappers import InvalidSubsessionResultsDataException
from ir_client.subsession_results.models import SimSessionDriverEntry, SimSession
from ir_client.subsession_results.models import SimSessionTeamEntry
from ir_client.subsession_results.models import SimSessionType
from ir_client.subsession_results.models import SubsessionResults


def test_map_subsession_results_empty_dict():
    with pytest.raises(InvalidSubsessionResultsDataException):
        mappers.map_subsession_results({})


def test_map_subsession_results_no_entries():
    with pytest.raises(InvalidSubsessionResultsDataException):
        mappers.map_subsession_results({'rows': []})


def test_map_subsession_results_solo_open_qualifying():
    __test_map_subsession_results_solo('Open+Qualifying')


def test_map_subsession_results_solo_lone_qualifying():
    __test_map_subsession_results_solo('Lone+Qualifying')


def __test_map_subsession_results_solo(qualifying_type):
    data = {
        'driver_changes': 0,
        'max_team_drivers': 1,
        'subsessionid': 37253536,
        'start_time': '2021-02-04+22%3A30%3A45',
        "simulatedstarttime": "2021-03-04+12%3A00",
        'rows': [
            {
                'custid': 273159,
                'displayname': 'Markus+Dec',
                'simsestypename': 'Race',
                'simsesnum': 0,
                'carclassid': 2523,
                "ccName": "Dallara+P217",
                'carid': 88,
                'car_name': 'Dallara+P217',
                'finishposinclass': 1,
                'finishpos': 1,
                'oldirating': 3908,
                'newirating': 4036,
                'bestlaptime': 1517825
            },
            {
                'custid': 273159,
                'displayname': 'Markus+Dec',
                'simsestypename': qualifying_type,
                'simsesnum': -1,
                'carclassid': 2523,
                "ccName": "Dallara+P217",
                'carid': 88,
                'car_name': 'Dallara+P217',
                'finishposinclass': 1,
                'finishpos': 1,
                'oldirating': 2063,
                'newirating': 2063,
                'bestlaptime': 1451774
            },
            {
                'custid': 273159,
                'displayname': 'Markus+Dec',
                'simsestypename': 'Open+Practice',
                'simsesnum': -2,
                'carclassid': 2523,
                "ccName": "Dallara+P217",
                'carid': 88,
                'car_name': 'Dallara+P217',
                'finishposinclass': 1,
                'finishpos': 1,
                'oldirating': 2063,
                'newirating': 2063,
                'bestlaptime': 1454744
            }
        ]
    }

    actual = mappers.map_subsession_results(data)

    expected = SubsessionResults(
        subsession_id=37253536,
        start_time=datetime(2021, 2, 4, hour=22, minute=30, second=45, tzinfo=timezone.utc),
        simulated_start_time=datetime(2021, 3, 4, hour=12, minute=0, tzinfo=timezone.utc),
        team_session=False,
        sim_session_results={
            SimSessionType.QUALIFY:
                SimSession(
                    number=-1,
                    entries=[
                        SimSessionDriverEntry(
                            entry_id=273159,
                            entry_name='Markus Dec',
                            car_class_id=2523,
                            car_class_name="Dallara P217",
                            car_id=88,
                            car_name="Dallara P217",
                            finish_position=1,
                            finish_position_class=1,
                            best_lap_time=1451774,
                            old_irating=2063,
                            new_irating=2063
                        )
                    ]
                ),
            SimSessionType.RACE:
                SimSession(
                    number=0,
                    entries=[
                        SimSessionDriverEntry(
                            entry_id=273159,
                            entry_name='Markus Dec',
                            car_class_id=2523,
                            car_class_name="Dallara P217",
                            car_id=88,
                            car_name="Dallara P217",
                            finish_position=1,
                            finish_position_class=1,
                            best_lap_time=1517825,
                            old_irating=3908,
                            new_irating=4036
                        )
                    ]
                )
        }
    )

    assert_that(actual).is_equal_to(expected)


def test_map_subsession_results_team_simsession():
    data = {
        'driver_changes': 1,
        'max_team_drivers': 2,
        'subsessionid': 37253536,
        'start_time': '2021-02-04+22%3A30%3A45',
        "simulatedstarttime": "2021-03-04+12%3A00",
        'rows': [
            {
                'custid': -150692,
                'groupid': -150692,
                'displayname': 'Porsche24+driven+by+Redline',
                'simsestypename': 'Race',
                'simsesnum': 0,
                'carclassid': 2523,
                "ccName": "Dallara+P217",
                'carid': 88,
                "car_name": "Dallara+P217",
                'finishposinclass': 1,
                'finishpos': 1,
                'bestlaptime': 1214669
            },
            {
                'custid': 273159,
                'groupid': -150692,
                'displayname': 'Markus+Dec',
                'simsestypename': 'Race',
                'simsesnum': 0,
                'carclassid': 2523,
                "ccName": "Dallara+P217",
                'carid': 88,
                "car_name": "Dallara+P217",
                'finishposinclass': 1,
                'finishpos': 1,
                'oldirating': 1206,
                'newirating': 1066,
                'bestlaptime': 1584680
            },
            {
                'custid': 232715,
                'groupid': -150692,
                'displayname': 'Anders+Myhre',
                'simsestypename': 'Race',
                'simsesnum': 0,
                'carclassid': 2523,
                "ccName": "Dallara+P217",
                'carid': 88,
                "car_name": "Dallara+P217",
                'finishposinclass': 1,
                'finishpos': 1,
                'oldirating': 983,
                'newirating': 878,
                'bestlaptime': 1578564
            },
            {
                'custid': -150692,
                'groupid': -150692,
                'displayname': 'Porsche24+driven+by+Redline',
                'simsestypename': 'Open+Qualifying',
                'simsesnum': -1,
                'carclassid': 2523,
                "ccName": "Dallara+P217",
                'carid': 88,
                "car_name": "Dallara+P217",
                'finishposinclass': 1,
                'finishpos': 1,
                'bestlaptime': 1214669
            },
            {
                'custid': 273159,
                'groupid': -150692,
                'displayname': 'Markus+Dec',
                'simsestypename': 'Open+Qualifying',
                'simsesnum': -1,
                'carclassid': 2523,
                "ccName": "Dallara+P217",
                'carid': 88,
                "car_name": "Dallara+P217",
                'finishposinclass': 1,
                'finishpos': 1,
                'oldirating': 1206,
                'newirating': 1206,
                'bestlaptime': 1299471
            },
            {
                'custid': -215159,
                'groupid': -215159,
                'displayname': 'BMW+Team+Redline',
                'simsestypename': 'Race',
                'simsesnum': 0,
                'carclassid': 4,
                "ccName": "GT4+Nurb",
                'carid': 5,
                "car_name": "Mercedes+GT4",
                'finishposinclass': 2,
                'finishpos': 2,
                'bestlaptime': 1223129
            },
            {
                'custid': 199325,
                'groupid': -215159,
                'displayname': 'Maximilian Benecke',
                'simsestypename': 'Race',
                'simsesnum': 0,
                'carclassid': 4,
                "ccName": "GT4+Nurb",
                'carid': 5,
                "car_name": "Mercedes+GT4",
                'finishposinclass': 2,
                'finishpos': 2,
                'oldirating': 4539,
                'newirating': 4411,
                'bestlaptime': 1478546
            },
            {
                'custid': 168966,
                'groupid': -215159,
                'displayname': 'Max Verstappen',
                'simsestypename': 'Race',
                'simsesnum': 0,
                'carclassid': 4,
                "ccName": "GT4+Nurb",
                'carid': 5,
                "car_name": "Mercedes+GT4",
                'finishposinclass': 2,
                'finishpos': 2,
                'oldirating': 5845,
                'newirating': 5889,
                'bestlaptime': 1530723
            },
            {
                'custid': -150692,
                'groupid': -150692,
                'displayname': 'Porsche24+driven+by+Redline',
                'simsestypename': 'Open+Practice',
                'simsesnum': -2,
                'carclassid': 2523,
                "ccName": "Dallara+P217",
                'carid': 88,
                "car_name": "Dallara+P217",
                'finishposinclass': 1,
                'finishpos': 1,
                'bestlaptime': 1234567
            },
            {
                'custid': 273159,
                'groupid': -150692,
                'displayname': 'Markus+Dec',
                'simsestypename': 'Open+Practice',
                'simsesnum': -2,
                'carclassid': 2523,
                "ccName": "Dallara+P217",
                'carid': 88,
                "car_name": "Dallara+P217",
                'finishposinclass': 1,
                'finishpos': 1,
                'oldirating': 2063,
                'newirating': 2063,
                'bestlaptime': 1234567
            }
        ]
    }
    expected = SubsessionResults(
        subsession_id=37253536,
        start_time=datetime(2021, 2, 4, hour=22, minute=30, second=45, tzinfo=timezone.utc),
        simulated_start_time=datetime(2021, 3, 4, hour=12, minute=0, tzinfo=timezone.utc),
        team_session=True,
        sim_session_results={
            SimSessionType.QUALIFY:
                SimSession(
                    number=-1,
                    entries=[
                        SimSessionTeamEntry(
                            entry_id=-150692,
                            entry_name='Porsche24 driven by Redline',
                            car_class_id=2523,
                            car_class_name="Dallara P217",
                            car_id=88,
                            car_name="Dallara P217",
                            finish_position=1,
                            finish_position_class=1,
                            best_lap_time=1214669,
                            drivers=[
                                SimSessionDriverEntry(
                                    entry_id=273159,
                                    entry_name='Markus Dec',
                                    car_class_id=2523,
                                    car_class_name="Dallara P217",
                                    car_id=88,
                                    car_name="Dallara P217",
                                    finish_position=1,
                                    finish_position_class=1,
                                    best_lap_time=1299471,
                                    old_irating=1206,
                                    new_irating=1206
                                )
                            ]
                        )
                    ]
                ),
            SimSessionType.RACE:
                SimSession(
                    number=0,
                    entries=[
                        SimSessionTeamEntry(
                            entry_id=-150692,
                            entry_name='Porsche24 driven by Redline',
                            car_class_id=2523,
                            car_class_name="Dallara P217",
                            car_id=88,
                            car_name="Dallara P217",
                            finish_position=1,
                            finish_position_class=1,
                            best_lap_time=1214669,
                            drivers=[
                                SimSessionDriverEntry(
                                    entry_id=273159,
                                    entry_name='Markus Dec',
                                    car_class_id=2523,
                                    car_class_name="Dallara P217",
                                    car_id=88,
                                    car_name="Dallara P217",
                                    finish_position=1,
                                    finish_position_class=1,
                                    best_lap_time=1584680,
                                    old_irating=1206,
                                    new_irating=1066
                                ),
                                SimSessionDriverEntry(
                                    entry_id=232715,
                                    entry_name='Anders Myhre',
                                    car_class_id=2523,
                                    car_class_name="Dallara P217",
                                    car_id=88,
                                    car_name="Dallara P217",
                                    finish_position=1,
                                    finish_position_class=1,
                                    best_lap_time=1578564,
                                    old_irating=983,
                                    new_irating=878
                                )
                            ]
                        ),
                        SimSessionTeamEntry(
                            entry_id=-215159,
                            entry_name='BMW Team Redline',
                            car_class_id=4,
                            car_class_name="GT4 Nurb",
                            car_id=5,
                            car_name="Mercedes GT4",
                            finish_position=2,
                            finish_position_class=2,
                            best_lap_time=1223129,
                            drivers=[
                                SimSessionDriverEntry(
                                    entry_id=199325,
                                    entry_name='Maximilian Benecke',
                                    car_class_id=4,
                                    car_class_name="GT4 Nurb",
                                    car_id=5,
                                    car_name="Mercedes GT4",
                                    finish_position=2,
                                    finish_position_class=2,
                                    best_lap_time=1478546,
                                    old_irating=4539,
                                    new_irating=4411
                                ),
                                SimSessionDriverEntry(
                                    entry_id=168966,
                                    entry_name='Max Verstappen',
                                    car_class_id=4,
                                    car_class_name="GT4 Nurb",
                                    car_id=5,
                                    car_name="Mercedes GT4",
                                    finish_position=2,
                                    finish_position_class=2,
                                    best_lap_time=1530723,
                                    old_irating=5845,
                                    new_irating=5889
                                )
                            ]
                        )
                    ]
                )
        }
    )
    actual = mappers.map_subsession_results(data)
    assert_that(actual).is_equal_to(expected)
