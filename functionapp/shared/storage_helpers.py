import logging
from azure.storage.blob import BlobServiceClient
from azure.cosmosdb.table.tableservice import TableService

##############
# BLOB STORAGE
##############


# Creates a blob service client
def create_blob_service_client(connection_string):
    blob_service_client = None
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        logging.info("Created blob service client.")
    except Exception as e:
        logging.error(f"Could not create blob service client: {e}")
    return blob_service_client


# Lists all the blobs in a given container
def list_blobs(container_name, connection_string):
    blob_service_client = create_blob_service_client(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blobs = []
    try:
        blob_list = container_client.list_blobs()
        print(blob_list)
        logging.info(f"Found {str(len(blobs))} blobs.")
    except Exception as e:
        logging.error(f"Could not list blobs: {e}")
    return blobs


# Creates a blob in blob storage from bytes
def upload_blob(container_name, blob_name, data, connection_string):
    blob_service_client = create_blob_service_client(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    try:
        blob_client.upload_blob(data=data)
        logging.info(f"Created blob {blob_name} successfully.")
        return True
    except Exception:
        try:
            blob_client.delete_blob()
            blob_client.upload_blob(data=data)
            logging.warning(f"Blob {blob_name} already exists, deleted it.")
            logging.info(f"Created blob {blob_name} successfully.")
            return True
        except Exception as e:
            logging.error(f"Error creating blob {blob_name}: {e}")
    return False


###############
# TABLE STORAGE
###############


# Creates an Azure Table Storage service
def create_table_service(connection_string):
    table_service = None
    try:
        table_service = TableService(connection_string=connection_string)
    except Exception as e:
        logging.error(f"Could not instantiate table service: {e}")
    return table_service


# Creates an entity if it doesn't exist, updates it if it does
def insert_or_replace_entity(table_name, entity, connection_string):
    table_service = create_table_service(connection_string)
    try:
        table_service.insert_or_replace_entity(table_name, entity)
        logging.info(f"Saved entity {entity} in table {table_name}.")
        return True
    except Exception as e:
        logging.error(f"Could not insert or update entity in table {table_name}:{e}")
        return False


# Queries a table to get an entity's info
def get_info(table_name, partition_key, row_key, connection_string):
    table_service = create_table_service(connection_string)
    try:
        entity = table_service.get_entity(table_name, partition_key, row_key)
        status = entity.status
        return status
    except Exception as e:
        logging.info(f"Could not query entity {row_key} in table {table_name}:{e}")
        return None


# Queries a table to get a list of entities
def query_entities(table_name, connection_string):
    table_service = create_table_service(connection_string)
    try:
        entities = table_service.query_entities(table_name)
        logging.info("Retrieved all entities.")
        return [e for e in entities]
    except Exception as e:
        logging.error(f"Could not query entities: {e}")
        return None
