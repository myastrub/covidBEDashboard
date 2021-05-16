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
Hospital[c.DATE] = pd.to_datetime(Hospital[c.DATE], format='%Y-%m-%d')

#Mortality by date, age, sex, and region
Mortal = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv')

#Total number of tests by date
Tests = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_tests.csv')
Tests[c.DATE] = pd.to_datetime(Tests[c.DATE], format='%Y-%m-%d')

#Administered vaccines by date, region, age, sex and dose
Vaccines = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_VACC.csv')
Vaccines[c.DATE] = pd.to_datetime(Vaccines[c.DATE], format='%Y-%m-%d')

#Administered vaccines by week, municipality, agegroup and dose
VAC_week = pd.read_csv('https://epistat.sciensano.be/data/COVID19BE_VACC_MUNI_CUM.csv')


#definition of functions used to calculate values for the dashboard
def getPeriod(referenceDate, days):
    '''Input:
        referenceDate - date from which to calculate last 14 days period
        days - days to remove from the beginning of the period
    Output:
        start and end dates of the last 14 days period
    TODO: to update the function to work not only with the today date. Low priority
    '''
    
    end_date = referenceDate - datetime.timedelta(days=days)
    start_date = end_date - datetime.timedelta(days=13)

    return start_date, end_date

def getNumberOfCases(cases, date):
    '''Input:
        cases - Cases dataset with a list of confirmed cases
        date - specific date at which number of cases has to be calculated
    Output:
        integer with a number of cases at a specific date
    '''
    cases_at_date = cases[cases[c.DATE].eq(date)]
    return cases_at_date[c.CASES].sum()

def getNumberOfAdmissions(hospital, date):
    '''Input:
        hospital - hospitalisation dataset with a list of admissions
        date - specific date at which number of cases has to be calculated
    Output:
        integer with a number of new admissions at a specific date
    '''
    hospital_at_date = hospital[hospital[c.DATE].eq(date)]
    return hospital_at_date[c.NEW_IN].sum()

def incidentsRate(cases, referenceDate):
    '''Input:
        cases - Cases dataset with a list of confirmed cases
        referenceDate - date from which count the incidents rate
        The incidents rate is calculated for last 14 days with 4 last days excluded
    Output:
        incidents rate as a float
    '''
    start_date, end_date = getPeriod(referenceDate, 4)
    sum_incidents = 0
    while start_date <= end_date:
        sum_incidents += 100000*getNumberOfCases(Cases, start_date)/c.POPULATION
        start_date += datetime.timedelta(days=1)

    return sum_incidents

def dailyCasesAverage(cases, referenceDate):
    '''Input:
        cases - Cases dataset with a list of confirmed cases
        referenceDate - date from which count the incidents rate
        The daily average is calculated for last 14 days with 4 last days excluded
    Output:
        daily average as a float
    '''
    start_date, end_date = getPeriod(referenceDate, 4)
    sum_cases = 0
    i = 0
    while start_date <= end_date:
        sum_cases += getNumberOfCases(cases, start_date)
        start_date += datetime.timedelta(days=1)
        i += 1

    return sum_cases / i

def dailyHospitalAverage(hospital, referenceDate):
    '''Input:
        hospital - hospitalisation dataset with a list of admissions
        referenceDate - date from which count the incidents rate
        The daily average is calculated for last 14 days with 4 last days excluded
    Output:
        daily average as a float
    '''
    start_date, end_date = getPeriod(referenceDate, 1)
    sum_hospital = 0
    i = 0
    while start_date <= end_date:
        sum_hospital += getNumberOfAdmissions(hospital, start_date)
        start_date += datetime.timedelta(days=1)
        i += 1

    return sum_hospital / i

def getNumberOfTests(tests, date):
    '''Input:
        tests- hospitalisation dataset with a number of tests done at a certain date
        date - specific date at which number of tests has to be calculated
    Output:
        number of tests at a specific date
    '''
    tests_at_date = tests[tests[c.DATE].eq(date)]
    return tests_at_date[c.TESTS_ALL].sum()

def getNumberOfPositiveTests(tests, date):
    '''Input:
        tests- tests dataset with a number of tests done at a certain date
        date - specific date at which number of tests has to be calculated
    Output:
        number of tests at a specific date
    '''
    tests_at_date = tests[tests[c.DATE].eq(date)]
    return tests_at_date[c.TESTS_ALL_POS].sum()

def getPositivityRate(tests, referenceDate):
    '''Input:
        tests - tests dataset with a list of tests
        referenceDate - date from which count the positivity rate
        The daily average is calculated for last 14 days with 4 last days excluded
    Output:
        daily average as a float
    '''
    start_date, end_date = getPeriod(referenceDate, 4)
    sum_tests = 0
    i = 0
    while start_date <= end_date:
        sum_tests += getNumberOfPositiveTests(tests, start_date) / getNumberOfTests(tests, start_date)
        start_date += datetime.timedelta(days=1)
        i += 1

    return sum_tests / i
