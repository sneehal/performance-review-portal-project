# app.py
# Flask AI Service entry point

from flask import Flask
from flask_cors import CORS
from routes.chatbot_routes import chatbot_bp
from config import config

# Create Flask app
app = Flask(__name__)

# Allow React frontend to call this service
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

# Register chatbot blueprint (group of routes)
app.register_blueprint(chatbot_bp)


@app.route("/")
def root():
    return {
        "status": "running",
        "service": "Performance Review Portal - Flask AI Service",
        "endpoints": ["/chatbot/ask", "/chatbot/health"]
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )