# Project Kino CRUD — Timur Tkachov

Opis projektu: 
Aplikacja demonstracyjna CRUD dla encji **Movie** — system zarządzania filmami w kinie.
Projekt przygotowany do pracy w VSCode.

# Technologie
- Python 3.10+
- Flask
- SQLite (plik `database.db`)
- HTML + JavaScript + Bootstrap (frontend)

# Uruchomienie projektu lokalnie (Windows/macOS/Linux)
1. Sklonuj repozytorium:
   ```bash
   git clone <URL_REPO> project-kino-CRUD-Timur-Tkachov
   cd project-kino-CRUD-Timur-Tkachov
   ```

2. Utwórz i aktywuj środowisko wirtualne:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```

3. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```

4. Uruchom aplikację:
   ```bash
   python app.py
   ```

5. Otwórz frontend w przeglądarce:
   http://127.0.0.1:5000/static/index.html

# Migracja SQL
W katalogu znajduje się plik `migrations/create_table_movies.sql` z definicją tabeli.
Aplikacja przy pierwszym uruchomieniu tworzy tabelę automatycznie używając SQLAlchemy.

## 🧭 Endpointy API (PL)
| Metoda | Ścieżka | Opis |
|---|---|---|
| GET | `/movies` | Pobierz listę filmów |
| GET | `/movies/<id>` | Pobierz szczegóły filmu |
| POST | `/movies` | Dodaj nowy film |
| PUT | `/movies/<id>` | Edytuj film |
| DELETE | `/movies/<id>` | Usuń film |

