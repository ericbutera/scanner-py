import asyncio
import os
import time

import aiohttp
from aiohttp import ClientSession
from cloudevents.conversion import to_json

from shared import (API_URL, ENDPOINT_URL, PAYLOAD_ENDPOINT, TIMEOUT,
                    VERIFY_SSL, bucket_to_event, list_buckets)


async def main():
    print("starting async io")
    start = time.perf_counter()

    # this blocks per call for some reason
    async with _get_session() as session:
        for bucket in list_buckets(ENDPOINT_URL):
            event = bucket_to_event(bucket)
            await emit(session, event)

    end = time.perf_counter()
    delta = end - start
    print("time: ", delta)


async def emit(session: ClientSession, event):
    """emit"""
    # headers, body = to_binary(event)
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.getenv("API_KEY"),
    }
    body = to_json(event, data_marshaller=str)

    async with session.post(
        PAYLOAD_ENDPOINT,
        headers=headers,
        data=body,
        verify_ssl=VERIFY_SSL,
        timeout=TIMEOUT
    ) as response:
        # print("status ", response.status)
        return response


async def _get_session():
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": os.getenv("API_KEY"),
    }
    return aiohttp.ClientSession(base_url=API_URL, headers=headers)

if __name__ == "__main__":
    asyncio.run(main())
