import os
import json
import datetime
import pandas as pd
import logging
import azure.functions as func
from ..shared import storage_helpers


# Gets the total amount by field
def get_amounts(df, field):
    df_total = df.groupby(by=field).sum()
    amounts = {}
    for i, row in df_total.iterrows():
        if i != 'N/A' and i != '':
            amount = row[0]
            print(f"{field}: {i} - amount: {amount}")
            amounts[i] = str(amount)
    return amounts


# Gets the number of occurences by field
def get_counts(df, field):
    df_count = df[field].value_counts()
    counts = {}
    for i in df_count.index:
        if i != 'N/A' and i != '':
            print(f"{field}: {i} - count: {df_count[i]}")
            counts[i] = str(df_count[i])
    return counts

# Returns info for a given field
def get_info(df, field):
    info = {'byAmount': [], 'byCount': []}
    info['byAmount'] = get_amounts(df, field)
    info['byCount'] = get_counts(df, field)
    return info


# Returns month based on date
def get_month(date):
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    if date != 'N/A' and date != '':
        return months[int(date.split('-')[1])-1]
    return 'N/A'


# Returns weekday based on date
def get_weekday(date):
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    if date != 'N/A' and date != '':
        date_converted = datetime.datetime.strptime(date, "%Y-%m-%d")
        return days[date_converted.weekday()]
    return 'N/A'


# Data analysis
def get_overview_info(data):

    # Loading data into a dataframe for easier manipulation
    try:
        df = pd.DataFrame.from_dict(data)
        logging.info("Loaded data into df.")
    except Exception as e:
        df = None
        logging.error(f"Could not load data into df: {e}")

    if not df.empty:
        overview_info = {}
        overview_info['total'] = df['amount'].sum()
        df['timerange'] = df['time'].apply(lambda x: x[:2])
        df['weekday'] = df['date'].apply(lambda x: get_weekday(x))
        df['month'] = df['date'].apply(lambda x: get_month(x))
        overview_info['category'] = get_info(df, 'PartitionKey')
        overview_info['date'] = get_info(df, 'date')
        overview_info['weekday'] = get_info(df, 'weekday')
        overview_info['month'] = get_info(df, 'month')
        overview_info['timerange'] = get_info(df, 'timerange')
        overview_info['merchant'] = get_info(df, 'merchant')
        return overview_info

    return None


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Overview function processed a request.')

    INFO_TABLE = os.environ['INFO_TABLE']
    CONNECTION_STRING = os.environ['STORAGE_CONNECTION_STRING']

    data = storage_helpers.query_entities(INFO_TABLE, CONNECTION_STRING)
    overview_info = get_overview_info(data)

    if overview_info:
        return func.HttpResponse(json.dumps(overview_info), status_code=200)
    else:
        return func.HttpResponse(
             "Overview analysis failed.",
             status_code=500
        )
