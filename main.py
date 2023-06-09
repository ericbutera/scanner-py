"""test"""
import os
import time

import requests
from cloudevents.conversion import to_json

from shared import (ENDPOINT_URL, EVENT_RECEIVER_URL, TIMEOUT, VERIFY_SSL,
                    bucket_to_event, list_buckets)


def main():
    """test"""
    print("start thread test")
    start = time.perf_counter()

    for bucket in list_buckets(ENDPOINT_URL):
        ev = bucket_to_event(bucket)
        emit(ev)

    end = time.perf_counter()
    delta = end - start
    print("time: ", delta)


def emit(event):
    """emit"""
    # headers, body = to_binary(event)
    body = to_json(event, data_marshaller=str)
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.getenv("API_KEY"),
    }
    res = requests.post(
        EVENT_RECEIVER_URL,
        headers=headers,
        data=body,
        verify=VERIFY_SSL,
        timeout=TIMEOUT
    )
    #  if resp.status_code == 200
    print("body ", res.text)
    return res.text


if __name__ == "__main__":
    main()
