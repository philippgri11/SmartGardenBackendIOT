import json

class Zone:
    def __init__(self, *args):
        if len(args) == 3:
            self.id = args[0]
            self.title = args[1]
            self.status = args[2]
        elif isinstance(args[0], tuple):
            zone = args[0]
            self.id = zone[0]
            self.title = zone[1]
            self.status = zone[2]

class ZoneEncoder(json.JSONEncoder):
    def default(self, zone):
        return {'id': zone.id, 'title': zone.title, 'status': zone.status}
