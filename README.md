# Student Management System (Flask + Async SQLAlchemy)

A modern, production-grade Student Management System built with **Flask**, **Asynchronous SQLAlchemy**, and **Pydantic** for robust data validation. This project features a clean, responsive UI with full CRUD capabilities and a modular architecture.

## 🚀 Features

- **Asynchronous Operations**: Uses `aiosqlite` and `asyncio` for non-blocking database interactions.
- **Robust Validation**: Data integrity is ensured through **Pydantic V2** schemas.
- **Custom Error Handling**: Dedicated handlers for 404, 500, and 400 errors with user-friendly pages.
- **Modular Architecture**: Organized into `routes`, `services`, `models`, and `schemas` for scalability.
- **Interactive UI**: Stylish dashboard with real-time feedback using **Flash messaging** and **Confirm-on-Delete** JavaScript.
- **RESTful API**: Supports both traditional form-based interactions and a JSON API.

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

5. **Run the application**:
   ```bash
   python run.py
   ```

6. **Access the app**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## 🛡️ License

This project is open-source and available under the [MIT License](LICENSE).
