import datasets as ds
import constants as c
import datetime

today = datetime.datetime(2021, 5, 15)

print(ds.incidentsRate(ds.Cases, today))