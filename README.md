# Student Management System (Flask + Async SQLAlchemy)

A modern, production-grade Student Management System built with **Flask**, **Asynchronous SQLAlchemy**, and **Pydantic** for robust data validation. This project features a clean, responsive UI with full CRUD capabilities and a modular architecture.

## 🚀 Features

- **Asynchronous Operations**: High-performance database interactions via `aiosqlite` and `asyncio`.
- **JWT Authentication**: Secure, stateless user sessions using **JSON Web Tokens** and HttpOnly cookies.
- **Role-Based Access (RBAC)**: Defined `admin` and `user` roles with protected administrative routes.
- **Premium UI / Dark Mode**: Modern **Indigo Theme** with a persistent **Dark/Light Mode** switcher.
- **User Management**: Administrative oversight dashboard for managing system users.
- **Robust Validation**: Server-side data integrity via **Pydantic V2** schemas.
- **Custom Error Handling**: Professional 404, 500, and 400 error pages.
- **Modular Architecture**: Clean separation of `routes`, `services`, `models`, and `schemas`.

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

5. **Create your Admin account**:
   ```bash
   python seed_admin.py YourUsername YourEmail YourPassword
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
