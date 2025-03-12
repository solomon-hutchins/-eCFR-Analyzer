from flask import Blueprint, jsonify
from services.data_processing import process_all_agencies_and_chapters

graph_routes = Blueprint('graph_routes', __name__)

@graph_routes.route('/refresh_graph', methods=['GET'])
def refresh_graph():
    result = process_all_agencies_and_chapters("agencies_data.json")
    return jsonify({"message": result}), (200 if "successfully" in result else 500)
