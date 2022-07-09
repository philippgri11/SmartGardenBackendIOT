from flask import json, request, jsonify
from flask_cors import cross_origin
from src.Rule import Rule
from src.scheduler import createNewJob, modifyJob, removeJob, conn

from src.wsgi import create_app

app = create_app()

with open("/home/pi/smartGardenBackendIOT/src/environment.json") as f:
    d = json.load(f)
    ALGORITHMS = d["ALGORITHMS"]

@app.route('/create_new_job', methods=['GET'])
@cross_origin()
def create_new_job():
    rule = getRulefromRequestData(request.data)
    GPIO = request.args.get('GPIO', type=int)
    createNewJob(rule, GPIO)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@app.route('/remove_Job', methods=['POST'])
@cross_origin()
def remove_Job():
    request_data = request.data
    id = json.loads(request_data)['id']
    removeJob(id)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@app.route('/update_status', methods=['POST'])
@cross_origin()
def update_status():
    request_data = request.data
    print(request_data)
    gpio = json.loads(request_data)['GPIO']
    status = json.loads(request_data)['status']
    conn.root.output(gpio,status)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200


@app.route('/modifyJob', methods=['POST'])
@cross_origin()
def modify_Job():
    rule = getRulefromRequestData(request.data)
    modifyJob(rule)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200

@app.route('/ping', methods=['GET'])
@cross_origin()
def ping():
    return jsonify(isError=False,
                   message="pong",
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



@app.route('/setRuhemodus', methods=['POST'])
@cross_origin()
def set_ruhemodus():
    request_data = request.data
    print(request_data)
    status = json.loads(request_data)['status']
    conn.root.setRuhemodusStatus(status)
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   ), 200

@app.route('/getRuhemodus', methods=['GET'])
@cross_origin()
def get_ruhemodus():
    print("get_ruhemodusIOT")
    status = conn.root.getStatusRuhemodus()
    print(status)
    payload = {"status": status}
    return json.dumps(payload)

if __name__ == '__main__':
    app.run()
