import sales_logger
import morning_report


def _validate_sale(service, quantity, price):
    if not service:
        return "service is required"
    if quantity <= 0:
        return "quantity must be greater than 0"
    if price < 0:
        return "price must be greater than or equal to 0"
    if quantity > 500:
        return "quantity too large"
    return None


def log_sale(service, quantity, price):
    err = _validate_sale(service, quantity, price)

    if err:
        return {
            "ok": False,
            "tool": "log_sale",
            "error": err,
        }

    sales_logger.log_sale(service, quantity, price)

    return {
        "ok": True,
        "tool": "log_sale",
        "message": "car care service sale logged successfully",
        "service": service,
        "quantity": quantity,
        "price": price,
        "total": quantity * price,
    }


def get_yesterday_summary():
    report = morning_report.create_report()

    return {
        "ok": True,
        "tool": "get_yesterday_summary",
        "report": report,
    }


TOOL_REGISTRY = {
    "log_sale": {
        "fn": log_sale,
        "args": ("service", "quantity", "price"),
        "coerce": {
            "service": str,
            "quantity": int,
            "price": float,
        },
    },
    "get_yesterday_summary": {
        "fn": get_yesterday_summary,
        "args": (),
        "coerce": {},
    },
}