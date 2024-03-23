import argparse
import asyncio
import json
import aiofiles
from pathlib import Path
from passlib.context import CryptContext
from config import sender_log

accounts = {
    "account_hash": "9b0cab56-ff6b-11e9-a4c8-0242ac110003"
}
ACCOUNTS_PATH = (Path(__file__).parent / 'accounts.json').absolute()


def decode_utf8(data):
    return data.decode("utf-8", "ignore")


def encode_utf8(data):
    return data.encode("utf-8", "ignore")


async def write_accounts(account, file_path=ACCOUNTS_PATH):
    async with aiofiles.open(file_path, mode='a', encoding='utf-8') as file:
        await file.write(json.dumps(account, ensure_ascii=False, indent=4))


async def read_accounts(account, file_path=ACCOUNTS_PATH):
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
        accounts = await file.read()
        if account in accounts:
            return account if account in accounts else False


async def register(HOST, PORT, parser):
    reader, writer = await asyncio.open_connection(
        HOST, PORT
    )

    data = await reader.readline()
    sender_log.debug(f'{data.decode()!r}')

    writer.write("\n".encode())
    await writer.drain()

    data2 = await reader.readline()
    sender_log.debug(f'{data2.decode()!r}')  # 'Enter preferred nickname below:\n'

    writer.write(parser.reg.encode())
    sender_log.debug(f"{parser.reg} --")  # DEBUG:writer:nik --
    await writer.drain()

    writer.write("\n".encode())
    await writer.drain()

    data3 = await reader.readline()
    sender_log.debug(f'{data3.decode()!r}')

    # await write_accounts(json.loads(data3.decode()))

    writer.write("\n".encode())
    await writer.drain()

    # find_nickname = await read_accounts(parser.nickname)
    #
    # if find_nickname:
    #     sender_log.debug("Username already exist.")
    #     writer.close()
    #     await writer.wait_closed()
    #     return
    #
    # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # hash_code = pwd_context.hash(find_nickname.decode())
    #
    # accounts = {
    #     "nickname": find_nickname.decode(),
    #     "account_hash": hash_code
    # }
    # sender_log.debug(accounts)
    #
    # writer.write(accounts.encode())
    # sender_log.debug(f"{parser.nickname} --")  # DEBUG:writer:nik --
    # await writer.drain()


    writer.close()
    await writer.wait_closed()
    # await write_accounts(accounts)

    # await authorise(HOST, PORT, token)


async def authorise(HOST, PORT, parser):
    reader, writer = await asyncio.open_connection(
        HOST, PORT
    )

    data = await reader.readline()
    sender_log.debug(f'{data.decode()!r}')

    # writer.write("\n".encode())
    # await writer.drain()
    #
    # data2 = await reader.readline()
    # sender_log.debug(f'{data2.decode()!r}')  # 'Enter preferred nickname below:\n'

    writer.write(parser.token.encode())
    sender_log.debug(f"{parser.token} --")  # DEBUG:writer:nik --
    await writer.drain()

    writer.write("\n".encode())
    await writer.drain()

    data3 = await reader.readline()
    sender_log.debug(f'{data3.decode()!r}')

    message = "!!! -My message -!!!"

    await submit_message(reader, writer, message)


async def submit_message(reader, writer, message):

    writer.write("\n".encode())
    await writer.drain()

    data = await reader.readline()
    writer.write(data)

    writer.write("\n".encode())
    await writer.drain()
    await asyncio.sleep(0.05)

    writer.write(encode_utf8(f"{message.strip()}\n"))
    sender_log.debug(message)
    await writer.drain()

    writer.write("\n".encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()


def argparser():

    parser = argparse.ArgumentParser(description="Chat client")

    parser.add_argument("-ht", "--host", type=str, default="minechat.dvmn.org", help="Enter host")
    parser.add_argument("-p", "--port", type=int, default=5050, help="Enter port")
    parser.add_argument("-t", "--token", type=str,  help="Enter hash token")
    parser.add_argument("-r", "--reg", type=str,  help="Enter nickname for registration")
    return parser.parse_args()


async def main():
    parser = argparser()
    host = parser.host
    port = parser.port

    if parser.reg:
        await register(host, port, parser)

    if parser.token:
        await authorise(host, port, parser)


asyncio.run(main())