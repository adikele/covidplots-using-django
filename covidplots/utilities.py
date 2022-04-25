import io
import random
import pandas as pd

DATA_FILE = "EUOpenData_06_12_2020"
DATA_DATE = "06/12/2020"
NEXT_UPDATE_DATE = "13/12/2020"
NUMBER_OF_DAYS = 240
global x, y


def list_all_countries():
    """
    Function returns a list of all countries
    """
    df = pd.read_csv(DATA_FILE)
    dict_all_countries = fetch_all_countries(df)
    list_all_countries = []
    for i in dict_all_countries.values():
        for j in i:
            list_all_countries.append(j)
    list_all_countries_sorted = sorted(list_all_countries)
    return list_all_countries_sorted


def read_input():
    print("At the prompt below, enter name of a country and press enter.")
    country = input("Enter country name: ")
    return country


# this function is not used
def input_validataion(name_country, dict_all_countries):
    """
    Function takes name_country, a string.
    It queries the population api to check if name_country exists in database
    Function returns true if name_country exists, false otherwise
    """
    for country_list in dict_all_countries.values():
        if name_country in country_list:
            return True
    return False


def fetch_all_countries(df):
    """
    Function finds the list of countries from all the continents
    It takes a dataframe of the input data file
    Returns a dict with keys --> continents
                      values --> list of countries in the respective continents
    """
    continents = ("Africa", "Europe", "America", "Oceania", "Asia")
    dict_all_countries = dict()
    for i in continents:
        df_current = df[(df["continentExp"] == i) & (df["dateRep"] == DATA_DATE)]
        dict_countries_current_continent = df_current.to_dict()
        list_countries_current_continent = list(
            dict_countries_current_continent["countriesAndTerritories"].values()
        )
        dict_all_countries[i] = list_countries_current_continent
    return dict_all_countries


def fetch_home_continent_data(df, country_sel):
    """
    Function finds the countries and cases for the home continent
    It takes (i) a dataframe of the input data file (ii) a string, country_sel
    Returns two lists: (i) a list of countries (ii) a list of cases
    """
    # determining the continent in which the selected country is situated
    dfc = df[
        (df["countriesAndTerritories"] == country_sel) & (df["dateRep"] == DATA_DATE)
    ]
    dict1 = dfc.to_dict()
    continent = list(dict1["continentExp"].values())
    continent = continent[0]

    # getting the list of countries from the same continent
    df2 = df[(df["continentExp"] == continent) & (df["dateRep"] == DATA_DATE)]
    dict2_countries_of_a_continent = df2.to_dict()
    list_countries = list(
        dict2_countries_of_a_continent["countriesAndTerritories"].values()
    )

    # extracting the number of Covid cases for the countries from the same continent
    list_cases = dict2_countries_of_a_continent[
        "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"
    ].values()

    return (list_countries, list_cases)


def random_countries(list_countries, country_sel):
    """
    Function selects 4 random countries, none of which are to be the user-selected country
    It takes (i) a list of countries
    (ii) a string, country_sel
    Returns a list of 4 random countries
    """
    list_countries_random = random.sample(list_countries, 4)
    if country_sel in list_countries_random:
        while True:
            list_countries_random = random.sample(list_countries, 4)
            if country_sel not in list_countries_random:
                break  # this way we always have 5 unique countries: 4 + 1
    return list_countries_random


def fetch_five_countries_data(dict_countries_cases, country_sel, list_countries_random):
    """
    Function creates a dict of countries and cases for 5 countries
    It takes (i) a dict of countries and cases (ii) a string, country_sel
    (iii) a list of 4 random countries
    Returns a dict of countries and cases for 5 countries
    """
    dict_fivecountries = dict()
    dict_fivecountries[country_sel] = dict_countries_cases[country_sel]

    for country in list_countries_random:
        dict_fivecountries[country] = dict_countries_cases[country]

    return dict_fivecountries


def creating_date_list(df, n):
    df1 = df[df["countriesAndTerritories"] == "Afghanistan"]
    dict1_one_country = df1.to_dict()
    date_list = list(dict1_one_country["dateRep"].values())
    newlistdate_list = date_list[:n]  # take the last "n" days
    newlistdate_list.reverse()  # reverse the list, now list ends with latest date
    return newlistdate_list


def fetch_all_continent_data(df):
    """
    Function finds the countries and cases for all continents
    It takes a dataframe of the input data file
    Returns two things:
    (i) a list of countries
    (ii) a dict with keys --> countries
                   values --> list of cases for each of the days recorded since Dec 2019
    """
    # extracting the countries from all continents:
    df3 = df[(df["dateRep"] == DATA_DATE)]
    dict3_countries_of_all_continent = df3.to_dict()
    countries_list = list(
        dict3_countries_of_all_continent["countriesAndTerritories"].values()
    )
    z = len(countries_list)  # getting the number of countries

    dict_countries_cases = dict()
    for i in range(z):
        df_current = df[df["countriesAndTerritories"] == countries_list[i]]
        dict_current = df_current.to_dict()
        dict_countries_cases[countries_list[i]] = list(
            dict_current[
                "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"
            ].values()
        )

    return countries_list, dict_countries_cases


def fetch_three_countries_data(
    dict_countries_cases, country_sel1, country_sel2, country_sel3, n
):
    """
    Function creates a dict of countries and cases for 3 countries
    It takes (i) a dict of countries and cases (ii) 3 strings, names of countries
    (iii) an integer, number of days for which data is desired.
    Returns a dict of countries and cases for 3 countries
    """
    # creating a dict of countries and cases for the 3 countries
    dict_threecountries = dict()
    dict_threecountries[country_sel1] = dict_countries_cases[country_sel1]
    dict_threecountries[country_sel2] = dict_countries_cases[country_sel2]
    dict_threecountries[country_sel3] = dict_countries_cases[country_sel3]

    # within the dict, "process" the list of case numbers
    for i in dict_threecountries.keys():
        abc_real_list = dict_threecountries[i]
        newabc_real_list = abc_real_list[:n]  # take the last "n" days
        newabc_real_list.reverse()  # reverse the list, now list ends with latest cases
        dict_threecountries[i] = newabc_real_list

    return dict_threecountries
