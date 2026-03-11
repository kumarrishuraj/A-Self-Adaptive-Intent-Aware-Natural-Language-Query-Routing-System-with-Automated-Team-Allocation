from flask import Flask, request, jsonify

from Services.routing_service import route_query
from Services.ticket_service import create_ticket, get_tickets, resolve_ticket

app = Flask(__name__)


@app.route("/submit_query", methods=["POST"])
def submit_query():

    data = request.json

    name = data["name"]
    reg_no = data["reg_no"]
    query = data["query"]

    departments = route_query(query)

    ticket = create_ticket(name, reg_no, query, departments)

    return jsonify(ticket)


@app.route("/tickets/<department>", methods=["GET"])
def fetch_tickets(department):

    tickets = get_tickets(department)

    return jsonify(tickets)


@app.route("/resolve/<int:ticket_id>", methods=["POST"])
def resolve(ticket_id):

    ticket = resolve_ticket(ticket_id)

    return jsonify(ticket)

@app.route("/")
def home():
    return "Backend is running successfully"
if __name__ == "__main__":
    app.run(debug=True)