from django.shortcuts import render

# Importing database model from the dashboard_core app:
from dashboard_core.models import ExternalDatabase

# Importing Velkoz Stock Data API:
from velkoz_api.velkoz_query_api.velkoz_stock_data.stock_data_api import StockDataAPI

# Importing 3rd Party Packages:
from datetime import datetime
import pandas as pd
import json

def stock_dashboard_index(request):
    """The method renders the template “stock_dashboard_index.html” with
     a context populated with metadata queried from an external database.

    The main purpose of this method is to perform data queries to an external 
    database containing stock data that is used to populate the django template. 
    The template rendered is meant to serve as a summary dashboard about stock data 
    contained with the external velkoz database. The queries that are made to the 
    external database are made via the velkoz_stock_data API. The queries that are 
    currently made are:

    - StockDataAPI.get_stock_database_summary() --> Summary Data on stocks contained within the database.
    
    Args:
        request (http request): The http request that is sent to the server from
            the client.
    Returns:
        django.shortcuts.render: The django template rendered as html with full
            context.

   """    
    # Creating empty context to be passed into the html template:
    context = {}
    
    # Querying the stock database model from the dashboard_core application:
    stock_db = ExternalDatabase.objects.get(db_name = "stock_data_db")
    stock_db_uri = stock_db.build_db_uri()

    # TODO: Automatically set the database uri as an environment variable:

    # Creating instance of Velkoz Data API to query data:
    stock_data_api = StockDataAPI() # Database URI should be declared as environment variable.

    # Querying external database for summary data on stock database:
    stock_summary_df = stock_data_api.get_stock_database_summary() # Returns dataframe.

    # Slicing the dataframe based on the seach parameter from front-end GET:
    if "search" not in request.GET:
        pass

    else:

        # If the search string is blank do not perform slice:
        if request.GET['search'] == '':
            pass

        else:
            # Slicing dataframe based on input string:
            stock_summary_df = stock_summary_df[stock_summary_df.index.isin([
                request.GET['search'].upper()])]
        
    # Converting the dataframe into a json to be passed into the template:
    json_stock_summary_data = stock_summary_df.reset_index().to_json(orient="records")
    stock_summary_data = json.loads(json_stock_summary_data)

    # Populating context:
    context["stock_summary_table"] = stock_summary_data

    return render(request, 'stock_dashboard/stock_dashboard_index.html',
        context=context)


def stock_dashboard_individual(request, ticker):
    """
    TODO: Add Documentation
    """
    # Creating empty context to be populated:
    context = {}
    context['ticker'] = ticker

    # Declaring the stock data API:
    stock_api = StockDataAPI()

    # Using the API to query the price timeseries of ticker param:
    ticker_price_df = stock_api.get_price_history(ticker)

    # Extracting the index and the closing price from the dataframe:
    context['price_history_index'] = [str(date) for date in ticker_price_df.index]
    context['price_history_close'] = list(ticker_price_df['close'])

    return render(request, 'stock_dashboard/stock_dashboard_individual.html',
        context=context)

















