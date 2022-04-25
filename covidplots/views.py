import pandas as pd
import django
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CountriesSelectForm
from .forms import CountrySelectForm
from .utilities import *
import random


def index(request):
    return render(request, "index.html")


def api_info(request):
    return render(request, "covidplots/api_info.html")


def valstreetdesign(request):
    return render(request, "covidplots/valstreetdesign.html")


# NOTE: template and graph functions for bargraphs start from here..
def create_figure(countries, cases):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(countries, cases, color="blue")
    axis.set_ylabel("Persons infected in last 14 days (source: EU Open Data)")
    axis.set_title(
        f"Cumulative number (14 days) of COVID-19 cases per 100000 persons \n Data updated on: {DATA_DATE}  Next update: {NEXT_UPDATE_DATE}"
    )
    return fig


def select_country_form(request):
    global x
    global y
    form = CountrySelectForm()
    if request.method == "POST":
        form = CountrySelectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            country_sel = cd.get("selected_country")
            df = pd.read_csv(DATA_FILE)

            list_countries, list_cases = fetch_home_continent_data(df, country_sel)
            dict_continent = dict(zip(list_countries, list_cases))
            list_countries_random = random_countries(list_countries, country_sel)
            dict_fivecountries = fetch_five_countries_data(
                dict_continent, country_sel, list_countries_random
            )

            x = dict_fivecountries.keys()
            y = dict_fivecountries.values()

            fig = create_figure(x, y)

            response = django.http.HttpResponse(content_type="image/png")
            FigureCanvas(fig).print_png(response)
            return response

    else:
        # this is the case when user sees the form for the first time
        form = CountrySelectForm()
    return render(request, "covidplots/country_form.html", {"form": form})


# NOTE: template and graph functions for linegraphs start from here..
# plotting countries and cases over time:
def create_figure_linegraphs(newlistdate_list, dict_three_countries):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    for i in dict_three_countries.keys():
        axis.plot(newlistdate_list, dict_three_countries[i], label=i)
    axis.set_xticks(
        [
            "15/04/2020",
            "15/05/2020",
            "15/06/2020",
            "15/07/2020",
            "15/08/2020",
            "15/09/2020",
            "15/10/2020",
            "15/11/2020",
        ]
    )
    z = [
        "mid-April",
        "mid-May",
        "mid-June",
        "mid-July",
        "mid-Aug",
        "mid-Sept",
        "mid-Oct",
        "mid-Nov",
    ]
    axis.set_xticklabels(z)
    axis.set_ylabel("Cumulative number of new virus infections per 100000 inhabitants")
    axis.set_xlabel("Year 2020 (last update: 6th Dec 2020)")
    axis.set_title("Covid-19 infections - Country Graphs (source: EU Open Data)")
    axis.legend(loc="best")
    return fig


def select_countries_form(request):
    form = CountriesSelectForm()

    if request.method == "POST":
        form = CountriesSelectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            country_sel1 = cd.get("selected_country1")
            country_sel2 = cd.get("selected_country2")
            country_sel3 = cd.get("selected_country3")

            print(country_sel2)

            df = pd.read_csv(DATA_FILE)
            list_countries, dict_countries_cases = fetch_all_continent_data(df)

            dict_three_countries = fetch_three_countries_data(
                dict_countries_cases,
                country_sel1,
                country_sel2,
                country_sel3,
                NUMBER_OF_DAYS,
            )

            newlistdate_list = creating_date_list(df, NUMBER_OF_DAYS)

            fig = create_figure_linegraphs(newlistdate_list, dict_three_countries)

            response = django.http.HttpResponse(content_type="image/png")
            FigureCanvas(fig).print_png(response)
            return response

    else:
        # this is the case when user sees the form for the first time
        form = CountriesSelectForm()
        return render(request, "covidplots/countries_form.html", {"form": form})
