import numpy as np
import pandas as pd
import datetime
import constants as c

#definition of functions used to calculate values for the dashboard
def getPeriod(referenceDate, daysToRemove, period):
    '''Input:
        referenceDate - date from which to calculate last 14 days period
        daysToRemove - days to remove from the beginning of the period
        period - days until the end of the period (e.g. 7 days, 14 days)
    Output:
        start and end dates of the last 14 days period
    TODO: to update the function to work not only with the today date. Low priority
    '''
    
    end_date = referenceDate - datetime.timedelta(days=daysToRemove)
    start_date = end_date - datetime.timedelta(days=period-1)

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

def getIncidentsRate(cases, referenceDate, period):
    '''Input:
        cases - Cases dataset with a list of confirmed cases
        referenceDate - date from which count the incidents rate
        period - number of days for which calculate incidents rate
        The incidents rate is calculated for last 14 days with 4 last days excluded

    Output:
        incidents rate as a float
    '''
    start_date, end_date = getPeriod(referenceDate, 4, period)
    sum_incidents = 0
    while start_date <= end_date:
        sum_incidents += 100000*getNumberOfCases(cases, start_date)/c.POPULATION
        start_date += datetime.timedelta(days=1)

    return sum_incidents

def dailyCasesAverage(cases, referenceDate, period):
    '''Input:
        cases - Cases dataset with a list of confirmed cases
        referenceDate - date from which count the incidents rate
        period - number of days for which calculate daily average
    Output:
        daily average as a float
    '''
    start_date, end_date = getPeriod(referenceDate, 4, period)
    cases_at_period = cases[cases[c.DATE].ge(start_date) & cases[c.DATE].le(end_date)]
    sum_cases = cases_at_period[c.CASES].sum()
    return sum_cases / period

def dailyHospitalAverage(hospital, referenceDate, period):
    '''Input:
        hospital - hospitalisation dataset with a list of admissions
        referenceDate - date from which count the incidents rate
        period - number of days for which calculate daily average
    Output:
        daily average as a float
    '''
    start_date, end_date = getPeriod(referenceDate, 1, period)
    hospital_at_date = hospital[hospital[c.DATE].ge(start_date) & hospital[c.DATE].le(end_date)]
    sum_hospital = hospital_at_date[c.NEW_IN].sum()
    return sum_hospital / period

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

def getPositivityRate(tests, referenceDate, period):
    '''Input:
        tests - tests dataset with a list of tests
        referenceDate - date from which count the positivity rate
        period - number of days for which calculate positivity rate
    Output:
        daily average as a float
    '''
    start_date, end_date = getPeriod(referenceDate, 4, period)
    sum_tests = 0
    i = 0
    while start_date <= end_date:
        sum_tests += getNumberOfPositiveTests(tests, start_date) / getNumberOfTests(tests, start_date)
        start_date += datetime.timedelta(days=1)
        i += 1

    return sum_tests / i

def getFirstDoseCount(vaccines):
    '''Input:
        vaccines - vaccination dataset with a count of vaccinations per day
    Output:
        overall count of first dose vaccinations
    '''
    vaccines_first_dose = vaccines[vaccines[c.DOSE].ne(c.SECOND_DOSE)]
    return vaccines_first_dose[c.COUNT].sum()

def getSecondDoseCount(vaccines):
    '''Input:
        vaccines - vaccination dataset with a count of vaccinations per day
    Output:
        overall count of second dose vaccinations
    '''
    vaccines_second_dose = vaccines[vaccines[c.DOSE].ne(c.FIRST_DOSE)]
    return vaccines_second_dose[c.COUNT].sum()


