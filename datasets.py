import numpy as np
import pandas as pd
import datetime
import constants as c

#Data import from https://epistat.wiv-isp.be/covid/
#Confirmed cases by date, age, sex and province
Cases = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv')
Cases[c.DATE] = pd.to_datetime(Cases[c.DATE], format='%Y-%m-%d')
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


#definition of functions used to calculate values for the dashboard
def getNumberOfCases(cases, date):
    '''Input:
        cases - Cases dataset with a list of confirmed cases
        date - specific date at which number of cases has to be calculated
    Output:
        integer with a number of cases at a specific date
    '''
    cases_at_date = cases[cases[c.DATE].eq(date)]
    return cases_at_date[c.CASES].sum()

def incidentsRate(cases, referenceDate):
    '''Input:
        cases - Cases dataset with a list of confirmed cases
        referenceDate - date from which count the incidents rate
        The incidents rate is calculated for last 14 days with 4 last days excluded
    Output:
        incidents rate as a float
    '''
    four_days = datetime.timedelta(days=4)
    two_weeks = datetime.timedelta(days=13)
    
    end_date = referenceDate - four_days
    start_date = end_date - two_weeks

    sum_incidents = 0
    while start_date <= end_date:
        sum_incidents += 100000*getNumberOfCases(Cases, start_date)/c.POPULATION
        start_date += datetime.timedelta(days=1)

    return sum_incidents