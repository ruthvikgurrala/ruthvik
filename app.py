from flask import Flask, request, jsonify, send_from_directory,render_template
import cv2
import numpy as np
import os
import uuid

app = Flask(__name__)

uploads_folder = 'uploads'
os.makedirs(uploads_folder, exist_ok=True)

def generate_unique_filename(extension='.jpg'):
    return str(uuid.uuid4()) + extension

def apply_low_light(image_path):
    # Load the image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    print("at apply_noise")
    if img is None:
        print("Error: Image not found.")
        return
    

    # Convert image to LAB color space
    lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Split LAB image into L, A, and B channels
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) on L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_l_channel = clahe.apply(l_channel)

    # Merge the enhanced L channel with A and B channels
    enhanced_lab_image = cv2.merge((enhanced_l_channel, a_channel, b_channel))

    # Convert back to BGR color space
    enhanced_bgr_image = cv2.cvtColor(enhanced_lab_image, cv2.COLOR_LAB2BGR)

    unique_filename = str(uuid.uuid4()) + '.jpg'
    uploaded_image_path = os.path.join(uploads_folder, unique_filename)

    cv2.imwrite(uploaded_image_path, img)

    processed_filename = generate_unique_filename('_lowlight.jpg')
    processed_image_path = os.path.join(uploads_folder, processed_filename)
    cv2.imwrite(processed_image_path, enhanced_bgr_image)
    return processed_image_path


def apply_noise(image_path):
    img = cv2.imread(image_path)
    print("at apply_noise")
    if img is None:
        print("Error: Image not found.")
        return
    
    dst = cv2.fastNlMeansDenoising(img, None, 15, 7, 21 )

    unique_filename = str(uuid.uuid4()) + '.jpg'
    uploaded_image_path = os.path.join(uploads_folder, unique_filename)

    cv2.imwrite(uploaded_image_path, img)

    processed_filename = generate_unique_filename('_noise.jpg')
    processed_image_path = os.path.join(uploads_folder, processed_filename)
    cv2.imwrite(processed_image_path, dst)
    return processed_image_path

    
def apply_gaussharp(image_path, blur_strength, sharpness_factor1,sharpness_factor2):
    img = cv2.imread(image_path)
    print("at apply_gaussharp")
    if img is None:
        print("Error: Image not found.")
        return
    
    
    blur_strength = max(0, min(blur_strength, 20))  # Ensure blur_strength is within [0, 20]
    ksize = int(blur_strength * 3) * 2 + 1  # Calculate odd kernel size based on blur_strength

    gaus = cv2.GaussianBlur(img, (ksize, ksize), blur_strength)
    sharp = cv2.addWeighted(img, sharpness_factor1, gaus, -sharpness_factor2, 3)
    
    print(f"the sharpness_factor process is completed")

    unique_filename = str(uuid.uuid4()) + '.jpg'
    uploaded_image_path = os.path.join(uploads_folder, unique_filename)

    cv2.imwrite(uploaded_image_path, img)

    processed_filename = generate_unique_filename('_sharp.jpg')
    processed_image_path = os.path.join(uploads_folder, processed_filename)
    cv2.imwrite(processed_image_path, sharp)
    return processed_image_path

def apply_gaussian_blur(image_path,blur_strength):
    img = cv2.imread(image_path)
    print(f"at gaussian_blur image is read with variable{blur_strength}")
    if img is None:
        print("img is None")
        return None

    blur_strength = max(0, min(blur_strength, 20))  # Ensure blur_strength is within [0, 20]
    ksize = int(blur_strength * 3) * 2 + 1  # Calculate odd kernel size based on blur_strength

    gaus = cv2.GaussianBlur(img, (ksize, ksize), blur_strength)

    # Generate a unique filename for the uploaded image
    unique_filename = str(uuid.uuid4()) + '.jpg'
    uploaded_image_path = os.path.join(uploads_folder, unique_filename)

    # Save the uploaded image
    cv2.imwrite(uploaded_image_path, img)

    # Save the processed image and return its path
    processed_image_path = os.path.join(uploads_folder, f'processed_{unique_filename}')
    cv2.imwrite(processed_image_path, gaus)
    return processed_image_path

