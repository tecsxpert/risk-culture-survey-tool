from flask import Flask, request, jsonify
from services.input_sanitizer import validate_request
from routes.categorise import categorise_bp   # 👈 NEW

app = Flask(__name__)

# 👇 Register teammate route
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