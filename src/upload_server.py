from flask import Flask, request, jsonify, send_from_directory, render_template
import os

app = Flask(__name__, 
            static_folder='.',
            template_folder='_layouts')

# Configure upload folder
UPLOAD_FOLDER = 'converter_markdown/input_folder'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/upload')
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
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return jsonify({'success': True, 'filename': file.filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 