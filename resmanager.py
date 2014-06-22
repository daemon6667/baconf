#!/usr/bin/env python

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

from parser import ParseConfigFile
from coreres import *
from copy import deepcopy

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


class ResourceBuilder:
    m_list_config_files = []
    """ m_list_resources stores a list of objects of identified resources """
    m_list_resources = {}
    def __init__(self, list_config_files):
        self.m_list_config_files = list_config_files

    def buildResourceFromConfig(self, config_file):
        parser = ParseConfigFile(config_file)
        for res_name in parser.resources().keys():
            for res in RESCLASSES:
                if RESCLASSES[res]['label'] == res_name:
                    print("Resource class "  +res_name)
                    for list_resources_of_a_class in parser.resources()[res_name]:
                        newres = RESCLASSES[res]['class']('')
                        for res_instance in list_resources_of_a_class:
                            #print(res_instance, " = ", list_resources_of_a_class[res_instance])
                            #print(res_instance, list_resources_of_a_class[res_instance])
                            newres.setValue(res_instance, list_resources_of_a_class[res_instance])
#                            print(newres.option(res_instance).print_plain())
                        newres.print_conf()



if __name__ == "__main__":
    import os, sys
    input_file = sys.argv[1]
    if not os.path.exists(input_file):  
        print("ERROR: Input file [%s] doesn't exist" % input_file)
        exit(1)
    r = ResourceBuilder([input_file, ])
    r.buildResourceFromConfig(input_file)
    for rr in r.m_list_resources:
        rr.print_conf()
     
