import os

import boto3
from cloudevents.http import CloudEvent
from dotenv import load_dotenv

VERIFY_SSL = False  # if dev
TIMEOUT = 10

EVENT_BUCKET_LIST = "io.butera.scanner.aws.s3.bucket.list"
EVENT_BUCKET = "io.butera.scanner.aws.s3.bucket"

load_dotenv()

ENDPOINT_URL = os.getenv("ENDPOINT_URL")

API_URL = os.getenv("API_URL")
PAYLOAD_ENDPOINT = os.getenv("PAYLOAD_ENDPOINT")
EVENT_RECEIVER_URL = f"{API_URL}{PAYLOAD_ENDPOINT}"


def list_buckets(endpoint_url):
    """list buckets"""
    print("lsiting buckets", endpoint_url)
    client = boto3.client("s3", endpoint_url=endpoint_url)
    buckets = client.list_buckets().get("Buckets", [])
    print("fetched buckets: ", len(buckets))
    return buckets


def bucket_to_event(bucket) -> CloudEvent:
    attributes = {
        "type": EVENT_BUCKET,
        "source": "scanner-py",
    }
    data = {
        "bucket": bucket["Name"],
    }
    return CloudEvent(attributes, data)
