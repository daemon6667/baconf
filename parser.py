#!/usr/bin/env python

from config import *
from copy import deepcopy

#
# m_resources variable format 
# m_resources = { 'client': [
#                            'client1': [ 'keyname1': 'value', 'keyname2': 'value' ],
#                            'client2': [ 'keyname1': 'value', 'keyname2': 'value' ],
#                           ],
#                 'device': [
#                           ]
#               }
#
class ParseConfigFile:
    m_name = ""
    m_resources = {}
    def __init__(self, filename):
        self.m_name = filename
        self.read()
    def resources(self):
        return self.m_resources
    def read(self):
        f = open(self.m_name, 'r')
        is_bracket_opened = False
        is_bracket_closed = True
        resource = {}
        is_res_found = False
        for raw_line in f.readlines():
            #print(raw_line)
            raw_line = raw_line.split('#', 1)[0].strip()
            if not len(raw_line): continue
            print(raw_line)
            if '{' in raw_line:
                res_name = raw_line.split('{', 1)[0].strip()
                is_bracket_opened = True
                is_bracket_closed = False
                is_res_found = True
                continue
            if '}' in raw_line:
                is_bracket_closed = True
                is_bracket_opened = False
                #print(resource)
                if is_res_found:
                    if res_name not in self.m_resources: self.m_resources[res_name] = []
                    self.m_resources[res_name].append(deepcopy(resource))
                    resource = {}
                    res_name = None
                    is_res_found = False
                continue
            if is_bracket_opened and not is_bracket_closed:
                keyname = raw_line.split('=', 1)[0].strip()
                value = raw_line.split('=', 1)[1].strip()
                if value[0] == value[-1] and value[0] == '"':
                    value = value[1:-1]
                if value[-1] == ";":
                    value = value[0:-1]
                if keyname not in resource: resource[keyname] = []
                resource[keyname].append(value)
        pass

if __name__ == "__main__":
#    p = ParseConfigFile("%s/%s" % (BACULA_DIR, BACULA_DIRECTOR_CONF))
#    print(p.resources())
    import sys
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
        p = ParseConfigFile(config_file)
        print(p.resources())
    else:
        print("No data available")


