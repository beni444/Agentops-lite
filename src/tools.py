ORDERS = {
    "1001": {"status": "delayed", "days_late": 5},
    "1002": {"status": "delivered", "days_late": 0},
}

def get_order_status(order_id):
    return ORDERS.get(order_id, {"error": "not_found"})

def issue_refund(order_id):
    return {"order_id": order_id, "refund": "approved"}

def create_ticket(issue):
    return {"ticket_id": "INC12345", "status": "created", "issue": issue}


TOOLS = {
    "get_order_status": get_order_status,
    "issue_refund": issue_refund,
    "create_ticket": create_ticket,
}
