import asyncio
import websockets
import json
import requests
import os

GRID_SIZE = 5  # 5x5 grid

# Clear the console for visual effect
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Draw the grid showing robot and goal
def draw_grid(robot_pos, goal_pos):
    clear_console()
    for y in range(GRID_SIZE):
        row = ""
        for x in range(GRID_SIZE):
            if (x, y) == robot_pos:
                row += "🤖 "
            elif (x, y) == goal_pos:
                row += "🎯 "
            else:
                row += ". "
        print(row)
    print("\n")  # Space between frames

# Map goal corners to coordinates
goal_corner = "NE"  # Can be NE, NW, SE, SW
goal_coords = {
    "NE": (GRID_SIZE-1, 0),
    "NW": (0, 0),
    "SE": (GRID_SIZE-1, GRID_SIZE-1),
    "SW": (0, GRID_SIZE-1)
}
goal_pos = goal_coords.get(goal_corner, (GRID_SIZE-1, 0))

# Set the goal using Flask server
try:
    resp = requests.post("http://127.0.0.1:5000/goal", json={"corner": goal_corner})
    print("Goal set:", resp.json())
except Exception as e:
    print("Error setting goal:", e)

# Connect to WebSocket server
async def robot_client():
    uri = "ws://localhost:8080"
    robot_pos = (0, GRID_SIZE-1)  # Start at bottom-left (SW)
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")

        while robot_pos != goal_pos:
            # Determine next move toward goal
            dx = goal_pos[0] - robot_pos[0]
            dy = goal_pos[1] - robot_pos[1]
            if dx > 0:
                direction = "right"
                robot_pos = (robot_pos[0]+1, robot_pos[1])
            elif dx < 0:
                direction = "left"
                robot_pos = (robot_pos[0]-1, robot_pos[1])
            elif dy > 0:
                direction = "down"
                robot_pos = (robot_pos[0], robot_pos[1]+1)
            elif dy < 0:
                direction = "up"
                robot_pos = (robot_pos[0], robot_pos[1]-1)
            else:
                break  # Already at goal

            # Send movement command
            command = {"action": "move", "direction": direction}
            await websocket.send(json.dumps(command))
            reply = await websocket.recv()

            # Draw the grid
            draw_grid(robot_pos, goal_pos)

            print(f"Sent command: {command}, Server replied: {reply}")
            await asyncio.sleep(0.5)  # Pause to see movement

        print("Robot reached the goal!")

# Run the WebSocket client
asyncio.run(robot_client())
