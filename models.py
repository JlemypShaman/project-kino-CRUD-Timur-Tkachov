from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    """Model reprezentujący film w bazie danych"""
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)

    # Metoda pomocnicza do konwersji obiektu na słownik (JSON)
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "rating": self.rating,
            "release_year": self.release_year
        }
