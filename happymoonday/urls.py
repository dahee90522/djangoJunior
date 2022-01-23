from django.urls import path

from . import views

app_name = 'happymoonday'
urlpatterns = [
    path('', views.index, name='index'),
    path('data_add', views.dataAdd, name='data_add'),
    path('rate', views.rate, name='rate'),
    path('comparison', views.comparison, name='comparison'),
]