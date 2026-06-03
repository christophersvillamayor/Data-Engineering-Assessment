import os
import json
import boto3
import logging
from typing import Tuple
from urllib.parse import unquote_plus

from orders_analytics import OrdersAnalytics

s3_client = boto3.client('s3')

"""
Modify this lambda function to perform the following questions

1. Find the most profitable Region, and its profit
2. What shipping method is most common for each Category
3. Output a glue table containing the number of orders for each Category and Sub Category
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL', 'INFO').upper()))

def get_s3_info_from_event(event: dict) -> Tuple[str, str]:
    """
    Extract bucket and key from S3 event
    """

    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]
    key = unquote_plus(record["s3"]["object"]["key"])

    return bucket, key


def load_csv_from_s3(bucket: str, key: str) -> OrdersAnalytics:
    """
    Load CSV from S3 into OrderAnalytics class
    """

    response = s3_client.get_object(Bucket=bucket, Key=key)
    return OrdersAnalytics(response['Body'])

def lambda_handler(event, context):
    "Lambda function to process S3 events and perform analytics on orders data"

    logger.info(f"Received event: {json.dumps(event, indent=2)}")

    bucket, key = get_s3_info_from_event(event)

    logger.info(f"Processing file: s3://{bucket}/{key}")
    oa = load_csv_from_s3(bucket, key)
    oa.generate_output_csvs()

    # FIXME: remove test output
    return {
        "statusCode": 200,
        "body": {
            "test": "test"
        }
    }