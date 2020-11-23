# VERSION 0.0.1
# AUTHOR: Matthew Teelucksingh
# DESCRIPTION: The container for the Velkoz Airflow Pipeline
# BUILD:
# SOURCE:

FROM puckel/docker-airflow

# Installing git and necessary system applications:
USER root
RUN apt update && apt install -y git
USER airflow

# Configuring the python environment via the requirements.txt:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Setting all environment variables used to config the velkoz airflow pipeline:
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DAG_FOLDER=${AIRFLOW_USER_HOME}/dags

# ENV Variables should be configured manually for each velkoz database: 
ENV VELKOZ_DB_URI="postgresql://django:entropy_investments@docker.for.mac.host.internal:5432/stock_data_db"

# Ticker CSV path environment variables, again to be manually configured:
ENV TICKER_DATABASE_SUMMARY_CSV_PATH=""
ENV TICKER_PRICE_CSV_PATH=${AIRFLOW_USER_HOME}/ticker_price_list.csv
ENV TICKER_HOLDINGS_CSV_PATH=""

# Copying all of the pipeline api scripts to the Airflow Pipeline DAG folder:
COPY velkoz_airflow_pipeline/stock_data_pipeline.py ${AIRFLOW_DAG_FOLDER}

# Copying the folder containing ticker csv files into the working directory:
COPY ticker_csv .

