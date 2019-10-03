from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='main-home'),
	path('team_details/', views.team_details, name='main-team-details'),
	path('results/', views.results, name='main-results'),
]