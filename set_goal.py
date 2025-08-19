from flask import Flask, request, jsonify

app = Flask(__name__)
current_goal = None

@app.route('/goal', methods=['POST'])
def set_goal():
    global current_goal
    data = request.json
    current_goal = data.get("corner")
    return jsonify({"status": "success", "goal": current_goal})
