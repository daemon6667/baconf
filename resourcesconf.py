#!/usr/bin/env python


class DefResources:
    m_name = ""
    m_data = {}
    def __init__(self, config_file):
        self.m_name = config_file
        self.parse()
    
    def parse(self):
        fd = open(self.m_name, "r")
        section = ""
        for raw_line_1 in fd.readlines():
            raw_line = raw_line_1.strip()
            if not len(raw_line) or raw_line[0] == "#": continue
            if raw_line[0] == '[' and raw_line[-1] == ']':
                section = raw_line[1:-1]
                self.m_data[section] = {}
                continue
            if len(section):
                keyoption = raw_line.split('=', 1)[0].strip().replace('  ', ' ')
                options = raw_line.split('=', 1)[1].strip()
                self.m_data[section][keyoption] = {} 
                for pair in options.split(' '):
                    key=pair.split('=', 1)[0]
                    value=pair.split('=', 1)[1]
                    self.m_data[section][keyoption][key] = value
        fd.close()

    def sections(self):
        return self.m_data.keys() 

    def section(self, section):
        result = None
        for x in self.m_data.keys():
            if x.lower() == section.lower():
                result = self.m_data[x]
        return result

    def attrs(self, section):
        result = None
        if self.has_section(section):
            result = self.m_data[section]
        return result

    def has_attr(self, section, attr):
        result = False
        if self.has_section(section):
            for x in self.section(section).keys():
                if x.lower() == attr.strip().lower():
                    result = True
                    break
        return result

    def attr_properties(self, section, attr):
        result = None
        for x in self.attrs(section):
            if x.lower() == attr.lower():
                result = self.attrs(section)[x]
                break
        return result
    
    def list_possiblevalues(self, section, attr):
        result = []
        if (self.has_attr(section, attr) and 'possiblevalues' in self.attr_properties(section, attr)):
            result = [ x.strip() for x in self.attr_properties(section, attr)['possiblevalues'].split(',') ]
        return result

    def has_section(self, section):
        return self.section(section) != None

#if __name__ == "__main__":
#    r = DefResources('resources.def')
#    print r.sections()
#    print r.attrs('Director')
#    print r.options('Director', 'Address')
#    print r.section('Director')
#
