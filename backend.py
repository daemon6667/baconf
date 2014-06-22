#!/usr/bin/env python

# -*- coding: utf-8 -*-
import sys, os, json
import ConfigParser
from bottle import post, route, run, request, template, response, redirect, static_file
from resmanager2 import ResourceBuilder
basedir = "/".join(os.path.abspath(sys.argv[0]).split('/')[0:-1])
filedefs = "%s/resources.def" % basedir
template_main = "html/main"


def jsonData():
    result = ResourceBuilder([ "%s/%s" % (basedir, "all.bacula"), ]).readConfigFiles()
    return result

def resourcesOptions():
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.readfp(open(filedefs))
    return config
    
jdata = jsonData()
known_resources = resourcesOptions()


@route("/")
def html_main():
    return template(template_main)

@route("/get/resource")
def list_resources():
    return json.dumps({'data': [ x for x in jdata ], 'success': True})

@route("/get/resource/<resource>")
def list_of_resource(resource):
    result = {'success': False}
    for x in jdata:
        if x.lower() == resource.lower():
            result['data'] = jdata[x]
            result['success'] = True
            break
    return json.dumps(result)

@route("/defs/resource")
def known_resources():
    result = {'data': resourcesOptions().sections(), 'success': True}
    return json.dumps(result)

#@route("/defs/resource/<resource>")
#def known_resource_options(resource):
#    result = {'success': False, }
#    res_conf = resourcesOptions()
#    if res_conf.has_section(resource):
#        result['success'] = True
#        result['data'] = res_conf.options(resource)
#    return json.dumps(result)

@route("/defs/resource/<resource>")
def know_resource_attributes(resource):
    result = {'success': False, }
    res_conf = resourcesOptions()
    if res_conf.has_section(resource):
        result['success'] = True
        list_options = {}
        for optname, attrs in res_conf.items(resource):
            values = {}
            for a in  (x.strip() for x in attrs.split(' ')):
                key = a.split('=', 1)[0].strip()
                value = a.split('=', 1)[1].strip()
                values[key] = value
            if 'Type' in values:
                if 'PossibleValues' in values:
                    values['PossibleValues'] = values['PossibleValues'].split(',')
                elif values['Type'] == 'Bool' and 'Default' in values:
                    values['Default'] = True if values['Default'].lower() in ['yes', 'true', ] else False
                elif values['Type'] in ['Integer', 'FSize', 'Duration'] and 'Default' in values:
                    values['Default'] = int(values['Default'])
                elif 'Required' in values:
                    values['Required'] = True if values['Required'].lower() in ['yes', 'true', ] else False
            list_options[optname] = values
        result['data'] = { resource: list_options }
    return json.dumps(result)

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True, reloader=True)
    pass

