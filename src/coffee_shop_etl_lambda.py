import logging
import os
import etl
from utils import s3_utils

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def lambda_handler(event, context):
    LOGGER.info('lambda_handler: starting')

    try:
        # LOGGER.info(f'lambda_handler: done')
        # Ensure the event contains records
        bucket_name, file_path = s3_utils.get_file_info(event)
        
        if "Records" not in event or len(event["Records"]) == 0:

            raise KeyError("No Records found in the event payload")
                # Extract bucket name and file key
        LOGGER.info(f"Processing file: {file_path} from bucket: {bucket_name}")

        # Load and process the CSV file
        csv_content = s3_utils.load_file(bucket_name, file_path)
        raw_data = etl.extract(csv_content)
        transformed_data = etl.transform(raw_data)
        normalized_tables = etl.normalize(transformed_data)

        

    except Exception as err:
        LOGGER.error(f'lambda_handler: failure: error={err}')
        raise err
