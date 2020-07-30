import asyncio
import aiohttp
import os
import time
import traceback
import asyncpg


POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

async def fetch(url, session, pgpool):
    start = time.time()
    async with session.get(url) as response:
        end = time.time()
        duration = end - start
        print("status: {code}; duration {duration}; {url}".format(
            code=response.status,
            duration=duration,
            url=url
        ))
        async with pgpool.acquire() as connection:
            async with connection.transaction():
                await connection.execute('''
                    INSERT INTO urlcheck(url, duration, response_code) VALUES($1, $2, $3)
                ''', url, duration, response.status)


async def bound_fetch(sem, url, session, pgpool):
    async with sem:
        try:
            await fetch(url, session, pgpool)
        except asyncio.TimeoutError:
            pass
        except:
            # todo logging
            traceback.print_exc()


async def run(concurrency, timeout):
    with open("./data/urls.txt") as f:
        content = f.readlines()
    urls = [x.strip() for x in content]

    pgpool = await asyncpg.create_pool(host='db', database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)
    tasks = []
    sem = asyncio.Semaphore(concurrency)
    client_timeout = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        for url in urls:
            task = asyncio.ensure_future(bound_fetch(sem, url, session, pgpool))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

interval = int(os.getenv('INTERVAL', 60))
concurrency = int(os.getenv('CONCURRENCY', 1))
timeout = int(os.getenv('TIMEOUT', 30))
print("interval/concurrency/timeout: {}/{}/{}".format(interval, concurrency, timeout))

while True:
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(concurrency, timeout))
    loop.run_until_complete(future)
    time.sleep(interval)