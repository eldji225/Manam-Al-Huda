from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Chemin du fichier d'avis
REVIEWS_FILE = "reviews.json"

def load_reviews():
    if os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_review(review):
    reviews = load_reviews()
    # Limiter à 20 avis pour éviter la surcharge
    if len(reviews) >= 20:
        reviews = reviews[-19:]  # Garde les 19 derniers
    reviews.append(review)
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit-review", methods=["POST"])
def submit_review():
    data = request.get_json()
    rating = data.get("rating")
    comment = data.get("comment", "").strip()

    if not rating or not (1 <= int(rating) <= 5):
        return jsonify({"error": "Veuillez choisir une note entre 1 et 5."}), 400

    # Filtrer les commentaires vides ou suspects
    if len(comment) > 300:
        return jsonify({"error": "Le commentaire est trop long (max 300 caractères)."}), 400

    review = {
        "rating": int(rating),
        "comment": comment if comment else "Aucun commentaire",
        "date": datetime.now().strftime("%d/%m/%Y")
    }

    save_review(review)
    return jsonify({"success": "Merci pour votre avis ! 🌙"})

@app.route("/get-reviews", methods=["GET"])
def get_reviews():
    reviews = load_reviews()
    # Retourner les 10 derniers avis
    return jsonify(reviews[-10:])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
