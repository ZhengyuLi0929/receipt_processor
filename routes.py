from flask import request, jsonify, abort
from services import process_receipt_service, get_points_service

def init_routes(app):
    @app.route('/receipts/process', methods=['POST'])
    def process_receipt():
        return process_receipt_service(request)

    @app.route('/receipts/<receipt_id>/points', methods=['GET'])
    def get_points(receipt_id):
        return get_points_service(receipt_id)
