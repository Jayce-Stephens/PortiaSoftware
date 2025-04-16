from flask import Flask, request
import os
import pandas as pd

test_file = ''

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Welcome to the file upload service!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # Save the uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        # Process the file
        try:
            df = pd.read_csv(filepath)
            html_table = df.to_html(classes='data', header="true")
            return f'<h2>File uploaded successfully!</h2>{html_table}'
        except Exception as e:
            return f'<p>Error reading CSV: {str(e)}</p>', 500
if __name__ == '__main__':
    app.run(debug=True)