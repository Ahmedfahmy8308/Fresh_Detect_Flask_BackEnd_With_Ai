# FreshDetect - AI-powered Fruit & Veggie Quality Scanner

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/) [![Flask](https://img.shields.io/badge/Flask-Backend-green?logo=flask)](https://flask.palletsprojects.com/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Installation Guide](#installation-guide)
- [Folder Structure](#folder-structure)
- [API Endpoints Documentation](#api-endpoints-documentation)
- [How the AI Model is Used](#how-the-ai-model-is-used)
- [Screenshots & Code Examples](#screenshots--code-examples)
- [License](#license)
- [Contribution Guidelines](#contribution-guidelines)
- [Future Improvements / Limitations](#future-improvements--limitations)

---

## Project Overview

**FreshDetect** is a Flask-based backend system that leverages deep learning (ResNet18) for real-time classification of fruits and vegetables as fresh or rotten. It provides a RESTful API for mobile clients, an admin dashboard for monitoring, and stores all metadata and results in MongoDB. The system supports device registration, image uploads, AI-powered predictions, feedback collection (voice messages), and comprehensive admin management.

---

## System Architecture

- **Flask Web Server**: Handles API requests, admin dashboard, and static file serving.
- **MongoDB**: Stores all persistent data (admins, devices, images, analysis results, feedback).
- **AI Model (PyTorch)**: Loads a pre-trained ResNet18 model for image classification.
- **Blueprints**: Modularizes routes for devices, images, feedback, and admin features.
- **Services Layer**: Encapsulates business logic (e.g., saving images, running predictions).
- **Templates**: Jinja2 HTML templates for the admin dashboard.

**High-Level Flow:**

1. Device registers via API.
2. Device uploads an image.
3. Image is saved, AI model predicts class/quality, results stored in DB.
4. Admins access dashboard to view/manage data and statistics.

---

## Technologies Used

- **Flask**: Web framework for Python.
- **Flasgger**: Swagger/OpenAPI documentation for Flask APIs.
- **PyTorch**: Deep learning framework for AI model inference.
- **Torchvision**: Image transformations and model utilities.
- **Pillow**: Image processing.
- **MongoDB**: NoSQL database.
- **pymongo**: MongoDB driver for Python.
- **Jinja2**: Templating engine for HTML.
- **gunicorn**: Production WSGI server.
- **Werkzeug**: WSGI utilities.

---

## Installation Guide

1. **Clone the repository:**

   ```bash
   git clone <https://github.com/Ahmedfahmy8308/Fresh_Detect_Flask_BackEnd_With_Ai>
   cd flask

   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Start MongoDB** (ensure it's running on `localhost:27017`).
6. **Run the application:**
   ```bash
   python main.py
   ```
7. **Access:**
   - Dashboard: [http://127.0.0.1:5000](http://127.0.0.1:5000)
   - API Docs: [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

---

## Folder Structure

```text
Fresh_Detect_Flask_BackEnd_With_Ai/
│
├── app/
│   ├── __init__.py                # App factory, default admin creation
│   ├── db.py                      # MongoDB connection
│   ├── routes.py                  # Registers all blueprints
│   ├── controllers/               # Route handlers (API & admin)
│   │   ├── device_controller.py
│   │   ├── image_controller.py
│   │   ├── feedback_controller.py
│   │   └── admin/                 # Admin dashboard controllers
│   ├── services/                  # Business logic (AI, DB ops)
│   │   ├── device_service.py
│   │   ├── image_service.py
│   │   ├── feedback_service.py
│   │   └── predict_service.py
│   ├── templates/                 # Jinja2 HTML templates
│   └── static/                    # Static files (CSS, uploads, images)
├── Model/                         # AI model weights
│   └── best_model.pth
├── main.py                        # App entry point
├── config.py                      # Configuration (DB URI, secret key)
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## API Endpoints Documentation

### Device Endpoints

- **POST `/api/register-device`**
  - Registers a new device.
  - **Body:**
    ```json
    { "device_model": "string", "device_type": "string" }
    ```
  - **Response:**
    ```json
    { "device_ID": "string" }
    ```

### Image Endpoints

- **POST `/api/upload-image`**
  - Uploads an image for prediction.
  - **Form Data:** `device_ID`, `image` (file)
  - **Response:**
    ```json
    { "image_ID": "...", "predicted_class": "...", "quality_score": ... }
    ```

### Feedback Endpoints

- **POST `/api/submit-feedback`**
  - Submits a voice message feedback.
  - **Form Data:** `device_ID`, `voice_message` (file)
  - **Response:**
    ```json
    { "feedback_ID": "..." }
    ```

### Admin Dashboard (Web)

- **GET /**: Dashboard overview (stats)
- **GET /admins**: List admins
- **POST /admins/add**: Add admin
- **GET/POST /admins/<admin_id>/edit**: Edit admin
- **GET /admins/<admin_id>/delete**: Delete admin
- **GET /devices**: List devices
- **GET /images**: List images
- **GET /analysis**: View analysis results
- **GET /feedbacks**: List feedbacks
- **GET /login, /logout**: Admin authentication

---

## How the AI Model is Used

### Model Loading

The AI model is loaded in `app/services/predict_service.py`:

```python
class PredictService:
    def __init__(self):
        self.model = self.load_model()
        ...
    def load_model(self):
        model = models.resnet18()
        model.load_state_dict(torch.load('Model/best_model.pth', map_location='cpu'))
        model.eval()
        return model
```

### Prediction Workflow

- When an image is uploaded via `/api/upload-image`, the file is saved and passed to the prediction service.
- The image is preprocessed (resized, normalized) and fed to the model.
- The model outputs a class label (e.g., "FreshMango") and a quality score.
- Results are stored in MongoDB and returned to the client.

**Example:**

```python
from app.services.image_service import save_image

def upload_image():
    ...
    result = save_image(file, device_ID)
    return jsonify(result)
```

---

## Screenshots & Code Examples

### Example: Device Registration

```python
@device_controller.route('/register-device', methods=['POST'])
def register_device():
    data = request.get_json()
    device_ID = insert_device(data['device_model'], data['device_type'])
    return jsonify({"device_ID": device_ID})
```

### Example: Admin Dashboard Template

```html
<!-- app/templates/dashboard.html -->
<p>Total Admins: {{ counts.admins }}</p>
<p>Total Devices: {{ counts.devices }}</p>
<p>Total Images: {{ counts.images }}</p>
<p>Average Quality Score: {{ avg_quality_score }}</p>
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contribution Guidelines

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear messages.
4. Push to your fork and submit a pull request.
5. For major changes, please open an issue first to discuss what you would like to change.

---

## Future Improvements / Limitations

- **Model Improvements:** Enhance AI accuracy with more data and advanced architectures.
- **Security:** Implement password hashing and stronger authentication for admins.
- **Scalability:** Add Docker support and production-ready deployment scripts.
- **Feedback Analysis:** Transcribe and analyze voice feedback.
- **User Roles:** Add more granular admin/user roles.
- **Frontend:** Build a dedicated frontend for end-users.

---

For any questions, contact [ahmedfahmy@ieee.org](mailto:ahmedfahmy@ieee.org).
