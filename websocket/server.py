import asyncio
import random
import websockets
from datetime import datetime

async def generate_data():
    while True:
        ts = str(datetime.now())
        price = random.randint(1, 100)
        data = f"{ts} - {price}"
        yield data
        await asyncio.sleep(1)

async def server(websocket):
    data_generator = generate_data()
    async for data in data_generator:
        await websocket.send(data)

start_server = websockets.serve(server, 'localhost', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
