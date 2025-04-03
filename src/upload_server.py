from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'converter_markdown/input_folder'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure static folder for layouts
LAYOUTS_FOLDER = '_layouts'

@app.route('/')
def index():
    return send_from_directory(LAYOUTS_FOLDER, 'default.html')

@app.route('/drag_drop_upload.html')
def upload_page():
    return send_from_directory(LAYOUTS_FOLDER, 'drag_drop_upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return jsonify({'success': True, 'filename': filename})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 