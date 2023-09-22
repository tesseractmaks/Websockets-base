import asyncio


async def get_messages():
    reader, writer = await asyncio.open_connection(
        "minechat.dvmn.org", 5000,
    )
    while True:
        data = await reader.read(300)
        print(f'Received: {data.decode()!r}')

asyncio.run(get_messages())
