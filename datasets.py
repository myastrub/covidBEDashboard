import numpy as np
import pandas as pd

#Data import from https://epistat.wiv-isp.be/covid/
#Confirmed cases by date, age, sex and province
Cases = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv')

#Cumulative number of confirmed cases by municipality
CUM_cases = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI_CUM.csv')

#Confirmed cases by date and municipality
MUN_cases = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv')

#Hospitalisations by date and provinces
Hospital = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv')

#Mortality by date, age, sex, and region
Mortal = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv')

#Total number of tests by date
Tests = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_tests.csv')

#Administered vaccines by date, region, age, sex and dose
Vaccines = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_VACC.csv')

#Administered vaccines by week, municipality, agegroup and dose
VAC_week = pd.read_csv('https://epistat.sciensano.be/data/COVID19BE_VACC_MUNI_CUM.csv')


