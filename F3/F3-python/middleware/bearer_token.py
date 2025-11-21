from flask import request

def bearer_token_middleware(app):
    @app.before_request
    def extract_bearer_token():
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            request.token = auth_header.split(' ')[1]
        else:
            request.token = None
