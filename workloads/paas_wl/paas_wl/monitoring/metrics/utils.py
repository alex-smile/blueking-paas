# -*- coding: utf-8 -*-
import datetime
from dataclasses import dataclass
from typing import Union

from django.utils import timezone

from paas_wl.utils.basic import get_time_delta


@dataclass
class MetricSmartTimeRange:
    """
    A smart model for handling time range

    - transfer date string to a correct format
    - provider quick access time range by timedelta or simple time phase (1s/1m/1h etc.)
    """

    # start & end will be formatted as unix timestamp
    start: str = ''
    end: str = ''
    # prometheus default interval
    step: str = '15s'
    # if time_range_str, override start & end
    # timedelta or time phase both support
    time_range_str: Union[datetime.timedelta, str] = ''
    time_format = "%Y-%m-%d %H:%M:%S"

    def __hash__(self):
        return hash(self.start + self.end)

    @classmethod
    def from_request_data(cls, data):
        # transfer 1s/2m/3h to timedelta
        if data.get('time_range_str'):
            return cls(time_range_str=data['time_range_str'], step=data['step'])
        else:
            return cls(start=data['start_time'], end=data['end_time'], step=data['step'])

    @staticmethod
    def _bake_timestamp(timestamp):
        return str(round(timestamp))

    def range_to_delta(self):
        if isinstance(self.time_range_str, datetime.timedelta):
            return

        elif isinstance(self.time_range_str, str):
            self.time_range_str = get_time_delta(self.time_range_str)
            return

        else:
            raise ValueError("to_now only support timedelta and time phase")

    def __post_init__(self):
        if self.time_range_str:
            # make sure to_now is instance of timedelta
            self.range_to_delta()

            end = timezone.localtime()
            start = end - self.time_range_str

            self.end = self._bake_timestamp(end.timestamp())
            self.start = self._bake_timestamp(start.timestamp())
        else:
            self.start = self._bake_timestamp(
                timezone.make_aware(datetime.datetime.strptime(self.start, self.time_format)).timestamp()
            )
            self.end = self._bake_timestamp(
                timezone.make_aware(datetime.datetime.strptime(self.end, self.time_format)).timestamp()
            )

            if int(self.start) > int(self.end):
                raise ValueError("start should earlier than end")

    def to_dict(self):
        return {'start': self.start, 'end': self.end, 'step': self.step}
