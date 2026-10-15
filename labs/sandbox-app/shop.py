"""Tiny shopping helpers used by the GH-600 labs."""


def parse_price(text: str) -> float:
    """Parse a price like '$1,234.50' into a float."""
    return float(text.replace("$", ""))  # BUG (seeded): fails on thousands separators


def apply_discount(price: float, percent: float) -> float:
    """Return price after a percent discount."""
    return price - price * percent / 100


def total(prices: list[float]) -> float:
    return sum(prices)


def average(prices: list[float]) -> float:
    return sum(prices) / len(prices)  # BUG (seeded): ZeroDivisionError on empty list
