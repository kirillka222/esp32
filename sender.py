import asyncio
import websockets
import json
import random

async def send_data():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        while True:
            x = round(random.uniform(0, 100), 1)
            y = round(random.uniform(0, 100), 1)
            z = round(random.uniform(0, 20), 1)
            speed = round(random.uniform(0, 10), 1)
            data = {"x": x, "y": y, "z": z, "speed": speed}
            await websocket.send(json.dumps(data))
            print("Отправлено:", data)
            await asyncio.sleep(1)

asyncio.run(send_data())


