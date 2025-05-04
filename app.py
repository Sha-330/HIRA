from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2 as cv
from mri import StrokeDetector
from blood import extract_text_from_pdf, parse_blood_test_results
from ct_scan import predict_image as predict_ct
from xray import predict_image as predict_xray
from keras.models import load_model

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load model and labels from HIRA/models directory
MODEL_DIR = r"Path\to\the\models\folder"
MRI_MODEL_PATH = os.path.join(MODEL_DIR, "stroke.h5")
MRI_LABELS_PATH = os.path.join(MODEL_DIR, "stroke_labels.txt")
CT_MODEL_PATH = os.path.join(MODEL_DIR, "ct.h5")
CT_LABELS_PATH = os.path.join(MODEL_DIR, "ct.txt")
XRAY_MODEL_PATH = os.path.join(MODEL_DIR, "xray.h5")
XRAY_LABELS_PATH = os.path.join(MODEL_DIR, "xray.txt")

ct_model = load_model(CT_MODEL_PATH, compile=False)
xray_model = load_model(XRAY_MODEL_PATH, compile=False)

# Load class labels
def load_labels(label_path):
    with open(label_path, "r") as f:
        return [line.strip() for line in f.readlines()]

ct_labels = load_labels(CT_LABELS_PATH)
xray_labels = load_labels(XRAY_LABELS_PATH)

def predict_ct_scan(image_path):
    img = cv.imread(image_path)
    if img is None:
        return "Error", 0.0
    img = cv.resize(img, (224, 224))
    img = img.astype("float32") / 127.5 - 1
    img = img.reshape(1, 224, 224, 3)
    prediction = ct_model.predict(img)
    index = prediction.argmax()
    return ct_labels[index], prediction[0][index]

def predict_xray_image(image_path):
    img = cv.imread(image_path)
    if img is None:
        return "Error", 0.0
    img = cv.resize(img, (224, 224))
    img = img.astype("float32") / 127.5 - 1
    img = img.reshape(1, 224, 224, 3)
    prediction = xray_model.predict(img)
    index = prediction.argmax()
    return xray_labels[index], prediction[0][index]

def process_image(image_path):
    """Process the uploaded image and return results."""
    img = cv.imread(image_path)
    if img is None:
        return None, "Error: Unable to read image file."
    
    detector = StrokeDetector()
    class_name, confidence_score = detector.predict(image_path)
    
    result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.png')
    cv.imwrite(result_image_path, img)
    return (class_name, confidence_score), result_image_path

def process_blood_test(pdf_path):
    """Extracts and parses blood test results from a PDF."""
    text = extract_text_from_pdf(pdf_path)
    results = parse_blood_test_results(text)
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "password":  # Simple auth check
            return redirect(url_for('upload'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file_type = request.form['fileType']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        if file_type == 'MRI':
            results, result_image = process_image(file_path)
            return render_template('result.html', results=results, file_type=file_type, result_image=result_image)
        elif file_type == 'Blood':
            results = process_blood_test(file_path)
            return render_template('result.html', results=results, file_type=file_type)
        elif file_type == 'CT-Scan':
            class_name, confidence_score = predict_ct_scan(file_path)
            return render_template('result.html', results=(class_name, confidence_score), file_type=file_type)
        elif file_type == 'X-Ray':
            class_name, confidence_score = predict_xray_image(file_path)
            return render_template('result.html', results=(class_name, confidence_score), file_type=file_type)
    return render_template('upload.html')

@app.route('/results')
def results():
    return render_template('result.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
