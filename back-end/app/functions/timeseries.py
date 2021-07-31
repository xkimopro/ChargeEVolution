import json
import datetime
import statistics
import numpy as np

def computeGraph(connection_time, disconnection_time, kwh_delivered):
    sessionSeries = dict()
    total_kwh = float(kwh_delivered)
    it = datetime.datetime.strptime(disconnection_time, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(connection_time, '%Y-%m-%d %H:%M:%S')
    interval = it.total_seconds()/60
    series = np.random.normal(100, 25, int(interval))
    M = sum(series)
    series *= total_kwh/M
    series = [round(s,2) for s in series]
    mean = statistics.mean(series)
    sessionSeries['time_series'] = ",".join([str(i) for i in series])
    sessionSeries['mean'] = float(round(mean, 2))
    sessionSeries['variation'] = float(round(statistics.variance(series), 4))
    return sessionSeries
