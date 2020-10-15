import os
import logging
import json
from requests import post
import azure.functions as func
from ..shared import storage_helpers


def analyze_receipt(data, url, key):

    headers = {
        'X-Inferuser-Token': key
    }

    files = [('file',  data)]
    response = post(url, headers=headers, files=files)

    return response.text, response.status_code


def save_receipt(data, result, table_name, container_name, connection_string):

    # Get fields of interest from API results
    json_result = json.loads(result)
    receipt_id = json_result['documents'][0]['id']
    predictions = json_result['predictions'][0]
    category = predictions['category']['value']
    date = predictions['date']['iso']
    time = predictions['time']['iso']
    merchant = predictions['merchant']['name']
    amount = predictions['total']['amount']
    logging.info(f"Category: {category}\nDate: {date}\nMerchant: {merchant}\nAmount: {amount}")

    # Save info to Azure table
    receipt_entity = {'PartitionKey': category, 'RowKey': receipt_id, 'date': date, 'time': time, 'merchant': merchant, 'amount': amount}
    storage_helpers.insert_or_replace_entity(table_name, receipt_entity, connection_string)

    # Save image to blob storage
    file_name = receipt_id + '.jpg'
    storage_helpers.upload_blob(container_name, file_name, data, connection_string)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Analyze Receipt function processed a request.')

    file_sent = None

    API_ENDPOINT = os.environ['API_ENDPOINT']
    API_KEY = os.environ['API_KEY']
    INFO_TABLE = os.environ['INFO_TABLE']
    IMG_CONTAINER = os.environ['IMG_CONTAINER']
    CONNECTION_STRING = os.environ['STORAGE_CONNECTION_STRING']

    try:
        file_sent = req.get_body()
    except ValueError:
        pass

    if file_sent:
        result, status_code = analyze_receipt(file_sent, API_ENDPOINT, API_KEY)
        if status_code == 200:
            save_receipt(file_sent, result, INFO_TABLE, IMG_CONTAINER, CONNECTION_STRING)
            logging.info("Saved file info.")
        else:
            logging.warning(f"Did not save file info, status code: {status_code}")
        return func.HttpResponse(result, status_code=status_code)
    else:
        return func.HttpResponse(
             "Please pass a file in the request body",
             status_code=400
        )
