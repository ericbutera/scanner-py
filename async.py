import asyncio
import os
import time

import aiohttp
from aiohttp import ClientSession
from cloudevents.conversion import to_json

from shared import (API_URL, ENDPOINT_URL, PAYLOAD_ENDPOINT, TIMEOUT,
                    VERIFY_SSL, bucket_to_event, list_buckets)

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": os.getenv("API_KEY"),
}


async def main():
    print("starting async io")
    start = time.perf_counter()

    # TODO this will OOM; need to use a semaphore
    async with aiohttp.ClientSession(base_url=API_URL, headers=headers) as session:
        tasks = []
        for bucket in list_buckets(ENDPOINT_URL):
            ev = bucket_to_event(bucket)
            task = emit(session, ev)
            tasks.append(asyncio.ensure_future(task))

        results = await asyncio.gather(*tasks)
        print(results)

    end = time.perf_counter()
    delta = end - start
    print("time: ", delta)


async def emit(session: ClientSession, event):
    """emit"""
    # headers, body = to_binary(event)
    body = to_json(event, data_marshaller=str)
    async with session.post(
        PAYLOAD_ENDPOINT,
        # headers=headers,
        data=body,
        verify_ssl=VERIFY_SSL,
        timeout=TIMEOUT
    ) as resp:
        return await resp.text()


if __name__ == "__main__":
    asyncio.run(main())
