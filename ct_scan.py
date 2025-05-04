from keras.models import load_model  
import cv2  
import numpy as np  
import os  

# Set the correct path to the model  
MODEL_DIR = r"path\to\the\model-folder"  
CT_MODEL_PATH = os.path.join(MODEL_DIR, "ct.h5")  
LABELS_PATH = os.path.join(MODEL_DIR, "ct.txt")  

# Load the model  
model = load_model(CT_MODEL_PATH, compile=False)  

# Load class labels  
with open(LABELS_PATH, "r") as f:  
    class_names = [line.strip() for line in f.readlines()]  

def predict_image(image_path):  
    """Predicts the class of the given CT scan image."""  
    image = cv2.imread(image_path)  
    if image is None:  
        print("Error: Unable to read image. Check the file path.")  
        return "Error", 0.0  

    # Resize and normalize the image  
    image = cv2.resize(image, (224, 224))  
    image = image.astype("float32") / 127.5 - 1  
    image = image.reshape(1, 224, 224, 3)  

    # Predict using the model  
    prediction = model.predict(image)  
    index = np.argmax(prediction)  
    class_name = class_names[index]  
    confidence_score = prediction[0][index]  

    return class_name, confidence_score  
