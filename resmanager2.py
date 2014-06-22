#!/usr/bin/env python_

from resourceclient import ResourceClient
from resourceclient import ResourceDevice
from resourceclient import ResourceStorage
from resourceclient import ResourceDirector
from resourceclient import ResourceMessages
from resourceclient import ResourceCatalog
from resourceclient import ResourcePool
from resourceclient import ResourceJob
from resourceclient import ResourceFileSet
from resourceclient import ResourceSchedule
from resourceclient import ResourceConsole

from parser2 import ParseConfigFile as Parser
from coreres import *
from copy import deepcopy
import json

RESCLASSES = {  
    RESCLASS_CLIENT   : { 'label': 'Client'   , 'class': ResourceClient   , 'resource': OPTION_TYPE_RESOURCE_CLIENT },
    RESCLASS_DEVICE   : { 'label': 'Device'   , 'class': ResourceDevice   , 'resource': OPTION_TYPE_RESOURCE_DEVICE },
    RESCLASS_STORAGE  : { 'label': 'Storage'  , 'class': ResourceStorage  , 'resource': OPTION_TYPE_RESOURCE_STORAGE },
    RESCLASS_DIRECTOR : { 'label': 'Director' , 'class': ResourceDirector , 'resource': OPTION_TYPE_RESOURCE_DIRECTOR },
    RESCLASS_MESSAGE  : { 'label': 'Messages' , 'class': ResourceMessages , 'resource': OPTION_TYPE_RESOURCE_MESSAGES },
    RESCLASS_CATALOG  : { 'label': 'Catalog'  , 'class': ResourceCatalog  , 'resource': OPTION_TYPE_RESOURCE_CATALOG },
    RESCLASS_POOL     : { 'label': 'Pool'     , 'class': ResourcePool     , 'resource': OPTION_TYPE_RESOURCE_POOL },
    RESCLASS_JOB      : { 'label': 'Job'      , 'class': ResourceJob      , 'resource': OPTION_TYPE_RESOURCE_JOB },
    RESCLASS_FILESET  : { 'label': 'FileSet'  , 'class': ResourceFileSet  , 'resource': OPTION_TYPE_RESOURCE_FILESET },
    RESCLASS_SCHEDULE : { 'label': 'Schedule' , 'class': ResourceSchedule , 'resource': OPTION_TYPE_RESOURCE_SCHEDULE },
    RESCLASS_CONSOLE  : { 'label': 'Console'  , 'class': ResourceConsole  , 'resource': OPTION_TYPE_RESOURCE_CONSOLE },
}

ResourcesList = {
    RESCLASS_CLIENT   : ResourceClient,
    RESCLASS_DEVICE   : ResourceDevice,
    RESCLASS_STORAGE  : ResourceStorage,
    RESCLASS_DIRECTOR : ResourceDirector,
    RESCLASS_MESSAGE  : ResourceMessages,
    RESCLASS_CATALOG  : ResourceCatalog,
    RESCLASS_JOB      : ResourceJob,
    RESCLASS_FILESET  : ResourceFileSet,
    RESCLASS_SCHEDULE : ResourceSchedule,
    RESCLASS_CONSOLE  : ResourceConsole,
}

class Stack:
    m_values = {}
    m_icount = -1
    def push(self, value):
        self.mi_icount =+ 1
        self.m_values[m_icount] = value 
    def pop(self):
        result = self.m_values[self.m_icount]
        self.m_values[self.m_icount]
        self.m_icount =- 1
        return result

class MakeResourcesFromConfig:
    m_list_resources = []
    def __init__(self, list_parsed_data):
        self.building(list_parsed_data)
        pass
    def building(self, list_parsed_data):
        for res in RESCLASSES.keys():
            resources_names[RESCLASSES[res]['label'].lower()] = res
        op1 = ""
        op2 = ""
        resource
        for item in list_parsed_data:
            if not len(op1):
                op1 = item
                continue
            if not len(op2):
                op2 = item
            if len(op1) and len(op2):
                if op2 == "{" and op1 in resources_names:
                    resource = RESCLASS[op1]['class']('')


class ResourceBuilder:
    m_list_config_files = []
    """ m_list_resources stores a list of objects of identified resources """
    m_list_resources = {}
    def __init__(self, list_config_files):
        self.m_list_config_files = list_config_files

    def readConfigFiles(self):
        """
        Reads every listed in the constructor file
        """
        for f in self.m_list_config_files:
            py_data = self.readConfigFile(f)
            for res_item in py_data:
                try:
                    self.m_list_resources[res_item]
                except KeyError:
                    self.m_list_resources[res_item] = []
                self.m_list_resources[res_item] = (py_data[res_item])
        #print json.dumps(self.m_list_resources, indent=2)
        return self.m_list_resources

    def readConfigFile(self, filename):
        """
        Reads config file and adds its converted to python data content to m_list_resources
        """
        py_data = self.buildPythonDataFromConfig(Parser().read(filename))
#        print py_data
        return py_data

    def buildPythonDataFromConfig(self, list_parsed_data):
        """
        The function parsers the provided file and returns list of detected config options
        """
        idx = 0
        def convertStrToObject(sublist_of_values, is_top = False):
            key_name = None
            key_value = None
            resource = {}
            is_tag = False
            i_counter = 0
            while (i_counter < len(sublist_of_values)):
                item = sublist_of_values[i_counter]
                if   item in [ "{", ]:
                    key_name = sublist_of_values[i_counter-1]
                    (new_i_counter, tmp_res) = convertStrToObject(sublist_of_values[i_counter+1:])
                    i_counter += new_i_counter
                    # resource[key_name] = [ tmp_res, ] if is_top else tmp_res
                    try:
                        resource[key_name]
                    except:
                        resource[key_name] = []
                    resource[key_name].append(tmp_res)
                elif item in [ "}", ]: 
                    i_counter += 1
                    break
                elif item in [ '=', ]:
                    is_tag = True
                elif key_name and is_tag:
                    key_value = item
                    if key_name in resource:
                        if type(resource[key_name]) is list:
                            resource[key_name].append(item)
                        elif type(resource[key_name]) is str:
                            prev = resource[key_name]
                            resource[key_name] = [prev, item]
                    else:
                        resource[key_name] = ( item )
                    key_name = None
                    key_vaue = None
                    is_tag = False
                else:
                    key_name = item
                i_counter += 1
            return (i_counter, resource)
        (number, resource) = (convertStrToObject(list_parsed_data, True))
        return resource


if __name__ == "__main__":
    import os, sys
    input_file = sys.argv[1]
    if not os.path.exists(input_file):  
        print("ERROR: Input file [%s] doesn't exist" % input_file)
        exit(1)
    r = ResourceBuilder(sys.argv[1:])
    r.readConfigFiles()

