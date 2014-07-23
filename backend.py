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
    postdata = unpack_postdata(request.forms.allitems())
    print(json.dumps(postdata, indent=4))

    response['status'] = 'success'
    if postdata['cmd'] == 'save-record':
        s = Storage(storagename)
        save_result = s.saveResource(postdata['record']['specific_namespace']['text'], 
                                     postdata['record']['name'], 
                                     postdata['restype'],
                                     json.dumps(postdata['record']))
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
    for item in request.forms.allitems():
        print(item)
    postdata = unpack_postdata(request.forms.allitems())
    print(json.dumps(postdata, indent=4))
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

def convert_postdata(buff, str_data, value):
    #print("  >> Source: ", str_data)
    key = ""
    tag_open = False
    tag_close = False
    cur_pos = -1

    while cur_pos < len(str_data)-1:
        cur_pos += 1
        c = str_data[cur_pos]
        if c in ['[', ]:
            tag_open = True
            if len(key):
                buff[key] = {}
                convert_postdata(buff[key], str_data[cur_pos:], value)
                return
        elif c in [']', ] and tag_open:
            tag_close = True
            if cur_pos == len(str_data) - 1:
                if not len(key): key = "_"
                buff[key] = value
                continue
            else:
                buff[key] = {}
                convert_postdata(buff[key], str_data[cur_pos+1:], value)
                return
            key = ""
            tag_close = False
            tag_open = False
        else:
            key += c
        
        if cur_pos == len(str_data) - 1:
            buff[key] = value
        
def unpack_postdata(listdata):
    def merge_dicts(d1, d2, mode=0):    
        if not type(d2) is dict:
            raise Exception("d2 is not a dict")
    
        if not type(d1) is dict:
            if mode == 0:
                raise Exception("d1 is not a dict")
            return d2
    
        result = dict(d1)
    
        for k, v in d2.iteritems():
            if k in result and type(v) is dict:
                print("Key %s = %s" % ( k, v ))
                result[k] = merge_dicts(result[k], v, 1)
            else:
                if mode == 1:
                    print("Result=%s, dict=%s" % (result, d2))
                    for k2 in result:
                        if k2 in d2 and type(result[k2]) is not list:
                            result[k2] = [result[k2], ]
                    result.update(d2)
                else:
                    if k in result:
                        if type(result[k]) != list:
                            result[k] = [result[k], v]
                        else:
                            result[k].append(v)
                    else:
                        result[k] = v
        return result
    buffer = {}
    for longkey, value in listdata:
        temp_buffer = {}
        convert_postdata(temp_buffer, longkey, value)
        buffer = merge_dicts(buffer, temp_buffer)
    return buffer

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
    pass

