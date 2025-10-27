"""
inventory_system.py

Simple, educational inventory management functions used in static code
analysis exercises. This module intentionally contains simplified and unsafe
patterns (mutable default arguments, eval usage, bare except) for teaching
purposes — do not use as-is in production.
"""

import json
from datetime import datetime

# Global variable


stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add qty of an item to the global inventory.

    Parameters:
        item: Item name to add. If falsy, the function returns without change.
        qty: Quantity to add (may be negative to subtract).
        logs: Optional list to append a human-readable log entry. If None,
            no log is recorded.

    Side effects:
        Mutates the module-level `stock_data` dictionary and appends to
        `logs` if a list is provided.

    Returns:
        None
    """
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    if logs is not None:
        logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """Remove ``qty`` of ``item`` from the inventory.

    If the item does not exist the function returns silently. If the
    resulting quantity is less than or equal to zero the item is removed
    from the store.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]

    except KeyError:
        # Item not present — nothing to remove
        pass


def get_qty(item):
    """Return the quantity for ``item`` or 0 if the item is missing."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory from a JSON file into the in-memory store.

    If the file does not exist the function does nothing. The existing
    ``stock_data`` dictionary is updated rather than rebound so external
    references keep working.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return

    if isinstance(data, dict):
        stock_data.clear()
        stock_data.update(data)


def save_data(file="inventory.json"):
    """Save the in-memory inventory to a JSON file using UTF-8."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, ensure_ascii=False, indent=2)


def print_data():
    """Print a simple inventory report to stdout."""
    print("Items Report")
    for i, q in stock_data.items():
        print(i, "->", q)


def check_low_items(threshold=5):
    """Return a list of items whose quantity is below ``threshold``."""
    result = []
    for i, q in stock_data.items():
        if q < threshold:
            result.append(i)
    return result


def main():
    """Run a short example demonstrating basic inventory operations."""
    add_item("apple", 10)
    add_item("banana", -2)
    # add_item(123, "ten")  # invalid types, no check (left commented)
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
