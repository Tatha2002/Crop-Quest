# 🌱 CropQuest

**CropQuest** is a machine learning-based agricultural web application built with **Django** that helps users make informed farming decisions through crop recommendation, crop yield prediction, and plant disease detection.

## 🚀 Features

### 🌾 Crop Recommendation

* Recommends the most suitable crop based on soil and environmental parameters.
* Uses a **machine learning classification model**.
* Parameters include nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall.

### 📊 Crop Yield Prediction

* Predicts expected crop yield based on agricultural and environmental parameters.
* Uses a **machine learning regression model**.

### 🍃 Plant Disease Prediction

* Detects plant diseases from uploaded plant images.
* Uses a **ResNet50 CNN model** trained using TensorFlow/Keras.
* Image preprocessing is performed before sending the image to the trained model.

### 🔐 Authentication & Security

* Implemented **JWT-based authentication**.
* Supports secure user registration and login.
* Protected API endpoints using JWT authentication.

### 🔌 REST APIs

* Developed REST APIs using **Django REST Framework**.
* APIs are available for authentication and ML prediction services.

### ⚙️ Background Processing

* Integrated **Celery and Redis** for background task processing.
* Time-consuming disease prediction tasks are processed asynchronously so they do not block the main application.

---

## 🛠️ Technologies Used

* **Backend:** Python, Django, Django REST Framework
* **Machine Learning:** Scikit-learn
* **Deep Learning:** TensorFlow, Keras, ResNet50
* **Data Processing:** Pandas, NumPy
* **Image Processing:** OpenCV
* **Authentication:** JWT
* **Task Queue:** Celery
* **Message Broker:** Redis
* **Database:** SQLite
* **Frontend:** HTML, CSS, Bootstrap, JavaScript, jQuery

---

## 🧠 Machine Learning Models

| Service                  | Type           | Model             |
| ------------------------ | -------------- | ----------------- |
| Crop Recommendation      | Classification | Random Forest     |
| Crop Yield Prediction    | Regression     | Linear Regression |
| Plant Disease Prediction | Deep Learning  | ResNet50 CNN      |

---

## 🏗️ Project Architecture

```text
CropQuest
│
├── accounts/
│   └── Authentication & User Management
│
├── crop_recomendation/
│   └── Crop Recommendation
│
├── yield_prediction/
│   └── Crop Yield Prediction
│
├── disease_prediction/
│   └── Plant Disease Prediction
│
├── ml/
│   └── Trained ML/DL Models
│
├── templates/
│   └── HTML Templates
│
├── static/
│   └── CSS, JavaScript & Static Files
│
├── media/
│   └── Uploaded Images
│
├── manage.py
└── requirements.txt
```

## 🔄 Application Workflow

```text
User
  │
  ▼
JWT Authentication
  │
  ▼
Django Application
  │
  ├── Crop Recommendation
  │       └── Classification Model
  │
  ├── Yield Prediction
  │       └── Regression Model
  │
  └── Disease Prediction
          └── Celery + Redis
                  │
                  ▼
             ResNet50 Model
                  │
                  ▼
             Disease Result
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd CropQuest
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Django Server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

## 🔐 Authentication

CropQuest uses **JWT authentication** for API security.

The general workflow is:

```text
Register
   ↓
Login
   ↓
JWT Access Token
   ↓
Authenticated API Request
   ↓
Prediction Service
```

## ⚡ Celery & Redis Setup

For disease prediction background processing, start the Redis server and Celery worker.

Example Celery command:

```bash
celery -A Crop_Recomendation_System worker --loglevel=info
```

Redis is used as the message broker between Django and Celery.

## 📌 Future Improvements

* Deploy the application to a cloud platform.
* Add more crop and disease classes.
* Improve model accuracy with additional training data.
* Add farmer-specific prediction history and analytics.
* Integrate weather and real-time agricultural data.

## 👨‍💻 Project

**CropQuest — Intelligent Crop and Fertilizer Recommendation System**

Built using **Django, Machine Learning, Deep Learning, REST APIs, JWT, Celery, and Redis**.
