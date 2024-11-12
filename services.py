from validator import validate_receipt
from calculator import calculate_points
import uuid
from threading import Lock
from flask import jsonify, abort
import hashlib, logging, json

# In-memory storage and lock
receipts = {}
receipts_lock = Lock()

# =====functions for the business logic=======
# validation of receipt
def process_receipt_service(request):
    data = request.get_json()
    if not data:
        abort(400, description="The receipt is invalid.")

    # Validate and process receipt
    try:
        validate_receipt(data)
    except ValueError as e:
        abort(400, description=str(e))

    # unique id
    receipt_str = json.dumps(data, sort_keys=True)
    receipt_id = hashlib.sha256(receipt_str.encode()).hexdigest()[:16]
    if receipt_id in receipts:
        abort(400, description="Duplicated receipt.")

    # storage
    points = calculate_points(data)
    with receipts_lock:
        receipts[receipt_id] = {'receipt': data, 'points': points}

    logging.info(f"Processed receipt with ID: {receipt_id}")

    return jsonify({"id": receipt_id}), 200


# getting the points
def get_points_service(receipt_id):
    with receipts_lock:
        receipt_entry = receipts.get(receipt_id)

    if not receipt_entry:
        abort(404, description="Receipt not found for that ID.")

    points = receipt_entry['points']
    logging.info(f"Retrieved points for receipt ID: {receipt_id}")

    return jsonify({"points": points}), 200
