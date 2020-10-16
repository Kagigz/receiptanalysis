import os
import logging
import azure.functions as func
from ..shared import storage_helpers

def get_imgs_list(location, sas_token, container_name, connection_string):

    imgs_list = []
    blobs = storage_helpers.list_blobs(container_name, connection_string)
    for blob in blobs:
        imgs_list.append(f"{location}{blob}{sas_token}")
    return imgs_list



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get Receipts Images function processed a request.')

    IMG_CONTAINER = os.environ['IMG_CONTAINER']
    CONNECTION_STRING = os.environ['STORAGE_CONNECTION_STRING']
    ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
    SAS_TOKEN = os.environ['SAS_TOKEN']
    imgs_location = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{IMG_CONTAINER}/"

    imgs_list = get_imgs_list(imgs_location, SAS_TOKEN, IMG_CONTAINER, CONNECTION_STRING)

    if len(imgs_list) > 0:
        return func.HttpResponse(str(imgs_list), status_code=200)
    else:
        return func.HttpResponse(
             "Could not get the list of images.",
             status_code=500
        )
