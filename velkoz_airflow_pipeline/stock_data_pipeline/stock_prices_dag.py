# Importing airflow packages:
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Importing the velkoz data extraction library packages:
from velkoz_web_packages.objects_stock_data.stock_data_compiler import compile_ticker_list
from velkoz_web_packages.objects_stock_data.objects_stock_price.web_objects_stock_price import NASDAQStockPriceResponseObject
from velkoz_web_packages.objects_stock_data.objects_stock_price.ingestion_engines_stock_price import StockPriceDataIngestionEngine

# Importing 3rd party packages:
from datetime import datetime
from datetime import timedelta
import time
import os

# <---------------------Initalizing DAG Relevant Data-------------------------->

# Initalizing the Stock Price Ingestion Engine:
database_url = 'postgres://airflow_account:Entropy_Investments@localhost:5432/stock_data_db'
# Extracting list of ticker symbols from the ticker_price_list static .csv file:
ticker_lst = compile_ticker_list("/home/matthew/Projects/python/velkoz_airflow_pipeline/velkoz_airflow_pipeline/stock_data_static_files/ticker_price_list.csv")


# <--------------------------DAG Construction Methods-------------------------->
def ingest_stock_price_data_from_ticker_lst(ticker_lst, db_uri):
    """
    The method wraps all the logic used to extract price data from a list of ticker
    symbols and write this price data to a database.

    The method creates a self-contained instance of an ingestion engine based on
    the input database URI. It iterates over the input list of ticker symbols and
    creates a list of initialized NASDAQStockPriceResponseObjects. These price
    objects are then passed into the ingestion engine. Once all the PriceResponseObjects
    are successfully added to the Ingestion Engine the method writes all data to the
    connected database.

    Creates list of price objects --> Ingest All Price Objects --> Write Price Objects to Database.

    Args:
        ticker_lst (list): A list of ticker symbol strings that the method converts
            to NASDAQStockPriceResponseObjects.

        db_uri (str): The database URL string that is used initalize an Ingestion
            Engine. It is the database that the price data is written to.
    """
    # Declaring an instance of a Stock Price Ingestion Engine:
    stock_price_ingestion_engine = StockPriceDataIngestionEngine(db_uri)

    # Creating an empty list to be populated with NASDAQStockPriceResponseObjects:
    price_objs_lst = []

    # Iterating over the ticker list, creating a list of NASDAQStockPriceResponseObjects:
    for ticker in ticker_lst:

        # Adding the price object to the list:
        price_objs_lst.append(NASDAQStockPriceResponseObject(ticker))

        # Sleeping to prevent timeout from Yahoo Servers:
        time.sleep(20)

    # Adding each StockPriceObject to the Ingestion Engine:
    for object in price_objs_lst:
        stock_price_ingestion_engine._insert_web_obj(object)

    # Writing all data contained in the ingestion engine to the database:
    stock_price_ingestion_engine._write_web_objects()

# <----------------------Constructing Pipeline DAGs---------------------------->

# Defining the default arguments for the stock price DAG:
stock_price_dag_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'start_date' : datetime(2020, 10, 20),
    'email_on_failure' : False,
    'email_on_retry' : False,
    'retries' : 2,
    'retry_delay' : timedelta(seconds=20)
}

# Defining the Stock Price DAG Object:
stock_price_dag = DAG(
    dag_id = 'stock_price_data_dag',
    description = "The DAG schedules processes that are used to update and maintain the velkoz database tables containing stock price time-series data.",
    schedule_interval = '@daily',
    default_args = stock_price_dag_args)

# Creating operator that writes all data to the attached database:
write_stock_price_data = PythonOperator(
    task_id = "write_price_data_to_db",
    python_callable = ingest_stock_price_data_from_ticker_lst,
    op_kwargs = {'ticker_lst':ticker_lst, 'db_uri':database_url},
    dag = stock_price_dag)
