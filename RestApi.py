import os
from urllib.request import urlopen
import flask
from flask import Flask, json, request, jsonify
from flask_cors import CORS, cross_origin
import Database
import scheduler
from model.Rule import Rule, RuleEncoder
from model.Zone import Zone, ZoneEncoder
from jose import jwt
from six import wraps

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Flask(__name__)

with open('environment.json') as f:
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


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@api.route('/save_zone_title', methods=['POST'])
@cross_origin()
@requires_auth
def set_zone_title():
    request_data = request.data
    title = json.loads(request_data)['title']
    zoneId = json.loads(request_data)['zoneId']
    Database.updateZoneTitel(zoneId, title)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@api.route('/get_zone_titel', methods=['GET'])
@cross_origin()
@requires_auth
def get_zone_titel():
    zoneId = request.args.get('zone_id', type=int)
    return json.dumps(Database.getZoneTitel(zoneId))


@api.route('/get_rules', methods=['GET'])
@cross_origin()
@requires_auth
def get_rules():
    zoneId = request.args.get('zone_id', type=int)
    rules = []
    [rules.append(Rule(rule)) for rule in Database.getRules(zoneId)]
    return json.dumps(rules, cls=RuleEncoder)


@api.route('/get_rule', methods=['GET'])
@cross_origin()
@requires_auth
def get_rule():
    ruleID = request.args.get('ruleId', type=int)
    return json.dumps(Database.getRuleByRuleId(ruleID), cls=RuleEncoder)


@api.route('/create_new_rule', methods=['GET'])
@cross_origin()
@requires_auth
def create_new_rule():
    zoneId = request.args.get('zoneID', type=int)
    Database.createNewRule(0, 0, 0, 0, "0000000", 0, zoneId)
    ruleID = Database.getLastRuleID()
    return json.dumps(Database.getRuleByRuleId(ruleID), cls=RuleEncoder)


@api.route('/delete_rule', methods=['POST'])
@cross_origin()
@requires_auth
def delete_rule():
    request_data = request.data
    id = json.loads(request_data)['id']
    scheduler.removeJob(id)
    Database.deleteRuleByRuleId(id)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@api.route('/update_status', methods=['POST'])
@cross_origin()
@requires_auth
def update_status():
    request_data = request.data
    id = json.loads(request_data)['id']
    status = json.loads(request_data)['status']
    Database.updateStatus(id, status)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@api.route('/save_rule', methods=['POST'])
@cross_origin()
@requires_auth
def save_rule():
    request_data = request.data
    id = json.loads(request_data)['id']
    bisHours = json.loads(request_data)['bis']['hours']
    bisMinutes = json.loads(request_data)['bis']['minutes']
    vonHours = json.loads(request_data)['von']['hours']
    vonminutes = json.loads(request_data)['von']['minutes']
    wochentag = json.loads(request_data)['wochentage']
    wetter = json.loads(request_data)['wetter']
    tage = ''
    for tag in wochentag:
        if (tag):
            tage += '1'
        else:
            tage += '0'
    rule = Rule(id, vonminutes, vonHours, bisMinutes, bisHours, tage, wetter)
    if rule.changed():
        scheduler.scheduleJob(rule)
        Database.saveRule(rule)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@api.route('/get_zones', methods=['GET'])
@cross_origin()
@requires_auth
def get_zones():
    zones = []
    [zones.append(Zone(zone)) for zone in Database.getZones()]
    return json.dumps(zones, cls=ZoneEncoder)


if __name__ == '__main__':
    api.run()
