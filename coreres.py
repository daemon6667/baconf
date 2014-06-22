#!/usr/bin/env python

from parser import ParseConfigFile
OPTION_TYPE_INT               = 1
OPTION_TYPE_STR               = 2
OPTION_TYPE_IPADDR            = 3
OPTION_TYPE_ENUM              = 4
OPTION_TYPE_SIZE              = 5 # it's for B, Kb, Mb, Gb
OPTION_TYPE_BOOL              = 6
OPTION_TYPE_RESOURCE_STORAGE  = 7
OPTION_TYPE_RESOURCE_CLIENT   = 8
OPTION_TYPE_RESOURCE_DEVICE   = 9
OPTION_TYPE_RESOURCE_POOL     = 10
OPTION_TYPE_RESOURCE_DIRECTOR = 11
OPTION_TYPE_RESOURCE_MESSAGES = 12
OPTION_TYPE_RESOURCE_JOB      = 13
OPTION_TYPE_RESOURCE_CATALOG  = 14
OPTION_TYPE_RESOURCE_CONSOLE  = 15
OPTION_TYPE_RESOURCE_FILESET  = 16
OPTION_TYPE_RESOURCE_SCHEDULE = 17
OPTION_TYPE_SCHEDULE          = 18
OPTION_TYPE_SUBRESOURCE       = 19

RESCLASS_CLIENT     = 1
RESCLASS_JOB        = 2
RESCLASS_POOL       = 3
RESCLASS_DEVICE     = 4
RESCLASS_STORAGE    = 5
RESCLASS_DIRECTOR   = 6
RESCLASS_MESSAGE    = 7
RESCLASS_CATALOG    = 8
RESCLASS_JOB        = 9
RESCLASS_FILESET    = 10
RESCLASS_SCHEDULE   = 11
RESCLASS_CONSOLE    = 12


RESOURCE_DEVICE_TYPE_FILE   = 1
RESOURCE_DEVICE_TYPES       = { RESOURCE_DEVICE_TYPE_FILE: 'File', }
RESOURCE_POOL_TYPE_BACKUP   = 1
RESOURCE_POOL_TYPE_RESTORE  = 2
RESOURCE_POOL_TYPES         = { RESOURCE_POOL_TYPE_BACKUP: 'Backup', RESOURCE_POOL_TYPE_RESTORE: 'Restore' }

MultipleValue       = False
SingleValue         = True
NonRequiredOption   = False
RequiredOption      = True

class ResourceOptionAbstract:
    m_name = ""
    m_type = ""
    m_value = []
    m_is_single = SingleValue
    m_is_required = RequiredOption
    def __init__(self, rname, rtype, is_required = RequiredOption, is_rsingle = SingleValue, rvalue = []):
        self.m_name = rname
        self.m_type = rtype
        self.m_value = self.setValue(rvalue)
        self.m_is_required = is_required
        self.m_is_single = is_rsingle
    def name(self): return self.m_name
    def type(self): return self.m_type
    def value(self): return self.m_value
    def is_required(self): return self.m_is_required
    def normalizeSingleMultiple(self, value):
        """
        Makes a list if the option is a list type.
        Makes a single value if the option must have a single value
        """
        result = value
        if self.m_is_single and type(value) is list:
            result = value[0]
        if not self.m_is_single and type(value) is not list:
            result = [value, ] 
        return result
    def setValue(self, value):
        t_val = self.normalizeSingleMultiple(value)
        if self.m_type == OPTION_TYPE_BOOL:
            if str(t_val).lower() in ['yes', 'true', True ]:
                self.m_value = True
            elif str(t_val).lower() in ['no', 'false', False ]:
                self.m_value = False
            else:
                print("WARNING: Option [%s, is_single = %s] doesn't have correct value [%s]" % (self.m_name, self.m_is_single, value))
        else:
            self.m_value = t_val
        #print("Assigned value (setValue) to %s is %s" % (self.m_name, self.m_value))
    def is_single(self): return self.is_single
    def print_plain(self):
        value = self.m_value
        if self.m_type == OPTION_TYPE_BOOL:
            value = 'Yes' if self.m_value else 'No'
        if self.m_type in [ OPTION_TYPE_STR, OPTION_TYPE_IPADDR, ]:
            value = '"%s"' % value
        #print("Assigned value (print_plain) to %s is %s" % (self.m_name, value))
        return ("%-30s = %s" % (self.m_name, value if len(str(value)) else '""'))

class ResourceAbstract:
    """
    The class describes a Resource object to as one described at bacula config files
    """
    m_name = ""
    m_type = ""
    m_options = []
    m_options_names = []
    m_class = 0
    def __init__(self, name, rclass):
        self.m_name = name
        self.m_class = rclass
        self.addOption('Name', OPTION_TYPE_STR, RequiredOption, SingleValue, name)
    def option(self, name):
        result = None
        for op in self.m_options.keys():
            if op.lower() == name.lower():
                result = op
                break
        return result
    def listOptions(self):
        """
        Returns list of names of options defined in the object
        """
        result = []
        for op in self.m_options:
            result.append(op.name())
        return result
    def option(self, name):
        """
        Returns the object option if it was found, overwise None object
        """
        result = None
        for op in self.m_options:
            if op.name().lower() == name.lower():
                result = op
        return result
    def addOption(self, rname, rtype, is_required = RequiredOption, is_rsingle = True, rvalue = []):
        self.m_options.append(ResourceOptionAbstract(rname, rtype, is_required, is_rsingle, rvalue))
        self.m_options_names.append(rname.lower())
    def setValue(self, option_name, option_value):
#        print("Trying to set [%s] for [%s]" % (option_value, option_name))
        try:
            self.option(option_name).setValue(option_value)
        except:
            print("WARNING: Option [%s] didn't find to assign new value [%s]" % (option_name, option_value))
    def print_conf(self):
        from resmanager import RESCLASSES
        options = ""
        for op in self.m_options:
            if not op.is_required() and op.value() == None: continue
            options = "%s\n    %s" % (options, op.print_plain())
        conf = """
%s {%s
}
""" % (RESCLASSES[self.m_class]['label'], options)
        print(conf)
    

if __name__ == "__main__":
    pass

