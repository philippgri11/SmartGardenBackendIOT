import os
from urllib.request import urlopen
import flask
from flask import json, request, jsonify, Flask
from flask_cors import cross_origin

from src.Rule import Rule
from jose import jwt
from six import wraps

from src.controlGPIO import output
from src.scheduler import scheduler

from src.wsgi import create_app

app = create_app()

with open("src/environment.json") as f:
    d = json.load(f)
    ALGORITHMS = d["ALGORITHMS"]
    AUTH0_DOMAIN = d["AUTH0_DOMAIN"]
    API_AUDIENCE = d["API_AUDIENCE"]


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must start with"
                             " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be"
                             " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_auth(f):
    """Determines if the Access Token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        print(os.getenv('AUTH0_DOMAIN'))
        print(AUTH0_DOMAIN)
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://" + AUTH0_DOMAIN + "/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                 "description":
                                     "incorrect claims,"
                                     "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                 "description":
                                     "Unable to parse authentication"
                                     " token."}, 401)

            flask._request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)

    return decorated


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.route('/create_new_job', methods=['GET'])
@cross_origin()
def create_new_job():
    rule = getRulefromRequestData(request.data)
    GPIO = request.args.get('GPIO', type=int)
    create_new_job(rule, GPIO)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@app.route('/remove_Job', methods=['POST'])
@cross_origin()
def remove_Job():
    request_data = request.data
    id = json.loads(request_data)['id']
    scheduler.removeJob(id)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@app.route('/update_status', methods=['POST'])
@cross_origin()
def update_status():
    request_data = request.data
    zoneId = json.loads(request_data)['ZoneId']
    status = json.loads(request_data)['status']
    output(zoneId,status)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@app.route('/modifyJob', methods=['POST'])
@cross_origin()
def modifyJob():
    rule = getRulefromRequestData(request.data)
    modifyJob(rule)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200

def getRulefromRequestData(request_data):
    id = json.loads(request_data)['id']
    bisHours = json.loads(request_data)['bis']['hours']
    bisMinutes = json.loads(request_data)['bis']['minutes']
    vonHours = json.loads(request_data)['von']['hours']
    vonminutes = json.loads(request_data)['von']['minutes']
    wochentag = json.loads(request_data)['wochentage']
    wetter = json.loads(request_data)['wetter']
    return Rule(id, vonminutes, vonHours, bisMinutes, bisHours, wochentag, wetter)


if __name__ == '__main__':
    app.run()
