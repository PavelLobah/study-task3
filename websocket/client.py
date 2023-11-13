import asyncio
import websockets


async def client():
    previous_price = None  
    async with websockets.connect('ws://localhost:8000') as websocket:
        while True:
            data = await websocket.recv()
            ts, price = data.split(" - ")

            if previous_price is None:
                previous_price = float(price)
                continue

            current_price = float(price)
            percent_change = ((current_price - previous_price) / previous_price) * 100

            print(f"Date-Time: {ts}, New price: {price}, Price change: {percent_change:.2f}%")
            previous_price = current_price

asyncio.get_event_loop().run_until_complete(client())
