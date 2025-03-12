import requests
from flask import Flask, jsonify, send_from_directory, render_template, request
from services.data_processing import process_all_agencies_and_chapters  # Ensure correct import
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serves the frontend

@app.route('/word_counts.csv')
def serve_csv():
    return send_from_directory('.', 'word_counts.csv', as_attachment=False)

@app.route('/refresh_graph', methods=['GET'])
def refresh_graph():
    # Process the data and update CSV if necessary
    result = process_all_agencies_and_chapters("agencies_data.json")
    
    # After processing, serve the updated CSV file
    return send_from_directory('.', 'word_counts.csv', as_attachment=True)

@app.route('/fetch_word_count_over_time', methods=['GET'])
@app.route('/fetch_word_count_over_time', methods=['GET'])
def fetch_word_count_over_time():
    word = request.args.get('word')
    date = request.args.get('date')
    
    if not word or not date:
        return jsonify({"message": "Word and date are required!"}), 400

    # eCFR API query URL
    url = f"https://www.ecfr.gov/api/search/v1/results?query={word}&last_modified_after={date}&per_page=1000&page=1&order=newest_first&paginate_by=results"

    try:
        response = requests.get(url)
        data = response.json()

        if "results" not in data:
            return jsonify({"message": "No results found."}), 404

        # Process the results to extract date and word count from 'full_text_excerpt'
        time_data = []
        word_regex = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)  # Case-insensitive match for the word
        
        for item in data["results"]:
            # Ensure 'full_text_excerpt' and 'starts_on' exist before processing
            if "full_text_excerpt" in item and "starts_on" in item:
                excerpt = item["full_text_excerpt"]
                count = len(word_regex.findall(excerpt))  # Count occurrences of the word
                time_data.append({
                    "date": item["starts_on"],  # Use 'starts_on' as the date
                    "count": count
                })

        return jsonify(time_data), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
