import asyncio
import websockets
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Store the goal
goal_position = {"corner": None}

# Flask route to set goal
@app.route('/goal', methods=['POST'])
def set_goal():
    data = request.json
    if "corner" in data:
        goal_position["corner"] = data["corner"]
        return jsonify({"status": "success", "goal": goal_position["corner"]})
    return jsonify({"status": "error", "message": "No corner provided"}), 400

# Flask route to get current goal
@app.route('/goal', methods=['GET'])
def get_goal():
    if goal_position["corner"]:
        return jsonify({"goal": goal_position["corner"]})
    return jsonify({"goal": None})

# WebSocket handler
async def ws_handler(websocket, path=None):
    print("WebSocket client connected")
    try:
        async for message in websocket:
            print("Received:", message)
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket client disconnected")

# Start Flask without blocking asyncio
async def start_flask():
    await asyncio.to_thread(app.run, host='127.0.0.1', port=5000)

async def main():
    ws_server = await websockets.serve(ws_handler, "localhost", 8080)
    print("WebSocket server started on ws://localhost:8080")
    
    await start_flask()

if __name__ == "__main__":
    asyncio.run(main())
