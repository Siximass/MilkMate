import sales_logger
import morning_report


def _validate_sale(menu, quantity, price):
    if not menu:
        return "menu is required"
    if quantity <= 0:
        return "quantity must be greater than 0"
    if price < 0:
        return "price must be greater than or equal to 0"
    if quantity > 500:
        return "quantity too large"
    return None


def log_sale(menu, quantity, price):
    err = _validate_sale(menu, quantity, price)

    if err:
        return {
            "ok": False,
            "tool": "log_sale",
            "error": err,
        }

    sales_logger.log_sale(menu, quantity, price)

    return {
        "ok": True,
        "tool": "log_sale",
        "message": "sale logged successfully",
        "menu": menu,
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
        "args": ("menu", "quantity", "price"),
        "coerce": {
            "menu": str,
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