import re
import sys
from datetime import timedelta, datetime, time
import numpy as np
import pandas as pd
from string import ascii_uppercase
from collections import OrderedDict


pd.options.mode.chained_assignment = None


class PlateParserError(Exception):
    pass

class PlateParser:
    re_plate_well_data = "([A-H][0-1][0-9]):\s+([-+]?\d*\.\d+|\d+)"
    re_plate_time = "Time:\s+([0-2][0-9]):([0-9][0-9]):([0-9][0-9])"
    re_plate_date = "Date:\s+([0-3][0-9])/([0-1][0-9])/([0-9]+)"
    re_plate_testname = "(^.*|\n)Testname:\s+(.+)"
    
    def __init__(self, paths):
        self.last_timepoint = 0
        self.time_elapsed = timedelta(seconds=0)
        self._data = pd.DataFrame(columns=["testname"])
        self.parse_files(paths)
        self._data = self._data.sort_index()

    def re_match_testname(self, string):
        pat = re.compile(self.re_plate_testname, re.MULTILINE)
        mat = pat.match(string)

        if mat is not None:
            hit  = mat.groups()[1]
            return hit

    def re_match_time(self, string):
        pat = re.compile(self.re_plate_time, re.MULTILINE)
        mat = pat.search(string)

        if mat is not None:
            h = int(mat.groups()[0])
            m = int(mat.groups()[1])
            s = int(mat.groups()[2])
            return (h, m, s)

    def re_match_date(self, string):
        pat = re.compile(self.re_plate_date, re.MULTILINE)
        mat = pat.search(string)
        if mat is not None:
            day = int(mat.groups()[0])
            month = int(mat.groups()[1])
            year = int(mat.groups()[2])
            return(day, month, year)

    def re_match_well(self, string):
        pat = re.compile(self.re_plate_well_data)
        mat = pat.findall(string)
        if mat is not None:
            return mat

    def calculate_time_delta(self):
        current_as_delta = timedelta(hours=self.current_timepoint.hour, minutes=self.current_timepoint.minute, seconds=self.current_timepoint.second)
        last_as_delta = timedelta(hours=self.last_timepoint.hour, minutes=self.last_timepoint.minute, seconds=self.last_timepoint.second)
        if current_as_delta < last_as_delta:
            current_as_delta += timedelta(days=1)
        return current_as_delta - last_as_delta

    def parse_files(self, paths):
        if paths is None or not paths:
            raise PlateParserError("No input paths given!")
        for file_idx, path in enumerate(paths):
            with open(path) as f:
                data = f.read()
                datapoints = data.split("-"*86)
                for datapoint_idx, datapoint in enumerate(datapoints):
                    testname = self.re_match_testname(datapoint)
                    time = self.re_match_time(datapoint)
                    date = self.re_match_date(datapoint)
                    dt = datetime(day=date[0], month=date[1], year=date[2], hour=time[0], minute=time[1], second=time[2])
                    data = self.re_match_well(datapoint)

                    for pair in data:
                        well, value = pair[0], pair[1]
                        self._data.loc[dt, well] = value
                    self._data.loc[dt, "testname"] = testname

    @property
    def testnames(self):
        return list(set(self._data["testname"]))
    @property
    def dates(self):
        return self._data.index

    def plate_from_testname(self, testname):
        if testname not in self.testnames:
            raise ValueError("Testname {!r} is not a valid testname for your data".format(testname))
        data = self._data[self._data["testname"] == testname]
        return Plate(data, testname)

    def plate_from_daterange(self, start, end):
        if not isinstance(start, datetime):
            raise TypeError("Start date must be datetime")
        if not isinstance(end, datetime):
            raise TypeError("End date must be datetime")
        if not start in self.dates:
            raise ValueError("Invalid start date! Must be exact datetime match")
        if not end in self.dates:
            raise ValueError("Invalid end date! Must be exact datetime match")

        data = self._data[(self._data.index >= start) & (self._data.index <= end)]
        n_testnames = len(set(data['testname']))
        if n_testnames > 1:
            raise PlateParserError("More than one testname in the data range!")
        return Plate(data, data['testname'].values[1])
        

class Plate:
    def __init__(self, well_data, testname):
        self.data = well_data
        self.testname = testname

        elapsed = well_data.index - well_data.index[0]
        datetime = well_data.index.values

        self.data['elapsed'] = elapsed
        self.data['datetime'] = datetime
        self.data.index = pd.Series([i for i, x in enumerate(self.data.index)])
        cols = self.data.columns.tolist()
        move = [ "testname", "elapsed", "datetime"]
        for x in move:
            cols.remove(x)
        for i, x in enumerate(move):
            cols.insert(i, x)
        self.data = self.data[cols]

    def __repr__(self):
        return("Plate({!r})".format(self.testname))
    def __str__(self):
        return(str(self.data))

    @property
    def date_range(self):
        return "{} - {}".format(self.data["datetime"].iloc[0], self.data["datetime"].iloc[-1])

    @property
    def time_range(self):
        return "{} - {}".format(self.data['elapsed'].iloc[0], self.data['elapsed'].iloc[-1])

    @property
    def to_csv(self):
        return self.data.to_csv

if __name__ == "__main__":
    paths = sys.argv[1:]
    parser = PlateParser(paths)
    start = parser.dates[1]
    end = parser.dates[-1]
    plate = parser.plate_from_daterange(start, end)
    print(repr(plate.to_csv()))
