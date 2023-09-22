import asyncio
import datetime

from pathlib import Path

import aiofiles

OUT_PATH = (Path(__file__).parent / 'chat.log').absolute()


async def write_to_disk(data):
    file_path = OUT_PATH
    time_now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    async with aiofiles.open(file_path, mode='a') as f:
        # for i in data:
        await f.write(f"[{time_now}] {data.decode()!r}\n")


async def get_messages():
    reader, writer = await asyncio.open_connection(
        "minechat.dvmn.org", 5000,
    )
    while True:
        data = await reader.read(300)
        await write_to_disk(data)
        print(f'Received: {data.decode()!r}')
    writer.close()
    await writer.wait_closed()

asyncio.run(get_messages())


# print(x)