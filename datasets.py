import numpy as np
import pandas as pd
import datetime
import constants as c

# Import of the data needed for the dashboard from:
# https://epistat.wiv-isp.be/covid/
# Confirmed cases by date, age, sex and province
cases = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv')
cases[c.DATE] = pd.to_datetime(cases[c.DATE], format='%Y-%m-%d')

""" Cumulative number of confirmed cases by municipality
CUM_cases = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI_CUM.csv') """

""" Confirmed cases by date and municipality
MUN_cases = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv') """

# Hospitalisations by date and provinces
hospital = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv')
hospital[c.DATE] = pd.to_datetime(hospital[c.DATE], format='%Y-%m-%d')

""" Mortality by date, age, sex, and region
Mortal = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv') """

# Total number of tests by date
tests = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_tests.csv')
tests[c.DATE] = pd.to_datetime(tests[c.DATE], format='%Y-%m-%d')

# Administered vaccines by date, region, age, sex and dose
vaccines = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_VACC.csv')
vaccines[c.DATE] = pd.to_datetime(vaccines[c.DATE], format='%Y-%m-%d')

""" Administered vaccines by week, municipality, agegroup and dose
VAC_week = pd.read_csv('https://epistat.sciensano.be/data/COVID19BE_VACC_MUNI_CUM.csv') """


def get_period(reference_date, days_to_remove, period):
    """Input:
        reference_date - date from which to calculate last 14 days period
        days_to_remove - days to remove from the beginning of the period
        period - days until the end of the period (e.g. 7 days, 14 days)
    Output:
        start and end dates of the last 14 days period
    TODO: to update the function to work not only with the today date.
    Low priority
    """

    end_date = reference_date - datetime.timedelta(days=days_to_remove)
    start_date = end_date - datetime.timedelta(days=period - 1)

    return start_date, end_date


def get_number_of_cases(cases, date):
    """Input:
        cases - Cases dataset with a list of confirmed cases
        date - specific date at which number of cases has to be calculated
    Output:
        integer with a number of cases at a specific date
    """
    cases_at_date = cases[cases[c.DATE].eq(date)]
    return cases_at_date[c.CASES].sum()


def get_number_of_admissions(hospital, date):
    """Input:
        hospital - hospitalisation dataset with a list of admissions
        date - specific date at which number of cases has to be calculated
    Output:
        integer with a number of new admissions at a specific date
    """
    hospital_at_date = hospital[hospital[c.DATE].eq(date)]
    return hospital_at_date[c.NEW_IN].sum()


def get_incidents_rate(cases, reference_date, period):
    """Input:
        cases - Cases dataset with a list of confirmed cases
        reference_date - date from which count the incidents rate
        period - number of days for which calculate incidents rate
        The incidents rate is calculated for last 14 days
        with 4 last days excluded
    Output:
        incidents rate as a float
    """
    start_date, end_date = get_period(reference_date, 4, period)
    sum_incidents = 0
    while start_date <= end_date:
        sum_incidents += (
            100000 * get_number_of_cases(cases, start_date) / c.POPULATION
        )
        start_date += datetime.timedelta(days=1)

    return sum_incidents


def get_daily_cases_average(cases, reference_date, period):
    """Input:
        cases - Cases dataset with a list of confirmed cases
        reference_date - date from which count the incidents rate
        period - number of days for which calculate daily average
    Output:
        daily average as a float
    """
    start_date, end_date = get_period(reference_date, 4, period)
    cases_at_period = cases[
        cases[c.DATE].ge(start_date) & cases[c.DATE].le(end_date)
    ]
    sum_cases = cases_at_period[c.CASES].sum()
    return sum_cases / period


def get_daily_hospital_average(hospital, reference_date, period):
    """Input:
        hospital - hospitalisation dataset with a list of admissions
        reference_date - date from which count the incidents rate
        period - number of days for which calculate daily average
    Output:
        daily average as a float
    """
    start_date, end_date = get_period(reference_date, 1, period)
    hospital_at_date = hospital[
        hospital[c.DATE].ge(start_date) & hospital[c.DATE].le(end_date)
    ]
    sum_hospital = hospital_at_date[c.NEW_IN].sum()
    return sum_hospital / period


def get_number_of_tests(tests, date):
    """Input:
        tests- hospitalisation dataset with a number of tests done at a date
        date - specific date at which number of tests has to be calculated
    Output:
        number of tests at a specific date
    """
    tests_at_date = tests[tests[c.DATE].eq(date)]
    return tests_at_date[c.TESTS_ALL].sum()


def get_number_of_positive_tests(tests, date):
    """Input:
        tests- tests dataset with a number of tests done at a date
        date - specific date at which number of tests has to be calculated
    Output:
        number of tests at a specific date
    """
    tests_at_date = tests[tests[c.DATE].eq(date)]
    return tests_at_date[c.TESTS_ALL_POS].sum()


def get_positivity_rate(tests, reference_date, period):
    """Input:
        tests - tests dataset with a list of tests
        reference_date - date from which count the positivity rate
        period - number of days for which calculate positivity rate
    Output:
        daily average as a float
    """
    start_date, end_date = get_period(reference_date, 4, period)
    sum_tests = 0
    i = 0
    while start_date <= end_date:
        sum_tests += get_number_of_positive_tests(
            tests, start_date
        ) / get_number_of_tests(tests, start_date)
        start_date += datetime.timedelta(days=1)
        i += 1

    return sum_tests / i


