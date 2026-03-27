from app.main import create_app  # Import the app factory function from the app package

app = create_app()  # Initialize the Flask application using the factory

if __name__ == "__main__":  # Ensure the script runs only when executed directly
    app.run(debug=True)  # Start the development server with debug mode enabled
