#from SO working answer
import django
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
#import numpy as np


from django.shortcuts import render

#LastStage LS additions:
from .forms import CountriesSelectForm #LS1

from .forms import CountrySelectForm #samkey last

#from .utilities import * #LS2
from .utilities import * 

from django.shortcuts import redirect  #LS2
from django.shortcuts import get_object_or_404  #LS2


#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas #from covid_bardgraphs_demo
#from matplotlib.figure import Figure
import random
import pandas as pd

# Create your views here.

#@app.route("/")
def index(request):
    return render(request, "index.html")

'''
in flask:
def index():
    return render_template("index.html")
'''

    
'''
@app.route("/api_info")
def api_info(request):
    return render(request, "api_info.html")


def country_form(request):
    df = pd.read_csv(DATA_FILE)
    dict_all_countries = fetch_all_countries(df)
    list_all_countries = []
    for i in dict_all_countries.values():
        for j in i:
            list_all_countries.append(j)
    list_all_countries_sorted = sorted(list_all_countries)
    return render(request, "country_form.jinja2", options=list_all_countries_sorted)


def select_country_form(request):
    form = CountryForm()
    if request.method=='POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #now in the object cd, you have the form as a dictionary.
            a = cd.get('a')
            print (a)
    else:
        #this is the case when user sees the form for the first time
        form = CountryForm() 
    return render(request, 'catalog/select_country_form.html', {'form': form})

'''
def create_figure(countries, cases):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(countries, cases, color="blue")
    axis.set_ylabel("Persons infected in last 14 days (source: EU Open Data)")
    axis.set_title(
        f"Cumulative number (14 days) of COVID-19 cases per 100000 persons \n Data updated on: {DATA_DATE}  Next update: {NEXT_UPDATE_DATE}"
    )
    return fig


#real for Django, reopening on 21.4
def select_country_form(request):
    global x
    global y
    form = CountrySelectForm()
    if request.method=='POST':
        form = CountrySelectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #now in the object cd, you have the form as a dictionary.
            
            #b = cd.get('fav_f')
            country_sel = cd.get('selected_country')

            df = pd.read_csv(DATA_FILE)

            list_countries, list_cases = fetch_home_continent_data(df, country_sel)
            #list_countries, list_cases = fetch_home_continent_data(df, country_sel) originalFlask

            dict_continent = dict(zip(list_countries, list_cases))

            list_countries_random = random_countries(list_countries, country_sel) #originalFlask

            #dict_fivecountries = fetch_five_countries_data(
            #    dict_continent, country_sel, list_countries_random
            #)  originalFlask
            dict_fivecountries = fetch_five_countries_data(
                dict_continent, country_sel, list_countries_random
            )

            x = dict_fivecountries.keys()
            y = dict_fivecountries.values()

            fig = create_figure(x, y)

            #output = io.BytesIO()
            #FigureCanvas(fig).print_png(output)

            response=django.http.HttpResponse(content_type='image/png')  #bhaylo1
            FigureCanvas(fig).print_png(response)  #bhaylo2
            #return render_template("countries_result.jinja2", result=dict_fivecountries.keys())
            return response

    else:
        #this is the case when user sees the form for the first time
        form = CountrySelectForm() 
    return render(request, 'covidplots/country_form.html', {'form': form})

'''
#@app.route("/countries_result", methods=["POST"])
def countries_result(request):
    global x
    global y
    if request.method == "POST":
        country_sel = request.form["country_name"]

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

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
    return render_template("countries_result.jinja2", result=dict_fivecountries.keys())

#EXTRA also in ORIGINAL -- need to simply remove this one 
@app.route("/plot.png")
def plot():
    global x
    global y
    fig = create_figure(x, y)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")
'''

# NOTE: template and graph functions for linegraphs start from here..
# plotting countries and cases over time:
def create_figure_linegraphs(newlistdate_list, dict_three_countries):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    for i in dict_three_countries.keys():
        axis.plot(newlistdate_list, dict_three_countries[i], label=i)
    axis.set_xticks(
        ["15/04/2020", "15/05/2020", "15/06/2020", "15/07/2020", "15/08/2020", "15/09/2020", "15/10/2020", "15/11/2020"]
    )
    z = ["mid-April", "mid-May", "mid-June", "mid-July", "mid-Aug", "mid-Sept", "mid-Oct", "mid-Nov"]
    axis.set_xticklabels(z)
    axis.set_ylabel("Cumulative number of new virus infections per 100000 inhabitants")
    axis.set_xlabel("Year 2020 (last update: 6th Dec 2020)")  
    axis.set_title("Covid-19 infections - Country Graphs (source: EU Open Data)")
    axis.legend(loc="best")
    return fig

'''
@app.route("/linegraphs_form")
def linegraphs_form():
    df = pd.read_csv(DATA_FILE)
    dict_all_countries = fetch_all_countries(df)
    list_all_countries = []
    for i in dict_all_countries.values():
        for j in i:
            list_all_countries.append(j)
    list_all_countries_sorted = sorted(list_all_countries)
    return render_template("linegraphs_form.jinja2", options=list_all_countries_sorted)


@app.route("/plot_linegraphs.png", methods=["POST"])
def plot_linegraphs():
    global x
    global y
    
    country_sel1 = request.form["country_name1"]
    country_sel2 = request.form["country_name2"]
    country_sel3 = request.form["country_name3"]

    df = pd.read_csv(DATA_FILE)

    list_countries, dict_countries_cases = fetch_all_continent_data(df)

    dict_three_countries = fetch_three_countries_data(
        dict_countries_cases, country_sel1, country_sel2, country_sel3, NUMBER_OF_DAYS
    )

    newlistdate_list = creating_date_list(df, NUMBER_OF_DAYS)
    #here the fn creating_date_list is called!!!

    fig = create_figure_linegraphs(newlistdate_list, dict_three_countries)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")
'''
#working..
def select_countries_form(request):
    form = CountriesSelectForm()
    
    if request.method=='POST':
        form = CountriesSelectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #now in the object cd, you have the form as a dictionary.
            
            #b = cd.get('fav_f')
            country_sel1 = cd.get('selected_country1')
            country_sel2 = cd.get('selected_country2')
            country_sel3 = cd.get('selected_country3')

            print (country_sel2)

            df = pd.read_csv(DATA_FILE)

            #list_countries, dict_countries_cases = utilities.fetch_all_continent_data(df)
            list_countries, dict_countries_cases = fetch_all_continent_data(df)

            dict_three_countries = fetch_three_countries_data(
            dict_countries_cases, country_sel1, country_sel2, country_sel3, NUMBER_OF_DAYS
            )

            newlistdate_list = creating_date_list(df, NUMBER_OF_DAYS)
            #here the fn creating_date_list is called!!!

            fig = create_figure_linegraphs(newlistdate_list, dict_three_countries)
            #output = io.BytesIO()
            response=django.http.HttpResponse(content_type='image/png')  #bhaylo
            #FigureCanvas(fig).print_png(output)
            FigureCanvas(fig).print_png(response)
            #return Response(output.getvalue(), mimetype="image/png")  #original
            #return render(request, output.getvalue(), mimetype="image/png") #doesn't work
            return response

    else:
        #this is the case when user sees the form for the first time
        form = CountriesSelectForm() 
        return render(request, 'covidplots/countries_form.html', {'form': form})
    

'''
    def ref_graph2(request): #this works
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        x = np.arange(-2,1.5,.01)
        y = np.sin(np.exp(2*x))
        ax.plot(x, y)
        response=django.http.HttpResponse(content_type='image/png')  #using this
        canvas.print_png(response)
        return response
'''