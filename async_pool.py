# WORK IN PROGRESS!
# https://stackoverflow.com/a/55780438/261272
import asyncio
import logging
from functools import partial

import asyncpool

from shared import (API_URL, ENDPOINT_URL, PAYLOAD_ENDPOINT, TIMEOUT,
                    VERIFY_SSL, bucket_to_event, list_buckets)


async def fetcher(bucket, queue):
    # print("Processing Value! -> {} * 2 = {}".format(initial_number, initial_number * 2))
    await emit(bucket_to_event(bucket))
    await asyncio.sleep(1)
    await queue.put(initial_number * 2)


async def result_reader(queue):
    while True:
        value = await queue.get()
        if value is None:
            break
        print("Got value! -> {}".format(value))


async def emit(event):
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


async def main():
    queue = asyncio.Queue()

    reader_future = asyncio.ensure_future(
        result_reader(queue), loop=loop)

    # Start a worker pool with 10 coroutines, invokes `example_coro` and waits for it to complete or 5 minutes to pass.

    worker_co = partial(get_object, client, bucket)
    async with asyncpool.AsyncPool(
        loop,
        num_workers=10,
        name="ExamplePool",
        logger=logging.getLogger("ExamplePool"),
        worker_co=fetcher,
        max_task_time=300,
        log_every_n=10
    ) as pool:
        for bucket in list_buckets(ENDPOINT_URL):
            await pool.push(bucket, queue)

    await queue.put(None)
    await reader_future

loop = asyncio.get_event_loop()

loop.run_until_complete(main())
