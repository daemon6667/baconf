#!/usr/bin/env python


#from config import *
from copy import deepcopy
NodeData   = 1
NodeSubset = 2
NodeType = [ NodeData, NodeSubset, ]


class ParseConfigFile:
    m_resources = {} 
    m_listdata = []
    def resources(self): return self.m_resources
    def read(self, configfile):
        """
        Returns content of the delivered config file
        """
        result = ""
        fd = None
        try:
            fd  = open(configfile, 'r')
        except:
            print("ERROR: Opening config file '%s'" % configfile)

        if fd:
            configtext = fd.read()
            special_c = [ ';', '\n', '#', '{', '}', '"', "'", ]
            #print(configtext)
            is_block_started = False
            is_comment = False
            is_string = False
            subset = []
            wordbuffer = ""
            is_keyname_found = False
            def add_option(data):
                if len(data):
                    self.m_listdata.append(data.strip())
                """
                if len(subset):
                    if subset[-1] is dict: subset[-1][op_name] = None
                    elif subset[-1] is list: subset[-1].append(op_name)
                else:
                    subset.append(op_name)
                """
            for raw_line in configtext:
                line_1 = raw_line.split('#', 1)[0].strip()

                # Cutting name of an option name
                if raw_line in ['=', ] and not is_string:
                    add_option(wordbuffer)
                    wordbuffer = ""
                    #print(keyname)
                    if not is_keyname_found: 
                        is_keyname_found = True
                    add_option('=')
                    continue
                """
                if raw_line in ['"', ]:
                    if is_string:
                        print "String added %s" % wordbuffer
                        add_option(wordbuffer)
                        self.is_string = False
                    else:
                        is_string = True
                    continue
                """
                if raw_line in [" ", ] and not is_string: 
                    continue
                if raw_line in ['#', ]: 
                    is_comment = True
                    if len(wordbuffer):
                        add_option(wordbuffer)
                    continue
                if raw_line in ['\n', ]: 
                    if is_comment: 
                        is_comment = False 
                    else:
                        add_option(wordbuffer)
                    wordbuffer = ""
                    continue
                if raw_line in ['{', '}', ]:
                    is_keyname_found = False
                    add_option(wordbuffer)
                    add_option(raw_line)
                    wordbuffer = ""
                    continue
                """
                if raw_line in ['{', ]:
                    add_option(wordbuffer)
                    wordbuffer = ""
                    is_block_started = True
                    continue
                if raw_line in ['}', ]:
                """
                """
                if raw_line in ['"', ]: 
                    if len(wordbuffer) and wordbuffer[-1] != '\\':
                        if is_string:
                            pass
                        else:
                            is_string = True
                        continue
                """
                wordbuffer += raw_line
            #print self.m_listdata 
            fd.close()
        return self.m_listdata
            

if __name__ == "__main__":
    import sys
    p = ParseConfigFile()
    p.read(sys.argv[1])

