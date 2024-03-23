import argparse
import asyncio

from os import getenv
from pathlib import Path

from reader import get_messages


OUT_PATH = (Path(__file__).parent / 'chat.log').absolute()
HOST_CLIENT = str(getenv("HOST_CLIENT", "188.246.233.198"))
PORT_CLIENT = int(getenv("PORT_CLIENT", 5000))


def get_arguments():
    parser = argparse.ArgumentParser(
        description='The code run chat.'
    )
    parser.add_argument(
        "-ph",
        '--path',
        type=str,
        help="Set path to catalog use arguments: '--path'"
    )
    parser.add_argument(
        "-ht",
        '--host',
        type=str,
        help="Enter host use arguments: '--host'"
    )
    parser.add_argument(
        "p",
        '--port',
        type=int,
        help="Enter port use argument: '--port' set number"
    )
    args = parser.parse_args()
    return args.path, args.host, args.port


if __name__ == '__main__':

    path, host, port = get_arguments()
    if not path:
        path = OUT_PATH
    if not host:
        host = HOST_CLIENT
    if not port:
        port = PORT_CLIENT

    asyncio.run(get_messages(path, host, port))

