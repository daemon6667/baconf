#!/usr/bin/env python

# -*- coding: utf-8 -*-
import sys, os, json
from bottle import post, route, run, request, template, response, redirect, static_file
from resmanager2 import ResourceBuilder
from resourcesconf import DefResources
from htmladd import HtmlFormAddResource
from storage import Storage
basedir = "/".join(os.path.abspath(sys.argv[0]).split('/')[0:-1])
filedefs = "%s/resources.def" % basedir
template_main = "html/main"
storagename = "super.db"


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

@post("/htmladd/<resource>/save")
def htmladd_resource_save(resource):
    import re
    data = {}
    restype = ""
    for key, value in (request.forms.allitems()):
	print(key, '=', value)
       # print(" Source key: ", key)
       # m = re.match('^(record)\[(\w+)\]$', key)
       # if m:
        #    data.append(m.groups()[1] + '=' + value)
#            print('Found: ', m.groups(), '=', value)
            #data[m.groups()[1]] = value
	#print(key, value)
    print(json.dumps(",".join(data)))
    return ""
    # print(request.params.get('record'))
    for (key, value) in request.forms.allitems():
        if key.startswith('record['):
            data[key[7:-1]] = value
        elif key == 'name':
            restype = value[5:]
#    print(data, restype)
    s = Storage(storagename)
    response['status'] = 'success'
    save_result = s.saveResource('default', data['name'], restype, json.dumps(data))
    if not save_result:
        response['status'] = 'error'
        response['message'] = 'The resources item was not saved'
    return response

@post("/resources")
def resources_list():
    data = Storage(storagename).listResources()
    send_data = {
        "status": "success",
        "total": len(data),
        "records": data
    }
    return  json.dumps(send_data)

@route("/get/namespaces")
def get_namespaces():
    return json.dumps(Storage(storagename).namespaces())

@route("/htmladd/<resource>/html")
def htmladd_resource_html(resource):
    return HtmlFormAddResource(DefResources(filedefs)).makeHtml(resource)

@route("/htmladd/<resource>/js")
def htmladd_resource_js(resource):
    namespaces = Storage(storagename).namespaces()
    if not len(namespaces): 
        namespaces = ['default', ]
    return HtmlFormAddResource(DefResources(filedefs)).makeJS(resource, json.dumps(namespaces))

@route("/html/<file>")
def static_uri(file):
    return static_file(file, root='html')

@route("/def/resource")
def def_resources():
    result = {'data': resourcesOptions().sections(), 'success': True}
    return json.dumps(result)

@route("/def/resource/<resource>")
def def_resource(resource):
    result = {'data': resourcesOptions().section(resource), 'success': True}
    return json.dumps(result)

@route("/def/resource/<resource>/<attr>/values")
def list_possiblevalues(resource, attr):
    return json.dumps(resourcesOptions().list_possiblevalues(resource, attr))


if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
    pass

