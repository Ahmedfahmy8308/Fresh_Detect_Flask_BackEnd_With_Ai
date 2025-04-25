import os
import uuid
from datetime import datetime
from app.db import db
from app.services.predict_service import PredictService

predict_service = PredictService()

def save_image(file, device_ID):
    image_ID = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    upload_folder = 'static/uploads'
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, f"{image_ID}_{file.filename}")
    file.save(file_path)

    predicted_class, quality_score, error_flag = predict_image(file_path)

    class_folder = os.path.join('static/images', predicted_class)
    os.makedirs(class_folder, exist_ok=True)
    final_path = os.path.join(class_folder, os.path.basename(file_path))
    os.rename(file_path, final_path)

    db.images.insert_one({
        "image_ID": image_ID,
        "device_ID": device_ID,
        "timestamp": timestamp,
        "path": final_path
    })

    db.results.insert_one({
        "result_ID": str(uuid.uuid4()),
        "image_ID": image_ID,
        "quality_score": quality_score,
        "error_flag": error_flag,
        "predicted_class": predicted_class
    })

    return {
        "image_ID": image_ID,
        "path": final_path
    }, {
        "predicted_class": predicted_class,
        "quality_score": quality_score,
        "error_flag": error_flag
    }

def predict_image(image_path):
    try:
        prediction = predict_service.predict(image_path)
        return prediction, 0.95, 0 
    except Exception as e:
        return "Error", 0, 1