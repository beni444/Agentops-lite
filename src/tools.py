import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "mock_crm.json"

with open(DATA_PATH, "r") as file:
    CRM_DATA = json.load(file)

ORDERS = {order["id"]: order for order in CRM_DATA["orders"]}


def get_order_status(order_id):
    order = ORDERS.get(order_id)

    if not order:
        return {"error": "order_not_found"}

    return {
        "order_id": order_id,
        "status": order["status"],
        "days_late": order.get("days_late", 0),
    }


def check_refund_eligibility(order_id):
    order = ORDERS.get(order_id)

    if not order:
        return {"eligible": False, "reason": "order_not_found"}

    return {
        "order_id": order_id,
        "eligible": order.get("refund_eligible", False),
        "reason": "delivery_delay" if order.get("days_late", 0) > 3 else "policy_not_met",
    }


def check_return_eligibility(order_id):
    order = ORDERS.get(order_id)

    if not order:
        return {"eligible": False, "reason": "order_not_found"}

    return {
        "order_id": order_id,
        "eligible": order.get("return_eligible", False),
        "return_window_days": 30 if order.get("return_eligible", False) else 0,
    }


def issue_refund(order_id):
    return {
        "order_id": order_id,
        "refund": "approved",
    }


def create_ticket(issue):
    return {
        "ticket_id": "INC12345",
        "status": "created",
        "issue": issue,
    }


TOOLS = {
    "get_order_status": get_order_status,
    "check_refund_eligibility": check_refund_eligibility,
    "check_return_eligibility": check_return_eligibility,
    "issue_refund": issue_refund,
    "create_ticket": create_ticket,
}