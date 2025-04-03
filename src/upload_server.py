from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, 
            static_folder='.',
            template_folder='_layouts')

# Configure upload folder
UPLOAD_FOLDER = 'converter_markdown/input_folder_markdown'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'md'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/drag-drop')
def upload_page():
    return render_template('drag_drop_upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False, 
                'error': 'Error: No file part in the request',
                'details': 'The request did not contain a file part. This might be due to incorrect form submission.'
            })
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False, 
                'error': 'Error: No file selected',
                'details': 'The file name is empty. Please select a file to upload.'
            })
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False, 
                'error': 'Error: Invalid file type',
                'details': f'File type not allowed. Only .md files are accepted. Received: {file.filename}'
            })
        
        # Secure the filename and create the full path
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Check if file already exists
        if os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': 'Error: File already exists',
                'details': f'A file with the name {filename} already exists in {UPLOAD_FOLDER}'
            })
        
        # Save the file
        file.save(file_path)
        
        # Verify the file was saved
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            return jsonify({
                'success': True, 
                'filename': filename,
                'message': f'File saved successfully to {UPLOAD_FOLDER}',
                'details': {
                    'path': file_path,
                    'size': f'{file_size} bytes'
                }
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'Error: File save verification failed',
                'details': f'File was not found at the expected location: {file_path}'
            })
            
    except PermissionError as e:
        return jsonify({
            'success': False,
            'error': 'Error: Permission denied',
            'details': f'Cannot write to {UPLOAD_FOLDER}. Check folder permissions: {str(e)}'
        })
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': 'Error: Unexpected error during upload',
            'details': f'Error type: {type(e).__name__}, Message: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True) 