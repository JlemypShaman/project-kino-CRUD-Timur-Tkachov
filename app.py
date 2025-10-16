# app.py
# -------------------------------------
# Główny plik aplikacji Flask (serwer)
# Udostępnia REST API dla encji "Movie"
# Komentarze w języku polskim

from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Movie

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # pozwala frontendowi (HTML/JS) komunikować się z API

# Konfiguracja bazy danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja ORM
db.init_app(app)

# Tworzenie tabeli w bazie, jeśli jeszcze nie istnieje
with app.app_context():
    db.create_all()

# ------------------ Pomocnicze funkcje walidacji ----------------------
def validate_movie_payload(data):
    """Walidacja prostych pól wejściowych. Zwraca tuple (is_valid, message)"""
    required = ['title', 'genre', 'rating', 'release_year']
    for field in required:
        if field not in data:
            return False, f"Pole '{field}' jest wymagane."
    # dodatkowa walidacja typów
    try:
        rating = float(data['rating'])
        year = int(data['release_year'])
    except (ValueError, TypeError):
        return False, "Niepoprawny typ pola 'rating' lub 'release_year'."
    if rating < 0 or rating > 10:
        return False, "Pole 'rating' musi być w zakresie 0-10."
    if year < 1800 or year > 2100:
        return False, "Pole 'release_year' ma nieprawidłową wartość."
    return True, "OK"

# ------------------ ROUTES ----------------------

# [GET] Pobierz wszystkie filmy
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([m.to_dict() for m in movies]), 200

# [GET] Pobierz film po ID
@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({"error": "Nie znaleziono filmu"}), 404
    return jsonify(movie.to_dict()), 200

# [POST] Dodaj nowy film
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json() or {}
    valid, msg = validate_movie_payload(data)
    if not valid:
        return jsonify({"error": msg}), 400
    new_movie = Movie(
        title=data['title'],
        genre=data['genre'],
        rating=float(data['rating']),
        release_year=int(data['release_year'])
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify(new_movie.to_dict()), 201

# [PUT] Zaktualizuj istniejący film
@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({"error": "Nie znaleziono filmu"}), 404
    data = request.get_json() or {}

    # Jeśli przesłano pola — walidujemy je selektywnie
    if 'rating' in data:
        try:
            r = float(data['rating'])
            if r < 0 or r > 10:
                return jsonify({"error": "Pole 'rating' musi być 0-10."}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Niepoprawny format 'rating'."}), 400
        movie.rating = r

    if 'release_year' in data:
        try:
            y = int(data['release_year'])
            if y < 1800 or y > 2100:
                return jsonify({"error": "Pole 'release_year' ma nieprawidłową wartość."}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Niepoprawny format 'release_year'."}), 400
        movie.release_year = y

    # pola tekstowe (bez skomplikowanej walidacji)
    movie.title = data.get('title', movie.title)
    movie.genre = data.get('genre', movie.genre)

    db.session.commit()
    return jsonify(movie.to_dict()), 200

# [DELETE] Usuń film po ID
@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({"error": "Nie znaleziono filmu"}), 404
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Film został usunięty"}), 200

# Prosty endpoint health-check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

# Uruchomienie serwera deweloperskiego
if __name__ == '__main__':
    app.run(debug=True)
