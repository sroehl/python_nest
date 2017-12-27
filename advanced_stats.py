from stats import *
import scipy.stats
import numpy as np


def get_stats(function):
    print(function.__name__)
    data_set = []
    for x in range(1,31):
        data_set += function(2017, 11, x)
    for x in range(1,31):
        data_set += function(2017, 12, x)
        #data_set += get_leakage_heat_for_date(2017, 11, x)
    print("Found {} points".format(len(data_set)))
    data_set = remove_outliers(data_set)
    npa = np.asarray(data_set)
    x = np.hsplit(npa, 2)[0]
    y = np.hsplit(npa, 2)[1]

    x = np.reshape(x, (x.size,))
    y = np.reshape(y, (y.size,))
    print(scipy.stats.linregress(x, y))
    print(scipy.stats.histogram(y, numbins=30, defaultlimits=(0,30)))
    print("Mean: {}".format(np.mean(y)))
    print("STDEV: {}".format(np.std(y)))
    print("\n\n")

get_stats(get_warmup_time)
get_stats(get_leakage_heat_for_date)