def get_first_dose_count(vaccines, date):
    """Input:
        vaccines - dataset with a count of vaccinations per day
        date - date at which get count
    Output:
        overall count of first dose vaccinations
    """
    vaccines_first_dose = vaccines[
        vaccines[c.DOSE].ne(c.SECOND_DOSE) & vaccines[c.DATE].le(date)]
    return vaccines_first_dose[c.COUNT].sum()


def get_second_dose_count(vaccines, date):
    """Input:
        vaccines - vaccination dataset with a count of vaccinations per day
        date - date at which get count
    Output:
        overall count of second dose vaccinations
    """
    vaccines_second_dose = vaccines[
        vaccines[c.DOSE].ne(c.FIRST_DOSE) & vaccines[c.DATE].le(date)]
    return vaccines_second_dose[c.COUNT].sum()


def get_indicators_dataset(cases, hospital, tests, vaccines, date):
    """Input:
        cases - Cases dataset with a list of confirmed cases
        hospital - Hospital dataset with a list of hospitalisation
        tests - Tests dataset with a list of performed tests
        vaccines - Vaccination dataset with a count of vaccinations per day
    Output:
        a new dataset with incidents rate, cases, hospitalisation,
        positivity rates figures for 14 days period for a specified date
    """

    period = 14

    record = {}
    record[c.DATE] = date
    record[c.INC_RATE_T] = get_incidents_rate(cases, date, period)
    record[c.INC_RATE_T14] = get_incidents_rate(
        cases, date - datetime.timedelta(days=14), period
    )
    record[c.CASES_T] = get_daily_cases_average(cases, date, period)
    record[c.CASES_T14] = get_daily_cases_average(
        cases, date - datetime.timedelta(days=14), period
    )
    record[c.HOSP_T] = get_daily_hospital_average(hospital, date, period)
    record[c.HOSP_T14] = get_daily_hospital_average(
        hospital, date - datetime.timedelta(days=14), period
    )
    record[c.TESTS_T] = get_positivity_rate(tests, date, period)
    record[c.TESTS_T14] = get_positivity_rate(
        tests, date - datetime.timedelta(days=14), period
    )
    record[c.FD_VACCINE_T] = get_first_dose_count(vaccines, date)
    record[c.FD_VACCINE_T14] = get_first_dose_count(
        vaccines, date-datetime.timedelta(days=14))
    record[c.FD_PERCENTAGE_T] = record[c.FD_VACCINE_T] / c.POPULATION_18
    record[c.FD_PERCENTAGE_T14] = record[c.FD_VACCINE_T14] / c.POPULATION_18
    record[c.SD_VACCINE_T] = get_second_dose_count(vaccines, date)
    record[c.SD_VACCINE_T14] = get_second_dose_count(
        vaccines, date - datetime.timedelta(days=14))
    record[c.SD_PERCENTAGE_T] = record[c.SD_VACCINE_T] / c.POPULATION_18
    record[c.SD_PERCENTAGE_T14] = record[c.SD_VACCINE_T14] / c.POPULATION_18

    return record


def get_cases_graph_data(cases):
    """Input:
        cases - Cases dataset with a list of confirmed cases
    Output:
        dataframe with a number of cases per date
    """
    pivot = pd.pivot_table(
        data=cases, values=c.CASES, index=c.DATE, aggfunc=np.sum
    )
    pivot = pivot.reset_index()
    return pivot


def get_hospital_graph_data(hospital):
    """Input:
        hospital - Hospital dataset with a list of hospitalisations
    Output:
        dataframe with a number of hospitalisations per date
    """
    pivot = pd.pivot_table(
        data=hospital, values=c.NEW_IN, index=c.DATE, aggfunc=np.sum
    )
    pivot = pivot.reset_index()
    return pivot


def get_positivity_rate_graph_data(tests):
    """Input:
        tests- hospitalisation dataset with a number of tests done at a date
    Output:
        dataframe with a positivity rate per date
    """
    tests_pos_rate = tests.copy()
    tests_pos_rate[c.POSITIVITY_RATE] = (
        tests_pos_rate[c.TESTS_ALL_POS] / tests_pos_rate[c.TESTS_ALL]
    )
    pivot = pd.pivot_table(
        data=tests_pos_rate,
        values=c.POSITIVITY_RATE,
        index=c.DATE,
        aggfunc=np.mean,
    )
    pivot = pivot.reset_index()
    return pivot


def get_vaccination_graph_data(vaccines):
    """Input:
        vaccines - Vaccination dataset with a count of vaccinations per day
    Output:
        dataframe with two values - first andd second doses administred per day
    """
    # First dose and second dose filtering
    vaccines_fd = vaccines[vaccines[c.DOSE].ne(c.SECOND_DOSE)]
    vaccines_sd = vaccines[vaccines[c.DOSE].ne(c.FIRST_DOSE)]

    # generate pivots
    pivot_fd = pd.pivot_table(
        data=vaccines_fd, values=c.COUNT, index=c.DATE, aggfunc=np.sum
    )
    pivot_fd = pivot_fd.reset_index()
    pivot_fd[c.FD_VACCINE] = pivot_fd[c.COUNT].cumsum()

    pivot_sd = pd.pivot_table(
        data=vaccines_sd, values=c.COUNT, index=c.DATE, aggfunc=np.sum
    )
    pivot_sd = pivot_sd.reset_index()
    pivot_sd[c.SD_VACCINE] = pivot_sd[c.COUNT].cumsum()

    pivot = pivot_fd.merge(pivot_sd, on=c.DATE)

    return pivot
