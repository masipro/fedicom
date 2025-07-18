import uuid
from flask import request

def tx_id_middleware(app):
    @app.before_request
    def generate_tx_id():
        request.txId = str(uuid.uuid4())
