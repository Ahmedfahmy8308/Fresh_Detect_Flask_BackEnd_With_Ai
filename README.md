# 🥬 FreshDetect - AI-powered Fruit & Veggie Quality Scanner

**FreshDetect** is a Flask-based web API and admin dashboard that uses a deep learning model (ResNet18) to identify the type and freshness of fruits and vegetables. It enables real-time image classification, device tracking, feedback collection, and admin-level monitoring.

---

## 📌 Author

- **Name**: Ahmed Fahmy  
- **Email**: [ahmedfahmy@ieee.org](mailto:ahmedfahmy@ieee.org)

---

## 🚀 Features

### 🔍 Prediction System
- Upload an image via mobile app and get predictions like `FreshMango`, `RottenTomato`, etc.
- Images saved automatically in folders by prediction label.
- MongoDB stores:
  - Image metadata (device ID, upload time, unique ID, path).
  - Prediction results (image ID, predicted class, quality score, error flag).

### 📱 Device Management
- First-time app launch registers the device (model, type, time).
- Generates unique device ID and returns it for future API calls.

### 🗣️ Feedback Submission
- Submit voice message feedback from app.
- Stored in MongoDB with device ID, audio path, time, and admin reviewed flag.

### 📊 Admin Dashboard
- View statistics and manage:
  - Admin accounts
  - Registered devices
  - Uploaded images
  - Prediction results
  - Feedback submissions

---

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <https://github.com/Ahmedfahmy8308/Fresh_Detect_Flask_BackEnd_With_Ai>
   cd flask

2. Create a virtual environment:

   ```
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:

   ```
   python main.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000`. For Dashboard
   or go to `http://127.0.0.1:5000/apidocs` for Api

3. Upload an image to receive a prediction.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
