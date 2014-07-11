#!/usr/bin/env python


class Resources:
    m_name = ""
    m_data = {}
    def __init__(self, config_file):
        self.m_name = config_file
    
    def parse(self):
        fd = open(self.m_name, "r")
        section = ""
        for raw_line_1 in fd.readlines():
            raw_line = raw_line_1.strip()
            if raw_line[0] == "#" or not len(raw_line): continue
            if not raw_line.count('='): continue
            if raw_line[0] == '[' and key_line[-1] == ']':
                section = raw_line[1:-2]
                print(section)
                self.m_data[section] = {}
                continue
            print(raw_line)
            if len(section):
                keyoption = raw_line.split('=', 0)[0]
                options = raw_line.split('=', 0)[1]
                self.m_data[section][keyoption] = {} 
                for pair in options.split(','):
                    key=pair.split('=', 1)[0]
                    value=pair.split('=', 1)[1]
                    self.m_data[section][keyoption][key] = value
        fd.close()
        pass

    def listSections(self):
        result = []

        return result

if __name__ == "__main__":
    r = Resources('resourceslist.tpl')
    r.parse()
    print r.m_data

