import argparse
import asyncio
import datetime

from pathlib import Path

import aiofiles

OUT_PATH = (Path(__file__).parent / 'chat.log').absolute()
HOST = "188.246.233.198"
PORT = 5000


def get_arguments():
    parser = argparse.ArgumentParser(
        description='The code run chat.'
    )
    parser.add_argument(
        '--path',
        type=str,
        help="Set path to catalog use arguments: '--path'"
    )
    parser.add_argument(
        '--host',
        type=str,
        help="Enter host use arguments: '--host'"
    )
    parser.add_argument(
        '--port',
        type=int,
        help="Enter port use argument: '--port' set number"
    )
    args = parser.parse_args()
    return args.path, args.host, args.port


async def write_to_disk(data, file_path=OUT_PATH):
    time_now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    async with aiofiles.open(file_path, mode='a') as f:
        await f.write(f"[{time_now}] {data.decode()!r}\n")


async def get_messages(OUT_PATH, HOST, PORT):
    reader, writer = await asyncio.open_connection(
        HOST, PORT,
    )
    while True:
        data = await reader.read(300)
        await write_to_disk(data, OUT_PATH)
        print(f'Received: {data.decode()!r}')
    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':

    path, host, port = get_arguments()
    if not path:
        path = OUT_PATH
    if not host:
        host = HOST
    if not port:
        port = PORT

    asyncio.run(get_messages(path, host, port))



