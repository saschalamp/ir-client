from typing import List
from ir_client.utils.collections import defaultordereddict #TODO extract different lib
from datetime import datetime, timezone
from itertools import groupby

from ir_client.exceptions import MappingException
from ir_client.series_race_results.models import (
    SeriesRaceClassResult,
    SeriesRaceResult,
    SeriesRaceResultsSlot,
    SeriesRaceResultCollection
)

def map_series_race_results(data) -> SeriesRaceResultCollection:
    try:
        headers = {name: pos for (pos, name) in data['m'].items()}
        slots = defaultordereddict(lambda: SeriesRaceResultsSlot())
        slot_data = groupby(data['d'], lambda race: race[headers['start_time']])
        for start_time, splits in slot_data:
            dt_start_time = datetime.fromtimestamp(start_time / 1e3, tz=timezone.utc)
            split_data = groupby(splits, lambda race: race[headers['subsessionid']])
            split = 1
            for subsession_id, subsession_results in split_data:
                total_field_size = 0
                classes = {}
                for class_results in subsession_results:
                    car_class_id = class_results[headers["carclassid"]]
                    field_size = class_results[headers['sizeoffield']]
                    
                    classes[car_class_id] = SeriesRaceClassResult(
                        field_size=field_size,
                        strength_of_field=class_results[headers['strengthoffield']]
                    )

                    total_field_size += field_size
                result = SeriesRaceResult(
                    subsession_id=subsession_id,
                    total_field_size=total_field_size,
                    split=split,
                    classes=classes
                )
                slots[dt_start_time].results.append(result)
                split += 1
        return SeriesRaceResultCollection(slots=slots)
    except KeyError:
        raise InvalidSeriesRaceResultsDataException()


class InvalidSeriesRaceResultsDataException(MappingException):
    pass
