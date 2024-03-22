import asyncio
import json
import aiofiles
from pathlib import Path

from config import sender_log

accounts = {
    "account_hash": "9b0cab56-ff6b-11e9-a4c8-0242ac110003"
}
ACCOUNTS_PATH = (Path(__file__).parent / 'accounts.json').absolute()


async def write_accounts(account, file_path=ACCOUNTS_PATH):
    async with aiofiles.open(file_path, mode='a', encoding='utf-8') as file:
        await asyncio.to_thread(json.dump(account, file, ensure_ascii=False, indent=4))


async def read_accounts(account, file_path=ACCOUNTS_PATH):
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
        accounts = await file.read()
        if account in accounts:
            return account if account in accounts else False


async def register(HOST, PORT, token):
    sender_log.debug("Enter your personal hash for create new account.")
    reader, writer = await asyncio.open_connection(
        HOST, PORT
    )
    accounts = {
        "account_hash": token
    }
    writer.close()
    await writer.wait_closed()
    await write_accounts(accounts)

    await authorise(HOST, PORT, token)


async def authorise(HOST, PORT, token):
    reader, writer = await asyncio.open_connection(
        HOST, PORT
    )
    account = await read_accounts(token)

    if account:
        sender_log.debug("Success! You are enter in account!")
        return account["account_hash"]
    else:
        sender_log.debug("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
        await register(HOST, PORT, token)

    await register(HOST, PORT, token)
    await authorise(HOST, PORT, token)

async def submit_message(HOST, PORT, message):

    reader, writer = await asyncio.open_connection(
        HOST, PORT
    )

    data = await reader.readline()
    sender_log.debug(f'{data.decode()!r}')

    # writer.write(token.encode())
    # sender_log.debug(token)
    # await writer.drain()

    # token = await reader.readline()
    # if not json.loads(token):
    #     sender_log.debug("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
    #     await writer.drain()
    # else:
    #     sender_log.debug(f'{token.decode()!r}')

    writer.write(message.encode())
    sender_log.debug(message)
    await writer.drain()

    writer.write("\n".encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()

message = "!!! -My message -!!!\n"

send_host = "minechat.dvmn.org"
send_port = 5050

asyncio.run(submit_message(send_host, send_port, message))