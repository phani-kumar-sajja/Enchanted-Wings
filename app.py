from flask import Flask, render_template, request, redirect, url_for, session, flash
from flaskwebgui import FlaskUI
import sqlite3
import os
import logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 = all logs, 1 = warnings, 2 = errors, 3 = fatal
from keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)
app.secret_key = 'phani_3588'

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load model
try:
    model = load_model("vgg16_model.h5")
    logging.info("✅ Model loaded successfully.")
except Exception as e:
    logging.error(f"❌ Error loading model: {e}")
    model = None

# Load butterfly class names
butterfly_names = [
    'ADONIS','AFRICAN GIANT SWALLOWTAIL','AMERICAN SNOOT','AN 88','APPOLLO','ATALA','BANDED ORANGE HELICONIAN',
    'BANDED PEACOCK','BECKERS WHITE','BLACK HAIRSTREAK','BLUE MORPHO','BLUE SPOTTED CROW','BROWN SIPROETA',
    'CABBAGE WHITE','CAIRNS BIRDWING','CHECQUERED SKIPPER','CHESTNUT','CLEOPATRA','CLODIUS PARNASSIAN',
    'CLOUDED SULPHUR','COMMON BANDED AWL','COMMON WOOD-NYMPH','COPPER TAIL','CRECENT','CRIMSON PATCH',
    'DANAID EGGFLY','EASTERN COMA','EASTERN DAPPLE WHITE','EASTERN PINE ELFIN','ELBOWED PIERROT','GOLD BANDED',
    'GREAT EGGFLY','GREAT JAY','GREEN CELLED CATTLEHEART','GREY HAIRSTREAK','INDRA SWALLOW','IPHICLUS SISTER',
    'JULIA','LARGE MARBLE','MALACHITE','MANGROVE SKIPPER','MESTRA','METALMARK','MILBERTS TORTOISESHELL',
    'MONARCH','MOURNING CLOAK','ORANGE OAKLEAF','ORANGE TIP','ORCHARD SWALLOW','PAINTED LADY','PAPER KITE',
    'PEACOCK','PINE WHITE','PIPEVINE SWALLOW','POPINJAY','PURPLE HAIRSTREAK','PURPLISH COPPER','QUESTION MARK',
    'RED ADMIRAL','RED CRACKER','RED POSTMAN','RED SPOTTED PURPLE','SCARCE SWALLOW','SILVER SPOT SKIPPER',
    'SLEEPY ORANGE','SOOTYWING','SOUTHERN DOGFACE','STRAITED QUEEN','TROPICAL LEAFWING','TWO BARRED FLASHER',
    'ULYSES','VICEROY','WOOD SATYR','YELLOW SWALLOW TAIL','ZEBRA LONG WING'
]

@app.route('/')
def home():
    if 'user' not in session:
        logging.info("User not logged in, redirecting to auth page.")
        return redirect(url_for('auth'))
    return render_template('home.html')

@app.route('/auth', methods=['GET'])
def auth():
    return render_template('SignUp_LogIn_Form.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()

    if result:
        session['user'] = username
        return redirect(url_for('home'))
    else:
        logging.warning("❌ Invalid credentials!")
        return redirect(url_for('home'))

@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, email TEXT UNIQUE, password TEXT)')

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        logging.warning("⚠️ Username already exists!")
        return redirect(url_for('auth'))

    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    if c.fetchone():
        conn.close()
        logging.warning("❌ Email is already registered.")
        return redirect(url_for('auth'))

    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
              (username, email, password))
    conn.commit()
    conn.close()

    logging.info("✅ Registration successful.")
    return redirect(url_for('auth'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        logging.info("User not logged in, redirecting to auth page.")
        return redirect(url_for('auth'))
    if model is None:
        logging.error("Model not loaded.")
        flash("Model not available.", "error")
        return redirect(url_for('home'))

    if 'image' not in request.files:
        logging.warning("No image part in the request.")
        flash('No image file provided.', 'error')
        return redirect(url_for('home'))

    file = request.files['image']
    if file.filename == '':
        logging.warning("Empty filename.")
        flash('No selected file.', 'error')
        return redirect(url_for('home'))

    if not allowed_file(file.filename):
        logging.warning(f"Unsupported file type: {file.filename}")
        flash('Unsupported file type.', 'error')
        return redirect(url_for('home'))

    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        img = Image.open(filepath).convert('RGB').resize((224, 224))
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0).astype(np.float32)

        prediction = model.predict(img_array)
        predicted_class = butterfly_names[np.argmax(prediction)]

        print(f"Prediction: {predicted_class} for {file.filename}")

        return render_template('output.html', image_path=filepath, result=predicted_class)
    except Exception as e:
        logging.exception("Error during prediction")
        flash("Something went wrong during prediction.", "error")
        return redirect(url_for('home'))



@app.route('/about')
def about():
    if 'user' not in session:
        logging.info("User not logged in, redirecting to auth page.")
        return redirect(url_for('auth'))
    return render_template('about.html')



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth'))

if __name__ == "__main__":
    app.run(debug=True)
    # ui = FlaskUI(app=app, server="flask", width=1024, height=768)
    # ui.run()
