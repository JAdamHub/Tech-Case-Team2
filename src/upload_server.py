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

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/drag-drop')
def upload_page():
    return render_template('drag_drop_upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    
    try:
        # Secure the filename and create the full path
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save the file
        file.save(file_path)
        
        # Verify the file was saved
        if os.path.exists(file_path):
            return jsonify({
                'success': True, 
                'filename': filename,
                'message': f'File saved to {UPLOAD_FOLDER}'
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'File was not saved properly'
            })
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Error saving file: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True) 