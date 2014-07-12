#!/usr/bin/env python

# -*- coding: utf-8 -*-
import sys, os, json
#import ConfigParser
from bottle import post, route, run, request, template, response, redirect, static_file
from resmanager2 import ResourceBuilder
from resourcesconf import DefResources
basedir = "/".join(os.path.abspath(sys.argv[0]).split('/')[0:-1])
filedefs = "%s/resources.def" % basedir
template_main = "html/main"


def jsonData():
    result = ResourceBuilder([ "%s/%s" % (basedir, "all.bacula"), ]).readConfigFiles()
    return result

def resourcesOptions():
    return DefResources(filedefs) 
    
jdata = jsonData()
known_resources = resourcesOptions()

@route("/")
def html_main():
    return template(template_main)

@route("/def/resource")
def def_resources():
    result = {'data': resourcesOptions().sections(), 'success': True}
    return json.dumps(result)

@route("/def/resource/<resource>")
def def_resource(resource):
    result = {'data': resourcesOptions().section(resource), 'success': True}
    return json.dumps(result)

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True, reloader=True)
    pass

