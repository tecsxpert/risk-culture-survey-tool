from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask import Flask, request, jsonify
from services.input_sanitizer import validate_request
from routes.categorise import categorise_bp   # 👈 teammate import

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return {
        "error": "Too many requests",
        "message": "Rate limit exceeded. Try again later."
    }, 429

# 👇 register teammate route
app.register_blueprint(categorise_bp)

@app.before_request
def check_input():
    if request.method in ["POST", "PUT"]:
        error = validate_request()
        if error:
            return error

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Service is running successfully 🚀"})

@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    return jsonify({
        "message": "Request passed successfully",
        "cleaned_data": data
    })

if __name__ == "__main__":
    app.run(debug=True)