@app.route('/apply_low_light', methods=['POST'])
def apply_low_light_endpoint():
    try:
        print("at apply_low_light_endpoint try block")
        image = request.files['image']
        if image.filename == '':
            print("at image.filename== '' ")
            return jsonify({"error": "No selected image"}), 400

        image_path = os.path.join(uploads_folder, image.filename)
        print(image_path)
        image.save(image_path)

        processed_image_path = apply_low_light(image_path)
        print("at processed_image_path = apply_low_light(image_path) -- in apply noise end point")
        if processed_image_path is None:
            print("processed_image_path is none")
            return jsonify({"error": "Image not found"}), 404

        return jsonify({"message": "Success", "processed_image_path": processed_image_path})
    except Exception as e:
        print("at apply_noise_endpoint except block")
        print(str(e)) 
        return jsonify({"error": str(e)}), 500

@app.route('/apply_noise', methods=['POST'])
def apply_noise_endpoint():
    try:
        print("at apply_noise_endpoint try block")
        image = request.files['image']
        if image.filename == '':
            print("at image.filename== '' ")
            return jsonify({"error": "No selected image"}), 400

        image_path = os.path.join(uploads_folder, image.filename)
        print(image_path)
        image.save(image_path)

        processed_image_path = apply_noise(image_path)
        print("at processed_image_path = apply_noise(image_path) -- in apply noise end point")
        if processed_image_path is None:
            print("processed_image_path is none")
            return jsonify({"error": "Image not found"}), 404

        return jsonify({"message": "Success", "processed_image_path": processed_image_path})
    except Exception as e:
        print("at apply_noise_endpoint except block")
        print(str(e)) 
        return jsonify({"error": str(e)}), 500

@app.route('/apply_gaussharp', methods=['POST'])
def apply_gaussharp_endpoint():
    try:
        print("at apply_gaussharp_endpoint try block")
        image = request.files['image']
        if image.filename == '':
            print("at image.filename== '' ")
            return jsonify({"error": "No selected image"}), 400

        image_path = os.path.join(uploads_folder, image.filename)
        print(image_path)
        image.save(image_path)

        blur_strength = float(request.form.get('blur_strength',0.5))
        sharpness_factor1 = float(request.form.get('sharpnesss_factor',1.5))
        sharpness_factor2=sharpness_factor1-1
        print(f"blur strength is{blur_strength},sharpness factor1 is {sharpness_factor1},sharpness factor2 is {sharpness_factor2}")
        
        processed_image_path = apply_gaussharp(image_path, blur_strength, sharpness_factor1,sharpness_factor2)
        print("at processed_image_path = apply_gaussharp(image_path) -- in apply gaussion sharp end point")
        if processed_image_path is None:
            print("processed_image_path is none")
            return jsonify({"error": "Image not found"}), 404

        return jsonify({"message": "Success", "processed_image_path": processed_image_path})

    except Exception as e:
        print("at apply_gaussian_blur_endpoint except block")
        print(str(e)) 
        return jsonify({"error": str(e)}), 500

@app.route('/apply_gaussian_blur', methods=['POST'])
def apply_gaussian_blur_endpoint():
    try:
        print("at apply_gaussian_blur_endpoint try block")
        image = request.files['image']
        if image.filename == '':
            print("at image.filename== '' ")
            return jsonify({"error": "No selected image"}), 400

        image_path = os.path.join(uploads_folder, image.filename)
        print(image_path)
        image.save(image_path)

        blur_strength = float(request.form.get('blur_strength', 0.5))  # Get blur strength from form data
        processed_image_path = apply_gaussian_blur(image_path,blur_strength)
        print("at processed_image_path = apply_gaussian_blur(image_path) -- in apply gaussion blur end point")
        if processed_image_path is None:
            print("processed_image_path is none")
            return jsonify({"error": "Image not found"}), 404

        return jsonify({"message": "Success", "processed_image_path": processed_image_path})

    except Exception as e:
        print("at apply_gaussian_blur_endpoint except block")
        print(str(e)) 
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print("at uploaded_file")
    return send_from_directory(uploads_folder, filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/')
def index():
    print("at index")
    return render_template('wp7.html')  # Rendering the Jinja template
@app.route('/wp.html')
def index2():
    print("at index2")
    return render_template('wp.html')
@app.route('/wp6.html')
def index3():
    print("at index3")
    return render_template('wp6.html')
if __name__ == '__main__':
    app.run(debug=True)
