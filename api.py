from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Gesture Controlled Virtual Mouse API is Live"

@app.route("/status")
def status():
    return jsonify({
        "project": "Gesture Controlled Virtual Mouse",
        "engine": "Runs locally (OpenCV + MediaPipe)",
        "deployment": "Render"
    })

@app.route("/gestures")
def gestures():
    return jsonify({
        "move": "Index finger",
        "left_click": "Thumb + Index pinch",
        "right_click": "Index + Middle",
        "drag": "Fist",
        "scroll": "Open palm"
    })
