import os
import logging
import azure.functions as func
from ..shared import storage_helpers


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get Receipts Info function processed a request.')

    INFO_TABLE = os.environ['INFO_TABLE']
    CONNECTION_STRING = os.environ['STORAGE_CONNECTION_STRING']

    info_list = storage_helpers.query_entities(INFO_TABLE, CONNECTION_STRING)

    if len(info_list) > 0:
        return func.HttpResponse(str(info_list), status_code=200)
    else:
        return func.HttpResponse(
             "Could not get the list of info.",
             status_code=500
        )
