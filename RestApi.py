from flask import Flask, json

api = Flask(__name__)

def __init__(self):
    pass

@api.route('/get_zones', methods=['GET'])
def add_rule():
    return json.dumps({1: {'name': "Zonenname", 'status': True}, 2: {'name': "Zonenname2", 'status': False}})

@api.route('/get_rules', methods=['GET'])
def get_rule_ids(zone_id):
    return json.dumps({1: {'von': "", 'bis': "", 'wochentage': [], 'wetter': True}})

@api.route('/add_rule', methods=['GET'])
def add_rule():
    return True

@api.route('/delete_rule', methods=['GET'])
def delete_rule(rule_id):
    return True

if __name__ == '__main__':
    api.run()