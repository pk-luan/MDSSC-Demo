from flask import Flask, jsonify, request, render_template, send_file
import os
from io import BytesIO
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
app = Flask(__name__)


# Get all books
@app.route('/convert', methods=['POST'])
def get_books():
    print(request.files)
    print(request.data)
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if file:
        svg_content = file.read()
        drawing = svg2rlg(BytesIO(svg_content))
        buffer = BytesIO()
        renderPM.drawToFile(drawing, buffer, fmt="PNG")
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="converted.png", mimetype="image/png")

    return "Error in conversion"  # Handle other errors if necessary



@app.route('/', methods=['GET'])
def frontend():
    return render_template('index.html')
    
# Run the flask App
if __name__ == '__main__':
    app.run(debug=True)