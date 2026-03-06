from flask import Flask, request, jsonify
from routing import route_query

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Backend is running successfully"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Query not provided"}), 400

    user_query = data["query"]
    department = route_query(user_query)

    return jsonify({
        "query": user_query,
        "assigned_category": department
    })

if __name__ == "__main__":
    app.run(debug=True)