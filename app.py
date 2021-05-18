import datasets as ds
import constants as c
import pandas as pd
import datetime

#Import of the data needed for the dashboard from https://epistat.wiv-isp.be/covid/
#Confirmed cases by date, age, sex and province
Cases = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv')
Cases[c.DATE] = pd.to_datetime(Cases[c.DATE], format='%Y-%m-%d')

#Cumulative number of confirmed cases by municipality
CUM_cases = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI_CUM.csv')

#Confirmed cases by date and municipality
#MUN_cases = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv')

#Hospitalisations by date and provinces
Hospital = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv')
Hospital[c.DATE] = pd.to_datetime(Hospital[c.DATE], format='%Y-%m-%d')

#Mortality by date, age, sex, and region
#Mortal = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv')

#Total number of tests by date
Tests = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_tests.csv')
Tests[c.DATE] = pd.to_datetime(Tests[c.DATE], format='%Y-%m-%d')

#Administered vaccines by date, region, age, sex and dose
Vaccines = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_VACC.csv')
Vaccines[c.DATE] = pd.to_datetime(Vaccines[c.DATE], format='%Y-%m-%d')

#Administered vaccines by week, municipality, agegroup and dose
#VAC_week = pd.read_csv('https://epistat.sciensano.be/data/COVID19BE_VACC_MUNI_CUM.csv')

today = datetime.datetime(datetime.datetime.today().year, 
    datetime.datetime.today().month, 
    datetime.datetime.today().day)

#print(ds.dailyCasesAverage(Cases,today, 14))
#print(ds.dailyHospitalAverage(Hospital,today, 14))
#print(ds.getPositivityRate(ds.Tests, today, 13))
print(ds.getIndicatorsDataSet(Cases, Hospital, Tests, Vaccines, today))
#print(ds.getFirstDoseCount(Vaccines))
#print(ds.getSecondDoseCount(Vaccines))