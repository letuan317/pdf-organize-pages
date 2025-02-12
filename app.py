from flask import Flask, request, send_file, render_template, jsonify
import fitz  # pymupdf
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure file upload
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def reorder_pdf_pages(input_pdf, output_pdf):
    """
    Reorders pages in a PDF file.

    :param input_pdf: Path to the input PDF file.
    :param output_pdf: Path to save the reordered PDF.
    """
    new_doc = fitz.open()
    doc = fitz.open(input_pdf)
    total_pages = len(doc)
    if total_pages % 2 != 0:
        print("Number of pages must be even.")
        return False
    i = 0
    j = len(doc)
    while True:
        new_doc.insert_pdf(doc, from_page=i, to_page=i)
        new_doc.insert_pdf(doc, from_page=j - 1, to_page=j - 1)
        i += 1
        j -= 1
        if i == j:
            break

    new_doc.save(output_pdf)
    new_doc.close()
    doc.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_pdf = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_pdf)

        # Generate output file name by adding '_reorder' to the original filename
        base_name, ext = os.path.splitext(filename)
        output_pdf = os.path.join(
            app.config['OUTPUT_FOLDER'], f"{base_name}_reorder{ext}")

        # Simulate progress
        for i in range(10):  # Simulated 10 steps of progress
            # In a real-world scenario, you'd update progress based on actual file processing.
            # Here we're just simulating it with a delay.
            pass

        # Reorder the PDF pages
        reorder_pdf_pages(input_pdf, output_pdf)

        return send_file(output_pdf, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
