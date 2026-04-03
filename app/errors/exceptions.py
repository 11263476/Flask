class StudentAppError(Exception):
    status_code = 500
    message = "An unexpected error occurred"

    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv

class ResourceNotFoundError(StudentAppError):
    status_code = 404
    message = "Resource not found"

class ValidationError(StudentAppError):
    status_code = 400
    message = "Validation failed"
