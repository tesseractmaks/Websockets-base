import asyncio
import datetime
import aiofiles
from config import reader_log


async def write_to_disk(data, file_path):
    time_now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    async with aiofiles.open(file_path, mode="a") as f:
        await f.write(f"[{time_now}] {data.decode()!r}\n")


async def get_messages(out_path, host, port):
    reader, writer = await asyncio.open_connection(
        host,
        port,
    )
    try:

        while True:
            data = await reader.read(300)
            await write_to_disk(data, out_path)
            print(f"Received: {data.decode()!r}")
        writer.close()
        await writer.wait_closed()
    except (ConnectionRefusedError, ConnectionResetError, ConnectionError) as exc:
        reader_log.error(exc)
        writer.close()
        await writer.wait_closed()
