import asyncio
import websockets

async def test_ws():
    uri = "ws://localhost:8080"  # WebSocket server address
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello Server")  # Send a test message
        response = await websocket.recv()     # Receive server response
        print("Server replied:", response)

asyncio.run(test_ws())
