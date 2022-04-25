# covidplots-using-django
Web program displays bargraphs and linegraphs showing Covid-19 infection rates in different countries.
The project website can be found at: https://covid-19-vis2.lm.r.appspot.com/covidplots/

## Visualization of Covid-19 infections:
ORIGINAL PROJECT: This project was originally done in July - Dec 2020 using Flask. 
The purpose then was to develop software to visualize Covid-19 infection rates. 
Potential users were to be academicians, researchers and journalists. 
The project's Github page can be found here: https://github.com/adikele/covid-cases-webapp 
It is, however, not updated since December 2022.

CURRENT PROJECT: The original project is now redone using Django.
The goal of the current project is to compare the software development of a program in Flask and in Django.<br/>
The current project uses the following libraries: (i) Matplotlib 3.3.0 (ii) Pandas 1.1.0 (iii) Django 3.2.9

Users can plot two types of graphs. These are:<br/>
(i) Bargraphs of one user-entered country and four other countries from the same continent.<br/>
(ii) Linegraphs of infections in three user-entered countries over a period of time. 

![An example of a linegraph plot using the 'Spread of Infections in Countries' link](https://github.com/adikele/covidplots-using-django/blob/master/SweChiIndia.png)

### Structure:
The backend is a RESTful API application built with Django.
The data source is a csv file dated 6th December 2020 taken from the EU Open Data Portal: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data 
The csv file is converted into a dataframe in Pandas, from which the required data, based on user inputs, is extracted. 
This date is then ploted as graphs by using Matplotlib functions.


### Running this project:
On Linux and Mac: Download this project from Github and run it like any other Django Python project. Here are the steps to download and run the project:

Step 1 : Install Python 3.7+

Step 2 : In a terminal, first cd into the directory you would like to store this project. Then type the following commands one after:
```bash
mkdir covid-project && cd covid-project
python3 -m venv covid-venv
source covid-venv/bin/activate
git clone https://github.com/adikele/covidplots-using-django
cd covidplots-using-django
pip install -r requirements.txt
python manage.py runserver
```

### To Do: 
1. Create a dockerized container for the project
2. Create a frontend using React
3. Store results using a cloud service
