import asyncio

def do_sync():
    print("do_sync")


async def do_async():
    print("do_async")


async def main_async():
    await do_async()

asyncio.run(main_async())