import asyncio


async def send_messages(HOST, PORT, message):
    query = "f5e19a9c-e81d-11ee-aae7-0242ac110002\n"

    reader, writer = await asyncio.open_connection(
        HOST, PORT
    )

    data = await reader.read(300)
    print(f'{data.decode()!r}')

    writer.write(query.encode())
    await writer.drain()

    writer.write(message.encode())
    await writer.drain()

    writer.write("\n".encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()

message = "!!! -My message -!!!\n"

send_host = "minechat.dvmn.org"
send_port = 5050

asyncio.run(send_messages(send_host, send_port, message))