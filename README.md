# 🦋 Enchanted Wings: Butterfly Species Classifier

**Enchanted Wings** is a deep learning–based web application that identifies butterfly species from uploaded images using a fine-tuned VGG16 model. The application supports biodiversity monitoring, ecological research, and educational engagement through an intuitive, visually appealing interface.

---

## 🚀 Features

- 🧠 Transfer learning with VGG16 for high accuracy
- 🖼️ Image upload and real-time butterfly species prediction
- 🌐 Flask-based web interface
- 🎨 Glassmorphic UI with animated butterfly background
- 🔒 Optional user authentication
- 📄 Detailed About Page

---

## 📸 Demo

![App Screenshot](static/images/Home_screenshot.png)

Try it locally by uploading a butterfly image and getting the species name instantly.

---

## 📁 Project Structure

EnchantedWings/<br>
├── app.py # Main Flask backend<br>
├── vgg16_model.h5 # Trained model<br>
│<br>
├── static/<br>
│<br>
├── templates/<br>
│ ├── home.html # Upload and prediction UI<br>
│ ├── output.html # Result display page<br>
│ ├── about.html # Info page<br>
| └── SignUp_Login.html<br>
│<br>
├── database/users.db # SQLite DB for user login (optional)<br>
├── requirements.txt # Dependencies<br>
└── README.md # You're here!<br>

## ⚙️ Installation

### 🔹 Step 1: Clone the Repository

git clone https://github.com/phani-kumar-sajja/Enchanted-Wings.git
cd enchanted-wings
### 🔹 Step 2: Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
### 🔹 Step 3: Install Dependencies

pip install -r requirements.txt
### 🔹 Step 4: Run the App

python app.py
Open your browser at http://127.0.0.1:5000

🧠 Model
Architecture: VGG16

Framework: Keras + TensorFlow

Dataset: ~6,500 butterfly images across 75 species

Training: Conducted using transfer learning with frozen base layers and a custom classifier head

🌟 Screenshots<br>
Home Page ![Home Screenshot](static/images/Home_screenshot.png)<br>
About Page ![About Screenshot](static/images/About_screenshot.png)<br>
Result Page ![Result Screenshot](static/images/Output_screenshot.png)<br>
Login Page ![Login Screenshot](static/images/Login_screenshot.png)<br>

✨ Future Improvements
Add multilingual species descriptions

Enable mobile camera integration

Improve model with more data and augmentation

Deploy on platforms like Render, Vercel, or AWS

🛡️ License
MIT License © 2025 [Techie Bugs]

🤝 Acknowledgments<br>
<a href="https://www.kaggle.com/">Kaggle Butterfly Dataset</a><br>

<a href="https://www.tensorflow.org/">TensorFlow</a><br>

<a href="https://flask.palletsprojects.com/">Flask</a><br>

Inspired by the natural beauty of butterflies and the need for ecological awareness 🦋
