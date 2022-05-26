import string

from flask import Flask, json, request, jsonify
from flask_cors import CORS, cross_origin

import Database
from model.Rule import Rule, RuleEncoder
from model.Zone import Zone, ZoneEncoder

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Flask(__name__)


@api.route('/get_zones', methods=['GET'])
@cross_origin()
def add_rule():
    zones = []
    [zones.append(Zone(zone)) for zone in Database.getZones()]
    return json.dumps(zones, cls=ZoneEncoder)
    # return json.dumps([{'id': 'id1', 'title': 'title1', 'status': True},
    #                    {'id': 'id2', 'title': 'title2', 'status': False},
    #                    {'id': 'id2', 'title': 'title2', 'status': False},
    #                    {'id': 'id2', 'title': 'title2', 'status': False},
    #                    {'id': 'id3', 'title': 'title3', 'status': True},
    #                    {'id': 'id4', 'title': 'title4', 'status': False}])


@api.route('/save_zone_title', methods=['POST'])
@cross_origin()
def set_zone_title():
    request_data = request.data
    title = json.loads(request_data)['title']
    zoneId = json.loads(request_data)['zoneId']
    print(title)
    Database.updateZoneTitel(zoneId, title)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@api.route('/get_zone_titel', methods=['GET'])
@cross_origin()
def get_zone_titel():
    zoneId = request.args.get('zone_id', type=int)
    return json.dumps(Database.getZoneTitel(zoneId)[0])


@api.route('/get_rules', methods=['GET'])
@cross_origin()
def get_rules():
    zoneId = request.args.get('zone_id', type=int)
    rules = []
    [rules.append(Rule(rule)) for rule in Database.getRules(zoneId)]
    print(rules)
    return json.dumps(rules, cls=RuleEncoder)
    # return json.dumps([{'id': 1, 'von': {'hours': 15, 'minutes': 18}, 'bis': {'hours': 17, 'minutes': 10},
    #                     'wochentage': [True, True, True, False, True, False, True], 'wetter': True},
    #                    {'id': 2, 'von': {'hours': 13, 'minutes': 17}, 'bis': {'hours': 15, 'minutes': 13},
    #                     'wochentage': [True, False, True, False, True, False, True], 'wetter': True},
    #                    {'id': 2, 'von': {'hours': 13, 'minutes': 17}, 'bis': {'hours': 15, 'minutes': 13},
    #                     'wochentage': [True, False, True, False, True, False, True], 'wetter': True},
    #                    {'id': 3, 'von': {'hours': 13, 'minutes': 17}, 'bis': {'hours': 15, 'minutes': 13},
    #                     'wochentage': [True, False, True, True, True, False, True], 'wetter': True}])


@api.route('/get_rule', methods=['GET'])
@cross_origin()
def get_rule():
    ruleID = request.args.get('ruleId', type=int)
    print(ruleID)
    return json.dumps(Rule(Database.getRuleByRuleId(ruleID)[0]), cls=RuleEncoder)
    # return json.dumps({'id': 1, 'von': {'hours': 11, 'minutes': 15}, 'bis': {'hours': 17, 'minutes': 10},
    #                    'wochentage': [True, True, True, False, True, False, True], 'wetter': True})


@api.route('/create_new_rule', methods=['GET'])
@cross_origin()
def create_new_rule():
    zoneId = request.args.get('zoneID', type=int)
    print(zoneId)
    Database.createNewRule(0, 0, 0, 0, "0000000", 0, zoneId)
    ruleID = Database.getLastRuleID()
    return json.dumps(Rule(Database.getRuleByRuleId(ruleID)[0]), cls=RuleEncoder)
    # return json.dumps({'id': 1, 'von': {'hours': 15, 'minutes': 13}, 'bis': {'hours': 17, 'minutes': 10},
    #                    'wochentage': [True, True, True, False, True, False, True], 'wetter': True})


@api.route('/delete_rule', methods=['POST'])
@cross_origin()
def delete_rule():
    request_data = request.data
    id = json.loads(request_data)['id']
    Database.deleteRuleByRuleId(id)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@api.route('/update_status', methods=['POST'])
@cross_origin()
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
    Database.saveRule(vonminutes, vonHours, bisMinutes, bisHours, tage, wetter, id)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


if __name__ == '__main__':
    api.run()
