from django.urls import path
from . import views

urlpatterns = [

    # Main Home page:
    path('', views.main_index, name='main_index_page')

]
