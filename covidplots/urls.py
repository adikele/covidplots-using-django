from django.urls import path
from . import views

urlpatterns = [   
path('', views.index, name='index'),
path('bargraphs/', views.select_country_form, name='country_form'),  #for bargraphs
path('linegraphs/', views.select_countries_form, name='countries_form'),  #go to path linegraphs


]
