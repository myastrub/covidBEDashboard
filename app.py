import datasets as ds
import constants as c
import pandas as pd
import datetime

today = datetime.datetime(datetime.datetime.today().year, 
    datetime.datetime.today().month, 
    datetime.datetime.today().day)

dates = ds.Cases[c.DATE].unique()
dates[-1] = today
dates = pd.to_datetime(dates, format='%Y-%m-%d')

for date in dates:
    print(ds.dailyCasesAverage(ds.Cases, date))
#TODO: expand the Cases, Tests, Hospitalisation datasets with values of previous period (date - 14 days)

print(ds.dailyHospitalAverage(ds.Hospital,today))
print(ds.getPositivityRate(ds.Tests, today))