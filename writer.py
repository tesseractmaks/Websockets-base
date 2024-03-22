import asyncio
import json

from config import sender_log


async def send_messages(HOST, PORT, message):
    query = "f5e19a9c-e81d-11ee-aae7-0242ac110002\n"

    reader, writer = await asyncio.open_connection(
        HOST, PORT
    )

    data = await reader.readline()
    sender_log.debug(f'{data.decode()!r}')

    writer.write(query.encode())
    sender_log.debug(query)
    await writer.drain()

    token = await reader.readline()
    if not json.loads(token):
        sender_log.debug("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
        await writer.drain()
    else:
        sender_log.debug(f'{token.decode()!r}')

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

asyncio.run(send_messages(send_host, send_port, message))