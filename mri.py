from keras.models import load_model  
import cv2  
import numpy as np  
import os  

# Set the correct path to the model  
MODEL_DIR = r"C:\Users\mazin\Downloads\HIRA\models"  
MRI_MODEL_PATH = os.path.join(MODEL_DIR, "stroke.h5")  
LABELS_PATH = os.path.join(MODEL_DIR, "stroke_labels.txt")  

class StrokeDetector:
    def __init__(self, model_path=MRI_MODEL_PATH):
        """Initialize the StrokeDetector with the pre-trained model."""
        self.model = load_model(model_path, compile=False)
        with open(LABELS_PATH, "r") as f:
            self.class_names = [line.strip() for line in f.readlines()]

    def predict(self, image_path):
        """Predicts the class of the given MRI scan image."""
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Unable to read image. Check the file path.")
            return "Error", 0.0

        # Resize and normalize the image  
        image = cv2.resize(image, (224, 224))  
        image = image.astype("float32") / 127.5 - 1  
        image = image.reshape(1, 224, 224, 3)  

        # Predict using the model  
        prediction = self.model.predict(image)  
        index = np.argmax(prediction)  
        class_name = self.class_names[index]  
        confidence_score = prediction[0][index]  

        return class_name, confidence_score