from flask import Flask, request, jsonify
import os
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TMP_DIR = os.path.join(os.getcwd(), 'tmp')
os.makedirs(TMP_DIR, exist_ok=True)

def convert_docx_to_pdf(input_file, output_file):
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    libreoffice_path = r'C:\Program Files\LibreOffice\program\soffice.exe'

    command = [
        libreoffice_path,
        '--headless',
        '--convert-to', 'pdf',
        input_file,
        '--outdir', output_dir
    ]

    print("Running command:", " ".join(command))

    result = subprocess.run(command, capture_output=True, text=True)

    print("Command output:", result.stdout)
    print("Command error:", result.stderr)

    if result.returncode != 0:
        raise Exception(f"Command failed with error: {result.stderr}")

    return output_file

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    print('Received file:', file.filename)

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    input_file_path = os.path.join(TMP_DIR, file.filename)
    output_file_path = os.path.join(TMP_DIR, file.filename.rsplit('.', 1)[0] + '.pdf')

    file.save(input_file_path)
    
    print("Files in tmp directory:", os.listdir(TMP_DIR))

    try:
        pdf_file_path = convert_docx_to_pdf(input_file_path, output_file_path)

        if os.path.exists(pdf_file_path):
            print("PDF successfully created at:", pdf_file_path)
            return jsonify({'message': 'File converted successfully', 'pdf_file': pdf_file_path}), 200
        else:
            print("PDF file not created.")
            return jsonify({'error': 'PDF conversion failed, file not found.'}), 500

    except Exception as e:
        print(f"Error during conversion: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(input_file_path):
            os.remove(input_file_path)

if __name__ == '__main__':
    app.run(debug=True)
