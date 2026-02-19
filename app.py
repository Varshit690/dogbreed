from flask import Flask, render_template, request
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
import numpy as np
import os, uuid
from PIL import Image

app = Flask(__name__)

# =========================
# LOAD PRETRAINED MODELS
# =========================

# Main classifier (ImageNet – includes many dog breeds)
classifier = MobileNetV2(weights="imagenet")

# Optional: Dog / Non-dog detector (same model reused)
detector_model = classifier


# =========================
# ROUTES
# =========================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict")
def predict():
    return render_template("predict.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        try:
            with open("contacts.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"Name: {name}\nEmail: {email}\n"
                    f"Subject: {subject}\nMessage: {message}\n---\n"
                )
        except Exception:
            pass

        return render_template("contact.html", submitted=True)

    return render_template("contact.html", submitted=False)


@app.route("/result", methods=["POST"])
def result():
    file = request.files["file"]

    # Save uploaded image
    ext = os.path.splitext(file.filename)[1]
    fname = f"upload_{uuid.uuid4().hex}{ext}"
    img_path = os.path.join("static/images", fname)
    file.save(img_path)

    # =========================
    # DOG DETECTION
    # =========================

    try:
        det_img = image.load_img(img_path, target_size=(224, 224))
        det_arr = image.img_to_array(det_img)
        det_arr = np.expand_dims(det_arr, axis=0)
        det_arr = preprocess_input(det_arr)

        det_preds = detector_model.predict(det_arr)
        decoded = decode_predictions(det_preds, top=5)[0]

        # ImageNet dog classes start with "n020"
        is_dog = any(p[0].startswith("n020") for p in decoded)

    except Exception:
        is_dog = True  # fail-safe

    if not is_dog:
        return render_template(
            "output.html",
            prediction="No dog found in this image",
            image_path=img_path,
            confidence=None,
            no_dog=True
        )

    # =========================
    # BREED CLASSIFICATION
    # =========================

    preds = classifier.predict(det_arr)
    decoded = decode_predictions(preds, top=5)[0]

    # Keep only dog-related predictions
    dog_preds = [d for d in decoded if d[0].startswith("n020")]

    if not dog_preds:
        return render_template(
            "output.html",
            prediction="Dog detected, but breed not recognized",
            image_path=img_path,
            confidence=None,
            no_dog=False
        )

    # Top-1 prediction
    breed = dog_preds[0][1].replace("_", " ").title()
    confidence = dog_preds[0][2] * 100

    # Determine display type based on confidence
    if confidence >= 95:
        # High confidence: display the predicted breed
        return render_template(
            "output.html",
            prediction=breed,
            image_path=img_path,
            confidence=f"{confidence:.2f}",
            no_dog=False,
            high_confidence=True,
            similar_breeds=None
        )
    else:
        # Low confidence: display similar breeds
        similar_breeds = [
            (d[1].replace("_", " ").title(), round(d[2] * 100, 2))
            for d in dog_preds[:5]
        ]
        return render_template(
            "output.html",
            prediction=breed,
            image_path=img_path,
            confidence=f"{confidence:.2f}",
            no_dog=False,
            high_confidence=False,
            similar_breeds=similar_breeds
        )


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    print("Starting Flask app at http://127.0.0.1:5000")
    app.run(debug=True)
