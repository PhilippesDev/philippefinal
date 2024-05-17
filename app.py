from flask import Flask, send_from_directory, request, jsonify
import sqlite3

# Création de la table si elle n'existe pas déjà
def init_db():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FormData (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            email TEXT NOT NULL,
            sujet TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


app = Flask(__name__)

# Routes pour servir les fichiers statiques
@app.route('/assets/css/<path:path>')
def serve_css(path):
    return send_from_directory('iPortfolio/assets/css', path)

@app.route('/assets/img/<path:path>')
def serve_img(path):
    return send_from_directory('iPortfolio/assets/img', path)

@app.route('/assets/js/<path:path>')
def serve_js(path):
    return send_from_directory('iPortfolio/assets/js', path)

@app.route('/assets/vendor/<path:path>')
def serve_vendor(path):
    return send_from_directory('iPortfolio/assets/vendor', path)

@app.route('/')
def index():
    return send_from_directory('iPortfolio', 'index.html')

# Routes pour servir les autres fichiers HTML
@app.route('/<path:filename>')
def serve_html(filename):
    return send_from_directory('iPortfolio', filename)

# Route pour soumettre le formulaire et enregistrer les données dans la base de données
@app.route('/submit_form', methods=['POST'])
def submit_form():
    nom = request.form['name']
    email = request.form['email']
    sujet = request.form['subject']
    message = request.form['message']

    # Connexion à la base de données SQLite
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # Insertion des données dans la table correspondante
    cursor.execute("INSERT INTO FormData (nom, email, sujet, message) VALUES (?, ?, ?, ?)", (nom, email, sujet, message))
    
    # Commit et fermeture de la connexion
    conn.commit()
    conn.close()

    # Renvoyer une réponse JSON
    return jsonify({'message': 'Message envoyé avec succès'})


if __name__ == '__main__':
    init_db()
    app.run()