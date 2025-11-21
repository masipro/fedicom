class ErrorFedicom(Exception):
    def __init__(self, code=None, message=None, status_code=400):
        self.errors = []
        if code and message:
            self.insertar(code, message)
        self.status_code = status_code
        super().__init__(message)

    def insertar(self, code, message):
        self.errors.append({'code': code, 'message': message})

    def to_dict(self):
        return {'errors': self.errors}

    def tiene_errores(self):
        return len(self.errors) > 0
