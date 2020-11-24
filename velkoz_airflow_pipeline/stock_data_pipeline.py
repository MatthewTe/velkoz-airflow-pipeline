# Importing the velkoz data extraction library packages:
from velkoz_web_packages.objects_stock_data.stock_data_compiler import compile_ticker_list

# Importing the Velkoz Pipeline API:
from velkoz_api.velkoz_airflow_pipeline.stock_data_pipeline import VelkozStockPipeline

# Importing intenral packages:
import os
from sqlalchemy import create_engine

"""
Extracting CONFIG Parameters from the Environment:
"""
# Database URI:
database_uri = os.environ["VELKOZ_DB_URI"] 
#print("Extracted Database URL:", database_uri)

# Performing a test of the database connection to print to console (Uncomment):
"""
try:
    test_engine = create_engine(database_uri)
    test_conn = test_engine.connect()
    test_conn.close()
    test_engine.dispose()
    print("DATABASE CONNECTION:", True)

except:
    print("DATABASE CONNECTION", False)
""" 

# Extracting Absoloute Path to .csv file for stock price tickers:
price_csv_file_path = os.environ["TICKER_PRICE_CSV_PATH"] 

# Compiling csv into list of ticker strings via the stock data compiler:
price_ticker_lst = compile_ticker_list(price_csv_file_path)
stock_summary_ticker_lst = price_ticker_lst # TODO: Change to unique csv file in production.
#print("Extracted Ticker List:", price_ticker_lst)


"""
Calling Velkoz Airflow Pipeline API to create DAGs and Operators based on data extracted above: 
"""

"<---Stock Price Data--->"
# Creating Stock Pipeline Object:
stock_pipeline = VelkozStockPipeline(database_uri, "2020-11-23")


# Exposing Stock Price DAG and PythonOperartor to Global Execution Context:
stock_price_DAG_operator = stock_pipeline.schedule_stock_price_data_ingestion(
    price_ticker_lst) # DAG Object

stock_price_operator = stock_pipeline.stock_price_dag # PythonOperator Object

"<---Stock Database Summary Data--->"
# Exposing Stock Summary Data DAG:
stock_db_summary_DAG_operator = stock_pipeline.schedule_stock_summary_data_ingestion(
    stock_summary_ticker_lst) # DAG Object

stock_summary_data_operator = stock_pipeline.stock_sumary_dag # PythonOperator Object 
