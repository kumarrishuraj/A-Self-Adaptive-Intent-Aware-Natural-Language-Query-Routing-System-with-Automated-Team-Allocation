tickets = []
ticket_counter = 1


def create_ticket(name, reg_no, query, departments):

    global ticket_counter

    ticket = {
        "ticket_id": ticket_counter,
        "name": name,
        "reg_no": reg_no,
        "query": query,
        "departments": departments,
        "status": "open"
    }

    tickets.append(ticket)

    ticket_counter += 1

    return ticket


def get_tickets(department):

    result = []

    for ticket in tickets:
        if department in ticket["departments"]:
            result.append(ticket)

    return result


def resolve_ticket(ticket_id):

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            ticket["status"] = "resolved"
            return ticket

    return None