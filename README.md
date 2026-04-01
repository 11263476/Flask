# Student Management System (Flask + Async SQLAlchemy)

A modern, production-grade Student Management System built with **Flask**, **Asynchronous SQLAlchemy**, and **Pydantic** for robust data validation. This project features a clean, responsive UI with full CRUD capabilities and a modular architecture.

## 🚀 Key Features

- **JWT-Based Authentication**: Stateless security using `Flask-JWT-Extended` with HttpOnly cookies.
- **CSRF Protection**: Global security using `Flask-WTF` to prevent Cross-Site Request Forgery.
- **RBAC (Role-Based Access Control)**: Custom `@admin_required` decorators strictly protect all modification routes (Add, Edit, Delete).
- **Asynchronous Data Layer**: High-performance database operations using `SQLAlchemy` and `aiosqlite`.
- **Modern UI/UX**: Professional Indigo palette, persistent **Dark Mode**, and Glassmorphic navigation.

## 🛡️ Security Implementation

- **Stateless Identity**: Uses JWT tokens instead of traditional sessions, making the backend more scalable.
- **Unified CSRF Strategy**: One cryptographically-signed token protects every POST request in the app.
- **Password Hashing**: Uses `Werkzeug`'s industry-standard `pbkdf2:sha256` hashing.
- **Cookie Hardening**: Configured for `HttpOnly` to prevent XSS-based token theft.

## 📂 Project Structure

```text
flask/
├── app/
│   ├── db/              # Database models and configuration
│   ├── errors/          # Custom error handlers and exceptions
│   ├── routes/          # Flask blueprints and route definitions
│   ├── schemas/         # Pydantic validation schemas
│   ├── services/         # Business logic layer
│   ├── static/          # CSS and JavaScript assets
│   ├── templates/       # Jinja2 HTML templates
│   ├── config.py        # Application configuration
│   └── main.py          # App factory
├── venv/                # Virtual environment (ignored by Git)
├── .gitignore          # Git exclusion rules
├── init_db.py           # Database initialization script
├── requirements.txt     # Project dependencies
├── run.py               # Main application entry point
└── README.md            # Project documentation
```

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/11263476/Flask.git
   cd Flask
   ```

2. **Set up the virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # source venv/bin/activate # On Unix/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   ```bash
   python init_db.py
   ```

5. **Bootstrap/Reset Admin Account**:
Run the private seeding script to create your first admin or **reset a forgotten password**:
```powershell
python seed_admin.py <username> <email> <password>
```
*Note: If the username already exists, the script will securely update the password hash in-place.*
# Example: python seed_admin.py admin admin@example.com admin123
   ```

6. **Run the application**:
   ```bash
   python run.py
   ```

7. **Access the app**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## 🛡️ License

This project is open-source and available under the [MIT License](LICENSE).
