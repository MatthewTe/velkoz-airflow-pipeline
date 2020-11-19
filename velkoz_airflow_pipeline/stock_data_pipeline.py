# Importing the velkoz data extraction library packages:
from velkoz_web_packages.objects_stock_data.stock_data_compiler import compile_ticker_list
from velkoz_web_packages.objects_stock_data.objects_stock_price.web_objects_stock_price import NASDAQStockPriceResponseObject
from velkoz_web_packages.objects_stock_data.objects_stock_price.ingestion_engines_stock_price import StockPriceDataIngestionEngine

# Importing the Velkoz Pipeline API:
from velkoz_api.velkoz_airflow_pipeline.stock_data_pipeline import VelkozStockPipeline

# Importing intenral packages:
import os

"""
Extracting CONFIG Parameters from the Environment:
"""
# Database URI:
database_uri = os.environ["VELKOZ_DB_URI"] 

# Extracting Absoloute Path to .csv file for stock price tickers:
price_csv_file_path = os.environ["TICKER_PRICE_CSV_PATH"] 

# Compiling csv into list of ticker strings via the stock data compiler:
price_ticker_lst = compile_ticker_list(price_csv_file_path)

"""
Calling Velkoz Airflow Pipeline API to create DAGs and Operators based on data extracted above: 
"""


"<---Stock Price Data--->"

# Creating Stock Pipeline Object:
stock_pipeline = VelkozStockPipeline(database_uri, "2020-11-18")


# Exposing Stock Price DAG and PythonOperartor to Global Execution Context:
stock_price_DAG = stock_pipeline.stock_price_dag
stock_price_DAG_operator = stock_pipeline.schedule_stock_price_data_ingestion(
    price_csv_file_path)
