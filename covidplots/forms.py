from django import forms
from .utilities import list_all_countries


LIST_COUNTRIES_raw = list_all_countries()

LIST_COUNTRIES_processed = []


for i in LIST_COUNTRIES_raw:
    LIST_COUNTRIES_processed.append((i,i))


#LIST_COUNTRIES = [('India', 'Indiaa'),
#    ('Pakistan', 'Pakistann'), ('Nepal', 'Nepal'), ('Bhutan', 'Bhutan'), ('China', 'China'),]
#extended list to have five countries
#from examples I noticed that there is a comma at the end, can't say why
#ok, looks like the comma is not required

LIST_COUNTRIES_comremov = [('India', 'Indiaa'),
    ('Pakistan', 'Pakistann'), ('Nepal', 'Nepal'), ('Bhutan', 'Bhutan'), ('China', 'China')]



class CountrySelectForm(forms.Form):
    selected_country = forms.CharField(label='Select country:', widget=forms.Select(choices=LIST_COUNTRIES_processed )) 


class CountriesSelectForm(forms.Form):
    selected_country1 = forms.CharField(label='Select country 1:', widget=forms.Select(choices=LIST_COUNTRIES_processed )) 
    selected_country2 = forms.CharField(label='Select country 2:', widget=forms.Select(choices=LIST_COUNTRIES_processed ))
    selected_country3 = forms.CharField(label='Select country 3:', widget=forms.Select(choices=LIST_COUNTRIES_processed ))

