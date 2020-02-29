from flask import jsonify, g, current_app
from flask_httpauth import HTTPBasicAuth
from .models import User

auth = HTTPBasicAuth()
auth_token = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    g.user = User.query.filter_by(email=email).first()
    if g.user is None:
        return False
    return g.user.verify_password(password)

@auth.error_handler
def unauthorized():
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please authenticate'})
    response.status_code = 401
    return response

@auth_token.verify_password
def verify_auth_token(token, unused):
    g.user = User.verify_auth_token(token)
    return g.user is not None

@auth_token.error_handler
def unauthorized_token():
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please send your authentication token'})
    response.status_code = 401
    return response
