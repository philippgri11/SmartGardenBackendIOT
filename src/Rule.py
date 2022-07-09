import datetime
import json


class Rule:
    def __init__(self, *args):
        print(args)
        if len(args) == 5:
            self.id = args[0]
            self.von = args[1]
            self.bis = args[2]
            self.wochentag = args[3]
            self.wetter = args[4]
        elif len(args) == 7:
            self.id = args[0]
            self.von = datetime.time(args[2], args[1])
            self.bis = datetime.time(args[4], args[3])
            tag = []
            print('args[5]')
            print(args[5])
            for char in args[5]:
                tag.append(True) if (char == '1') else tag.append(False)
            self.wochentag = tag
            self.wetter = args[6]
        elif isinstance(args[0], tuple):
            zone = args[0]
            self.id = zone[0]
            self.von = datetime.time(zone[2], zone[1])
            self.bis = datetime.time(zone[4], zone[3])
            tag = []
            print('zone[5]')
            print(zone[5])
            for char in zone[5]:
                tag.append(True) if (char == '1') else tag.append(False)
            self.wochentag = tag
            self.wetter = zone[6]

    def getDayOfWeek(self):
        str = ''
        tage = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        for i in range(len(self.wochentag)):
            print(self.wochentag[i])
            if self.wochentag[i]:
                if len(str) > 0:
                    str += ','
                str += tage[i]
        if str == '':
            return 'mon'
        return str


class RuleEncoder(json.JSONEncoder):
    def default(self, rule):
        print(rule.id)
        return {'id': rule.id, 'von': {'hours': rule.von.hour, 'minutes': rule.von.minute},
                'bis': {'hours': rule.bis.hour, 'minutes': rule.bis.minute}, 'wochentage': rule.wochentag,
                'wetter': rule.wetter}
