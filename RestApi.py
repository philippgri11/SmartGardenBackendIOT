from flask import Flask, json, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Flask(__name__)


def __init__(self):
    pass


@api.route('/get_zones', methods=['GET'])
@cross_origin()
def add_rule():
    return json.dumps([{'id': 'id1', 'title': 'title1', 'status': True},
                       {'id': 'id2', 'title': 'title2', 'status': False},
                       {'id': 'id3', 'title': 'title3', 'status': True},
                       {'id': 'id4', 'title': 'title4', 'status': False}])


@api.route('/save_zone_title', methods=['POST'])
@cross_origin()
def set_zone_title():
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@api.route('/get_rules', methods=['GET'])
@cross_origin()
def get_rule_ids():
    page = request.args.get('zone_id', type=int)
    return json.dumps([{'id': 1, 'von': {'hours': 15, 'minutes': 18}, 'bis': {'hours': 17, 'minutes': 10},
                        'wochentage': [True, True, True, False, True, False, True], 'wetter': True},
                       {'id': 2, 'von': {'hours': 13, 'minutes': 17}, 'bis': {'hours': 15, 'minutes': 13},
                        'wochentage': [True, False, True, False, True, False, True], 'wetter': True},
                       {'id': 3, 'von': {'hours': 13, 'minutes': 17}, 'bis': {'hours': 15, 'minutes': 13},
                        'wochentage': [True, False, True, True, True, False, True], 'wetter': True}])


@api.route('/add_rule', methods=['GET'])
def add_rules():
    return True


@api.route('/delete_rule', methods=['POST'])
@cross_origin()
def delete_rule():
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@api.route('/save_rule', methods=['POST'])
@cross_origin()
def save_rule():
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


if __name__ == '__main__':
    api.run()
