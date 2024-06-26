import argparse
import asyncio
from config import sender_log, OpenConnection
from os import getenv


def encode_utf8(data):
    return data.encode("utf-8", "ignore")


async def register(host, port, parser):
    async with OpenConnection(host, port) as (reader, writer):
        data = await reader.readline()
        sender_log.debug(f"{data.decode()!r}")

        writer.write("\n".encode())
        await writer.drain()

        data_2 = await reader.readline()
        sender_log.debug(f"{data_2.decode()!r}")

        writer.write(parser.reg.encode())
        sender_log.debug(f"{parser.reg}")
        await writer.drain()

        writer.write("\n".encode())
        await writer.drain()

        data_3 = await reader.readline()
        sender_log.debug(f"{data_3.decode()!r}")

        writer.write("\n".encode())
        await writer.drain()


async def authorise(host, port, parser):
    async with OpenConnection(host, port) as (reader, writer):
        data = await reader.readline()
        sender_log.debug(f"{data.decode()!r}")

        writer.write(parser.token.encode())
        sender_log.debug(f"{parser.token} --")
        await writer.drain()

        writer.write("\n".encode())
        await writer.drain()

        data3 = await reader.readline()
        sender_log.debug(f"{data3.decode()!r}")
        await submit_message(reader, writer, parser.msg)


async def submit_message(reader, writer, message):
    writer.write("\n".encode())
    await writer.drain()

    data = await reader.readline()
    writer.write(data)
    await writer.drain()

    writer.write("\n".encode())
    await writer.drain()

    writer.write(encode_utf8(f"{message.strip()}\n"))
    sender_log.debug(message)
    await writer.drain()

    writer.write("\n".encode())
    await writer.drain()


def argparser():

    parser = argparse.ArgumentParser(description="Chat client")

    parser.add_argument(
        "-ht",
        "--host",
        type=str,
        default=str(getenv("CHAT_HOST", "minechat.dvmn.org")),
        help="Enter host",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=int(getenv("CHAT_PORT", 5050)),
        help="Enter port",
    )
    parser.add_argument("-t", "--token", type=str, help="Enter hash token")
    parser.add_argument("-r", "--reg", type=str, help="Enter nickname for registration")
    parser.add_argument("msg", type=str, help="Enter message")
    return parser.parse_args()


async def main():
    parser = argparser()
    host = parser.host
    port = parser.port

    if parser.reg:
        await register(host, port, parser)

    if parser.token:
        await authorise(host, port, parser)


if __name__ == "__main__":
    asyncio.run(main())
