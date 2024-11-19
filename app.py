from flask import Flask, render_template, request, send_file
import pdfkit
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_form():
    return render_template('form.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Get form data
    data = request.form.to_dict()
    
    # Handle Sonar file upload
    if 'sonar_file' in request.files:
        sonar_file = request.files['sonar_file']
        if sonar_file.filename != '':
            filename = f"uploads/sonar_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{sonar_file.filename}"
            os.makedirs('uploads', exist_ok=True)
            sonar_file.save(filename)
            data['sonar_filename'] = sonar_file.filename
    
    # Generate PDF from template
    rendered_template = render_template('pdf_template.html', data=data)
    
    # Configure pdfkit options
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    
    # Generate PDF
    pdf_path = 'temp_pdf.pdf'
    pdfkit.from_string(rendered_template, pdf_path, options=options)
    
    # Send PDF file
    return send_file(pdf_path, as_attachment=True, download_name='report.pdf')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Handle form submission without generating PDF
    data = request.form.to_dict()
    # Add your form submission logic here
    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True) 