from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from services.input_sanitizer import validate_request
from routes.categorise import categorise_bp

app = Flask(__name__)

# ✅ Rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

# ✅ Handle rate limit error
@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({
        "error": "Too many requests",
        "message": "Rate limit exceeded. Try again later."
    }), 429

# ✅ Register routes
app.register_blueprint(categorise_bp)

# ✅ Input validation middleware
@app.before_request
def check_input():
    if request.method in ["POST", "PUT"]:
        error = validate_request()
        if error:
            return error

# ✅ Health check endpoint (important for later days)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "AI Service"
    })

# ✅ Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI Service is running successfully 🚀"
    })

# ✅ Test route
@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    return jsonify({
        "message": "Request passed successfully",
        "cleaned_data": data
    })

if __name__ == "__main__":
    app.run()