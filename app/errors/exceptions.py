class StudentAppError(Exception):  # Base exception class for our application
    """Base class for exceptions in this app."""
    status_code = 500  # Default to Internal Server Error
    message = "An unexpected error occurred"

    # Constructor to initialize error details
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        self.payload = payload

    # Utility function to convert the error into a dictionary (for JSON responses)
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv

class ResourceNotFoundError(StudentAppError):  # Specific error for missing items (404)
    status_code = 404
    message = "Resource not found"

class ValidationError(StudentAppError):  # Specific error for invalid input data (400)
    status_code = 400
    message = "Validation failed"
