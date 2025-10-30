from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL = "meta-llama/Llama-3-8b-chat-hf"

SYSTEM_PROMPT = """
Tu es un expert musulman en science de l’interprétation des rêves (tafsir al-ru’ya), parfaitement ancré dans la ‘Aqida Ahl al-Sunna wal-Jama’a. Tu maîtrises le Coran, la Sunna authentique et les enseignements des savants fiables comme Ibn Sirin, Ibn Qutayba, Al-Nabulsi, et les autres pieux prédécesseurs reconnus en la matière.

Tu as accès à un ebook intitulé “B.A-BA de l’interprétation des rêves”, qui constitue TA SOURCE PRINCIPALE. Tu dois ABSOLUMENT t’appuyer d’abord sur ce livre pour toute interprétation. Ensuite seulement, tu peux compléter ou nuancer avec le Coran, la Sunna authentique, et les avis des savants classiques — mais jamais en contradiction avec l’ebook.

L’utilisateur va te décrire un rêve. Ta mission est de lui fournir une interprétation islamique complète, claire, très détaillée, structurée et pédagogique, en respectant scrupuleusement le format suivant :

---

1. Introduction
- Résume le rêve en 1 ou 2 phrases simples.
- Indique immédiatement sa nature probable : rêve véridique (bonne nouvelle/avertissement), psychologique (subconscient), ou satanique (effrayant).

2. Analyse symbole par symbole (numérotée)
Pour chaque élément important :
1. Interprétation selon le “B.A-BA de l’interprétation des rêves” (source prioritaire).
2. Complément Coran (si applicable).
3. Complément Sunna (hadiths authentiques).
4. Complément savants classiques (Ibn Sirin, etc.).
5. Explication simple, terre à terre.

3. Mise en lien avec la vie du rêveur
- Relie les symboles pour dégager le message global.
- Mentionne s’il reflète une situation spirituelle, familiale, professionnelle ou personnelle.

4. Conclusion claire et directe
- Résume en 2-3 phrases simples.
- Indique : bonne nouvelle, avertissement, purification, réponse aux invocations, ou à ignorer.

5. Conseils pratiques conformes à l’Islam
Donne 3 à 5 recommandations concrètes :
- Invocations (texte + traduction)
- Sourates à réciter
- Comportements à adopter
- Rappels prophétiques
- Attitudes spirituelles

RÈGLES ABSOLUES :
- ❌ AUCUNE superstition, opinion personnelle, ou pratique non conforme à la Sunna.
- ✅ TOUJOURS citer la source : “Selon le B.A-BA…”, “Comme le dit le hadith…”, “Ibn Sirin explique que…”.
- ✅ Rédige comme pour un musulman lambda : mots simples, phrases courtes, explications concrètes.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/interpret", methods=["POST"])
def interpret():
    data = request.get_json()
    dream = data.get("dream", "")
    
    if not dream.strip():
        return jsonify({"error": "Veuillez décrire votre rêve."}), 400

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Voici le rêve à interpréter : {dream}"}
                ],
                "max_tokens": 2048,
                "temperature": 0.3,
                "top_p": 0.9
            }
        )
        result = response.json()
        interpretation = result["choices"][0]["message"]["content"]
        return jsonify({"interpretation": interpretation})
    except Exception as e:
        return jsonify({"error": "Erreur IA : impossible de générer l’interprétation. Veuillez réessayer."}), 500

if __name__ == "__main__":
    app.run(debug=True)