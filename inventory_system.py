"""
inventory_system.py

Simple, educational inventory management functions used in static code
analysis exercises. This module intentionally contains simplified and unsafe
patterns (mutable default arguments, eval usage, bare except) for teaching
purposes — do not use as-is in production.
"""

import json
import logging
from datetime import datetime

# Global variable
stock_data = {}

def addItem(item="default", qty=0, logs=None):
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
        logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))

def removeItem(item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except:
        pass

def getQty(item):
    return stock_data[item]

def loadData(file="inventory.json"):
    f = open(file, "r")
    global stock_data
    stock_data = json.loads(f.read())
    f.close()

def saveData(file="inventory.json"):
    f = open(file, "w")
    f.write(json.dumps(stock_data))
    f.close()

def printData():
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def checkLowItems(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid types, no check
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    eval("print('eval used')")  # dangerous

main()
