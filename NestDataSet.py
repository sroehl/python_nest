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
        return self.get_values('temp')

    def get_target_temps(self):
        return self.get_values('target_temp')

    def get_outside_temps(self):
        return self.get_values('outside_temp')

    def get_states(self):
        dataset = self.get_values('state')
        modified_dataset = []
        min_range = self.get_min_range()
        for point in dataset:
            if point[1] != NestDataPoint.STATE_OFF:
                modified_dataset.append((point[0], min_range-1))
            else:
                modified_dataset.append((point[0], min_range-2))
        return modified_dataset

    def get_values(self, attribute):
        dataset = []
        if len(self.points) > 3:
            for i in range(0, len(self.points)):
                point = self.points[i]
                if i == 0 or i+1 >= len(self.points):
                    structTime = time.localtime(int(point.time))
                    dataset.append((datetime.datetime(*structTime[:6]), getattr(point, attribute)))
                else:
                    prev_point = self.points[i-1]
                    next_point = self.points[i+1]
                    if getattr(prev_point, attribute) != getattr(next_point, attribute):
                        structTime = time.localtime(int(point.time))
                        dataset.append((datetime.datetime(*structTime[:6]), getattr(point, attribute)))
        else:
            for point in self.points:
                structTime = time.localtime(int(point.time))
                dataset.append((datetime.datetime(*structTime[:6]), getattr(point, attribute)))
        print("attribute {} has length of {}".format(attribute, len(dataset)))
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
