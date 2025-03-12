from flask import Flask, jsonify, send_from_directory, render_template
from services.data_processing import process_all_agencies_and_chapters  # Ensure correct import

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

if __name__ == '__main__':
    app.run(debug=True)