#TODO: to expand with other datasets (tests, hospitalisations, etc.)
def getIndicatorsDataSet(cases, hospital, tests, vaccines, date):
    '''Input:
        cases - Cases dataset with a list of confirmed cases
        hospital - Hospital dataset with a list of hospitalisation
        tests - Tests dataset with a list of performed tests
        vaccines - Vaccination dataset with a count of vaccinations per day
    Output:
        a new dataset with incidents rate, cases, hospitalisation, positivity rates figures for 14 days period for a specified date
    '''
    
    period = 13
    
    record = {}
    record[c.DATE] = date
    record[c.INC_RATE_T] = getIncidentsRate(cases, date, period)
    record[c.INC_RATE_T14] = getIncidentsRate(cases, date - datetime.timedelta(days=14), period)
    record[c.CASES_T] = dailyCasesAverage(cases, date, period)
    record[c.CASES_T14] = dailyCasesAverage(cases, date - datetime.timedelta(days=14), period)
    record[c.HOSP_T] = dailyHospitalAverage(hospital, date, period)
    record[c.HOSP_T14] = dailyHospitalAverage(hospital, date - datetime.timedelta(days=14), period)
    record[c.TESTS_T] = getPositivityRate(tests, date, period)
    record[c.TESTS_T14] = getPositivityRate(tests, date - datetime.timedelta(days=14), period)
    record[c.FD_VACCINE] = getFirstDoseCount(vaccines)
    record[c.FD_PERCENTAGE] = record[c.FD_VACCINE] / c.POPULATION_18
    record[c.SD_VACCINE] = getSecondDoseCount(vaccines)
    record[c.SD_PERCENTAGE] = record[c.SD_VACCINE] / c.POPULATION_18
    
    return pd.DataFrame(data=record, index=[0])

def getCasesGraphData(cases):
    '''Input:
        cases - Cases dataset with a list of confirmed cases
    Output:
        dataframe with a number of cases per date
    '''
    pivot = pd.pivot_table(data=cases, values=c.CASES, index=c.DATE, aggfunc=np.sum)
    pivot = pivot.reset_index()
    return pivot

def getHospitalGraphData(hospital):
    '''Input:
        hospital - Hospital dataset with a list of hospitalisations
    Output:
        dataframe with a number of hospitalisations per date
    '''
    pivot = pd.pivot_table(data=hospital, values=c.NEW_IN, index=c.DATE, aggfunc=np.sum)
    pivot = pivot.reset_index()
    return pivot

def getPositivityRateGraphData(tests):
    '''Input:
        tests- hospitalisation dataset with a number of tests done at a certain date
    Output:
        dataframe with a positivity rate per date
    '''
    tests_pos_rate = tests.copy()
    tests_pos_rate[c.POSITIVITY_RATE] = tests_pos_rate[c.TESTS_ALL_POS] / tests_pos_rate[c.TESTS_ALL]
    pivot = pd.pivot_table(data=tests_pos_rate, values=c.POSITIVITY_RATE, index=c.DATE, aggfunc=np.mean)
    pivot = pivot.reset_index()
    return pivot

def getVaccinationGraohData(vaccines):
    '''Input:
        vaccines - Vaccination dataset with a count of vaccinations per day
    Output:
        dataframe with two values - first dose and second dose administred per day
    '''
    #First dose and second dose filtering
    vaccines_fd = vaccines[vaccines[c.DOSE].ne(c.SECOND_DOSE)]
    vaccines_sd = vaccines[vaccines[c.DOSE].ne(c.FIRST_DOSE)]

    #generate pivots
    pivot_fd = pd.pivot_table(data=vaccines_fd, values=c.COUNT, index=c.DATE, aggfunc=np.sum)
    pivot_fd = pivot_fd.reset_index()
    pivot_fd[c.FD_VACCINE] = pivot_fd[c.COUNT].cumsum()
    
    pivot_sd = pd.pivot_table(data=vaccines_sd, values=c.COUNT, index=c.DATE, aggfunc=np.sum)
    pivot_sd = pivot_sd.reset_index()
    pivot_sd[c.SD_VACCINE] = pivot_sd[c.COUNT].cumsum()
    
    pivot = pivot_fd.merge(pivot_sd, on=c.DATE)
    
    return pivot
