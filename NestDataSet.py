from NestDataPoint import NestDataPoint
import time
import datetime


class NestDataSet:

    def __len__(self):
        return len(self.points)

    def add_point(self, ndp):
        self.points.append(ndp)

    def get_times(self):
        times = []
        for point in self.points:
            times.append(point.time)
        return times

    def get_temps(self):
        dataset = []
        for point in self.points:
            structTime = time.localtime(int(point.time))
            dataset.append((datetime.datetime(*structTime[:6]), point.temp))
        return dataset

    def get_target_temps(self):
        dataset = []
        for point in self.points:
            structTime = time.localtime(int(point.time))
            dataset.append((datetime.datetime(*structTime[:6]), point.target_temp))
        return dataset

    def get_outside_temps(self):
        dataset = []
        for point in self.points:
            structTime = time.localtime(int(point.time))
            dataset.append((datetime.datetime(*structTime[:6]), point.outside_temp))
        return dataset

    def get_states(self):
        dataset = []
        min_range = self.get_min_range()
        for point in self.points:
            structTime = time.localtime(int(point.time))
            if point.state != NestDataPoint.STATE_OFF:
                dataset.append((datetime.datetime(*structTime[:6]), min_range-1))
            else:
                dataset.append((datetime.datetime(*structTime[:6]), min_range-2))
        return dataset

    def get_min_temp(self):
        min = self.points[0].temp
        for point in self.points:
            if point.temp < min:
                min = point.temp
        return min

    def get_max_temp(self):
        max = self.points[0].temp
        for point in self.points:
            if point.temp > max:
                max = point.temp

    def get_max_range(self):
        max = self.points[0].temp
        for point in self.points:
            if point.temp > max:
                max = point.temp
            if point.target_temp > max:
                max = point.target_temp
            if point.outside_temp > max:
                max = point.outside_temp
        return max

    def get_min_range(self):
        min = self.points[0].temp
        for point in self.points:
            if point.temp < min:
                min = point.temp
            if point.target_temp < min:
                min = point.target_temp
            if point.outside_temp < min:
                min = point.outside_temp
        return min-1

    def __init__(self):
        self.points = []
