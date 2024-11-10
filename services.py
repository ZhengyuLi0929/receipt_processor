from validator import validate_receipt
from calculator import calculate_points
import uuid
from threading import Lock
from flask import jsonify, abort
import logging

# In-memory storage
receipts = {}
receipts_lock = Lock()

def process_receipt_service(request):
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON payload.")

    # Validate and process receipt
    try:
        validate_receipt(data)
    except ValueError as e:
        abort(400, description=str(e))

    points = calculate_points(data)
    receipt_id = str(uuid.uuid4())

    with receipts_lock:
        receipts[receipt_id] = {'receipt': data, 'points': points}

    logging.info(f"Processed receipt with ID: {receipt_id}")

    return jsonify({"id": receipt_id}), 200

def get_points_service(receipt_id):
    with receipts_lock:
        receipt_entry = receipts.get(receipt_id)

    if not receipt_entry:
        abort(404, description="Receipt not found.")

    points = receipt_entry['points']
    logging.info(f"Retrieved points for receipt ID: {receipt_id}")

    return jsonify({"points": points}), 200
