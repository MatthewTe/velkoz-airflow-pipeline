from django.shortcuts import render

# Importing database model from the dashboard_core app:
from dashboard_core.models import ExternalDatabase

# Importing Velkoz Stock Data API:
from velkoz_api.velkoz_query_api.velkoz_stock_data.stock_data_api import StockDataAPI

# Importing 3rd Party Packages:
import pandas as pd
import json

def stock_dashboard_index(request):
    """
    TODO: Add Documentation.
    """    
    # Creating empty context to be passed into the html template:
    context = {}
    
    # Querying the stock database model from the dashboard_core application:
    stock_db = ExternalDatabase.objects.get(db_name = "stock_data_db")
    stock_db_uri = stock_db.build_db_uri()

    # Creating instance of Velkoz Data API to query data:
    stock_data_api = StockDataAPI() # Database URI should be declared as environment variable.

    # Querying external database for summary data on stock database:
    stock_summary_df = stock_data_api.get_stock_database_summary()
    
    # Converting the dataframe into a json to be passed into the template:
    json_stock_summary_data = stock_summary_df.reset_index().to_json(orient="records")
    stock_summary_data = json.loads(json_stock_summary_data)

    # Populating context:
    context["stock_summary_table"] = stock_summary_data

    return render(request, 'stock_dashboard/stock_dashboard_index.html', context=context)
