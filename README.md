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
- [Testing](#testing)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [License](#license)
- [Contribution Guidelines](#contribution-guidelines)
- [Future Improvements / Limitations](#future-improvements--limitations)
- [Contact](#contact)

---

## Project Overview

**FreshDetect** is a comprehensive backend system built with Flask and powered by a deep learning model (ResNet18) to classify fruits and vegetables as fresh or rotten from images. The system allows device registration, image uploads, AI-based analysis, user voice feedback collection, and provides an admin dashboard for monitoring, with all data stored in MongoDB.

**Project Objectives:**

- Automate and accelerate the process of assessing the quality of agricultural products.
- Provide a robust API that can be integrated with mobile applications or other systems.
- Enable administrators to monitor devices, results, and analyze data efficiently.

---

## System Architecture

- **Flask Web Server:** Handles API requests and admin dashboard.
- **MongoDB:** Stores all data (devices, images, results, feedback, admins).
- **AI Model (PyTorch):** Loads a pre-trained model for image analysis.
- **Blueprints:** Organizes code into modules (routes/controllers).
- **Services Layer:** Business logic (image saving, prediction, data management).
- **Templates:** HTML templates for the admin dashboard.

**Simplified Architecture Diagram:**

```
[Device/Mobile] --API--> [Flask Backend] --AI--> [Prediction]
                                   |                |
                                   v                v
                              [MongoDB]        [Admin Dashboard]
```

---

## Technologies Used

- **Flask**: Web framework for Python
- **Flasgger**: Swagger/OpenAPI documentation
- **PyTorch**: Deep learning framework
- **Torchvision**: Image transformations
- **Pillow**: Image processing
- **MongoDB**: NoSQL database
- **pymongo**: MongoDB driver
- **Jinja2**: HTML templating
- **gunicorn**: Production WSGI server
- **Werkzeug**: WSGI utilities

---

## Installation Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ahmedfahmy8308/Fresh_Detect_Flask_BackEnd_With_Ai.git
   cd Fresh_Detect_Flask_BackEnd_With_Ai
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
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

## Testing

- **Unit Tests:**
  - You can add tests using `pytest` or `unittest` to ensure code quality.
- **Manual Testing:**
  - Try uploading different images using Postman or any API tool and check the results in the dashboard.

---

## Troubleshooting & FAQ

- **MongoDB Connection Error:**
  - Make sure MongoDB service is running on your machine (`localhost:27017`).
- **Model Not Found:**
  - Ensure `best_model.pth` exists in the `Model/` directory.
- **Image Upload Issues:**
  - Make sure images are in a supported format (JPEG/PNG) and of reasonable size.

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
- **Multi-language Support:** Add Arabic and other language support for the dashboard and user interface.
- **User Experience:** Add notifications and alerts for admins.

---

## Contact

For any questions or support, contact: [ahmedfahmy@ieee.org](mailto:ahmedfahmy@ieee.org)

---

> This project was developed as a graduation project at the Faculty of Computer and Information, Domyat University, aiming to support digital transformation in the agricultural sector using artificial intelligence.
