import os
import numpy as np
import cv2
from ultralytics import SAM
from ultralytics.utils.downloads import safe_download
from PIL import Image
from flask import render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from app import app

# Configurations
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
MODEL_DIR = os.path.join(app.root_path,'models')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER,exist_ok=True)
os.makedirs(MODEL_DIR,exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR,'mobile_sam.pt')
if not os.path.exists(MODEL_PATH):
    safe_download(url="https://github.com/ultralytics/assets/releases/download/v8.2.0/mobile_sam.pt", dir=MODEL_DIR)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = SAM(MODEL_PATH)

# File handling functions
def clear_uploads_folder():
    """
    Clear all files in the uploads folder
    """
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

def is_allowed_file(filename):
    """
    Checking if a file has an allowed extension
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, filename):
    """
    Save the uploaded file to the uploads folder and return the file path.
    """
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return file_path

def generate_preview(x, y, filename):
    """
    Generate a preview of the selected region of interest using SAM.
    Returns the preview image path or None if unsuccessful.
    """
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = cv2.imread(image_path)
    if image is None:
        return None

    x_int = int(round(x))
    y_int = int(round(y))

    results = model.predict(source=image_path, points=[x_int, y_int], labels=[1], verbose=False)

    if not results or not results[0].masks or len(results[0].masks) == 0:
        return None

    try:
        mask = results[0].masks.data[0].cpu().numpy()
    except (IndexError, AttributeError):
        return None

    mask = (mask < 0.5).astype(np.uint8) * 255

    h, w = image.shape[:2]
    if mask.shape != (h, w):
        mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)

    overlay = np.zeros_like(image, dtype=np.uint8)
    overlay[mask == 255] = (0, 0, 255)  # Red color

    alpha = 0.5
    preview_image = cv2.addWeighted(image, 1 - alpha, overlay, alpha, 0.0)

    preview_image_path = "preview_" + filename
    preview_path = os.path.join(app.config['UPLOAD_FOLDER'], preview_image_path)
    cv2.imwrite(preview_path, preview_image)

    return preview_image_path

def generate_segment(x, y, filename):
    """
    Segment the original image for the final result using SAM.
    Returns the original filename and segmented filename with alpha channel, or (filename, None) if unsuccessful.
    """
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    if image is None:
        return filename, None

    x_int = int(round(x))
    y_int = int(round(y))

    results = model.predict(source=image_path, points=[x_int, y_int], labels=[1], verbose=False)

    if not results or not results[0].masks or len(results[0].masks) == 0:
        return filename, None

    try:
        mask = results[0].masks.data[0].cpu().numpy()
    except (IndexError, AttributeError):
        return filename, None

    mask = (mask < 0.5).astype(np.uint8) * 255

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgba = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2RGBA)
    image_rgba[:, :, 3] = mask  # Set alpha channel

    segmented_filename = "segmented_" + filename
    segmented_path = os.path.join(app.config['UPLOAD_FOLDER'], segmented_filename)
    cv2.imwrite(segmented_path, image_rgba)

    return filename, segmented_filename

# Flask Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    # Clear the uploads folder when showing the upload card
    if request.method == 'GET':
        clear_uploads_folder()

    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('main.html', error="No file part")
        file = request.files['file']
        if file.filename == '':
            return render_template('main.html', error="No selected file")
        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_file(file, filename)
            return render_template('main.html', uploaded_file=filename)
    return render_template('main.html')

@app.route('/preview', methods=['POST'])
def preview():
    x = request.form.get('x', '')
    y = request.form.get('y', '')
    filename = request.form.get('filename', '')
    if not x or not y or not filename:
        return render_template('main.html', uploaded_file=filename, error="Please select a region on the image")
    try:
        x = float(x)
        y = float(y)
    except ValueError:
        return render_template('main.html', uploaded_file=filename, error="Invalid coordinates")
    
    preview_file = generate_preview(x, y, filename)
    if preview_file is None:
        return render_template('main.html',uploaded_file=filename,error="There is no object in the selected region")

    return render_template('main.html', uploaded_file=filename, preview_file=preview_file, x_coord=x, y_coord=y)

@app.route('/segment', methods=['POST'])
def segment():
    x = request.form.get('x', '')
    y = request.form.get('y', '')
    filename = request.form.get('filename', '')

    if not x or not y or not filename:
        return render_template('main.html', uploaded_file=filename, error="Please select a region on the image")

    try:
        x = float(x)
        y = float(y)
    except ValueError:
        return render_template('main.html', uploaded_file=filename, error="Invalid coordinates")

    uploaded_file, result_file = generate_segment(x, y, filename)
    
    return render_template('main.html', uploaded_file=uploaded_file, result_file=result_file)

@app.route('/reset', methods=['GET'])
def reset():
    # Clear the uploads folder before returning to the upload phase
    clear_uploads_folder()
    return redirect(url_for('index'))

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/about')
def about_page():
    return render_template('about.html')