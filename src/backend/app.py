import sys
import os
import logging
from logging.handlers import RotatingFileHandler

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../../frontend/dist')

log_file_path = os.path.join(os.path.dirname(__file__), 'app.log')
handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=3)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

app.logger.info('Flask application starting up...')

CORS(app)

try:
    from dashboard import render_dashboard
    app.logger.info('Successfully imported render_dashboard.')
except Exception as e:
    app.logger.critical(f'Failed during import or initial setup: {e}', exc_info=True)
    raise

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/dashboard', methods=['POST'])
def api_dashboard():
    app.logger.info('Received request for /api/dashboard')
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        app.logger.warning('Dashboard request failed: User not authenticated')
        return jsonify({'error': 'User not authenticated'}), 401
    
    app.logger.debug(f'Calling render_dashboard for user: {user_id}')
    response = render_dashboard(data, user_id)
    
    if 'error' in response:
        app.logger.error(f"Error processing dashboard request for user {user_id}: {response.get('error')}")
    
    return jsonify(response)

if __name__ == '__main__':
    from waitress import serve
    app.logger.info('Starting server with waitress on port 5002.')
    serve(app, host='127.0.0.1', port=5002)
