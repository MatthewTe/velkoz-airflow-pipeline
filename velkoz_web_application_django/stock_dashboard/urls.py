from django.urls import path
from . import views

urlpatterns = [

    # Stock Data Dashboard Main Index Page:
    path('', views.stock_dashboard_index, name='stock_data_db'),

    # Individual Stock Dashboard:
    path('ticker_dashboard/<str:ticker>/', views.stock_dashboard_individual, 
    	name='stock_dashboard_individual')
    
    ]
