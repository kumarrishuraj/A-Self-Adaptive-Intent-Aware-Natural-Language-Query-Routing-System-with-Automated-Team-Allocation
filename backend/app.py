import sys
import os
import json
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, init_db
from routing import route_query

app = Flask(__name__)
# Initialize database tables
init_db()
# Enable CORS so frontend HTML files can access it
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')

def _now():
    return datetime.now().strftime("%H:%M")

def _today():
    return datetime.now().strftime("%d %b %Y")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
                
        if not token:
            return jsonify({'error': 'Token is missing or invalid!'}), 401
            
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['regNo']
        except Exception as e:
            return jsonify({'error': 'Token is invalid or expired!'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@app.route("/")
def home():
    return jsonify({"message": "TicketFlow Backend is running successfully"})

# --- Auth ---
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    regNo = data.get("regNo")
    password = data.get("password")

    if not name or not regNo or not password:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE reg_no = ?", (regNo,))
    if c.fetchone():
        conn.close()
        return jsonify({"error": "Registration number already signed up."}), 400

    password_hash = generate_password_hash(password)
    c.execute("INSERT INTO users (name, reg_no, password_hash) VALUES (?, ?, ?)",
              (name, regNo, password_hash))
    conn.commit()
    conn.close()
    
    token = jwt.encode({
        'regNo': regNo,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({"message": "User registered successfully", "token": token}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    regNo = data.get("regNo")
    password = data.get("password")

    if not regNo or not password:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT name, reg_no, password_hash FROM users WHERE reg_no = ?", (regNo,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
        token = jwt.encode({
            'regNo': user["reg_no"],
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({"user": {"name": user["name"], "regNo": user["reg_no"]}, "token": token}), 200
    else:
        return jsonify({"error": "Invalid registration number or password."}), 401

# --- Tickets ---
@app.route("/api/tickets/create", methods=["POST"])
@token_required
def create_ticket(current_user):
    data = request.json
    name = data.get("name")
    regNo = data.get("regNo")
    query = data.get("query")

    if not name or not regNo or not query:
        return jsonify({"error": "Missing fields"}), 400
        
    if current_user != regNo:
        return jsonify({"error": "Unauthorized ticket creation."}), 403

    departments = route_query(query)

    conn = get_db_connection()
    c = conn.cursor()

    # robust random ID
    ticket_id = "T-" + str(uuid.uuid4())[:8].upper()

    date_str = _today()
    time_str = _now()

    c.execute("""
        INSERT INTO tickets (id, name, reg_no, query, date, time, status, resolved_by, reply)
        VALUES (?, ?, ?, ?, ?, ?, 'Open', NULL, NULL)
    """, (ticket_id, name, regNo, query, date_str, time_str))

    for dept in departments:
        c.execute("INSERT INTO ticket_departments (ticket_id, department_name, is_current) VALUES (?, ?, 1)",
                  (ticket_id, dept))

    log_detail = f"Ticket created by {name}"
    c.execute("INSERT INTO ticket_logs (ticket_id, event, date, time, detail) VALUES (?, 'Created', ?, ?, ?)",
              (ticket_id, date_str, time_str, log_detail))

    route_detail = f"Routed to {', '.join(departments)}"
    c.execute("INSERT INTO ticket_logs (ticket_id, event, date, time, detail) VALUES (?, 'Routed', ?, ?, ?)",
              (ticket_id, date_str, time_str, route_detail))

    conn.commit()
    conn.close()

    return jsonify({
        "id": ticket_id,
        "name": name,
        "regNo": regNo,
        "query": query,
        "departments": departments,
        "status": "Open"
    }), 201

def _build_ticket_json(t, current_depts, past_depts, logs):
    return {
        "id": t["id"],
        "name": t["name"],
        "regNo": t["reg_no"],
        "query": t["query"],
        "date": t["date"],
        "time": t["time"],
        "status": t["status"],
        "resolvedBy": t["resolved_by"],
        "reply": t["reply"],
        "currentDepartments": current_depts,
        "pastDepartments": past_depts,
        "departments": current_depts + past_depts,
        "log": logs
    }

def _fetch_ticket_full(ticket_id, conn):
    c = conn.cursor()
    c.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    t = c.fetchone()
    if not t: return None

    c.execute("SELECT department_name, is_current FROM ticket_departments WHERE ticket_id = ?", (ticket_id,))
    depts = c.fetchall()
    current_depts = [d["department_name"] for d in depts if d["is_current"]]
    past_depts = [d["department_name"] for d in depts if not d["is_current"]]

    c.execute("SELECT event, date, time, detail FROM ticket_logs WHERE ticket_id = ? ORDER BY id ASC", (ticket_id,))
    logs = [dict(l) for l in c.fetchall()]

    return _build_ticket_json(t, current_depts, past_depts, logs)

@app.route("/api/tickets/student/<reg_no>", methods=["GET"])
@token_required
def get_student_tickets(current_user, reg_no):
    if current_user != reg_no:
        return jsonify({"error": "Unauthorized to view these tickets."}), 403

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM tickets WHERE reg_no = ? ORDER BY id DESC", (reg_no,))
    ticket_ids = [row["id"] for row in c.fetchall()]

    tickets = []
    for tid in ticket_ids:
        tickets.append(_fetch_ticket_full(tid, conn))
    conn.close()
    return jsonify(tickets), 200

@app.route("/api/tickets/dept/<department>", methods=["GET"])
# Note: For real world apps this should also be @token_required and verify if the user is staff for that dept
def get_dept_tickets(department):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT ticket_id FROM ticket_departments WHERE department_name = ?", (department,))
    ticket_ids = [row["ticket_id"] for row in c.fetchall()]

    tickets = []
    for tid in ticket_ids:
        t_json = _fetch_ticket_full(tid, conn)
        if t_json:
            if department not in t_json["currentDepartments"] and t_json["status"] == "Open":
                t_json["status"] = "Rerouted"
            tickets.append(t_json)
    
    # Sort tickets (newest first)
    tickets.sort(key=lambda x: str(x["id"]), reverse=True)
    conn.close()
    return jsonify(tickets), 200

@app.route("/api/tickets/resolve/<ticket_id>", methods=["POST"])
# Note: Should be restricted to department staff securely
def resolve_ticket(ticket_id):
    data = request.json
    reply = data.get("reply", "")
    department = data.get("department", "System")

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE tickets SET status = 'Resolved', resolved_by = ?, reply = ? WHERE id = ?",
              (department, reply, ticket_id))

    date_str = _today()
    time_str = _now()
    log_detail = f"Resolved by {department}" + (f': "{reply}"' if reply else "")
    c.execute("INSERT INTO ticket_logs (ticket_id, event, date, time, detail) VALUES (?, 'Resolved', ?, ?, ?)",
              (ticket_id, date_str, time_str, log_detail))
    conn.commit()

    t_json = _fetch_ticket_full(ticket_id, conn)
    conn.close()
    return jsonify(t_json), 200

@app.route("/api/tickets/reroute", methods=["POST"])
# Note: Should be restricted to department staff securely
def reroute_ticket():
    data = request.json
    ticket_id = data.get("ticket_id")
    new_department = data.get("new_department")

    if not ticket_id or not new_department:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    c = conn.cursor()

    t_json = _fetch_ticket_full(ticket_id, conn)
    if not t_json:
        conn.close()
        return jsonify({"error": "Ticket not found"}), 404

    from_depts = ", ".join(t_json["currentDepartments"])

    # Mark current as not current
    c.execute("UPDATE ticket_departments SET is_current = 0 WHERE ticket_id = ?", (ticket_id,))

    # Insert new current department
    c.execute("INSERT INTO ticket_departments (ticket_id, department_name, is_current) VALUES (?, ?, 1)",
              (ticket_id, new_department))

    c.execute("UPDATE tickets SET status = 'Open' WHERE id = ?", (ticket_id,))

    date_str = _today()
    time_str = _now()
    log_detail = f"Rerouted from {from_depts} to {new_department}"

    c.execute("INSERT INTO ticket_logs (ticket_id, event, date, time, detail) VALUES (?, 'Rerouted', ?, ?, ?)",
              (ticket_id, date_str, time_str, log_detail))

    conn.commit()

    updated = _fetch_ticket_full(ticket_id, conn)
    conn.close()
    return jsonify(updated), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)