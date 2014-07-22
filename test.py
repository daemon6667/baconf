#!/bin/bash

import json

def make_dict(buffer, str_data, value):
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
                buffer[key] = {}
                make_dict(buffer[key], str_data[cur_pos:], value)
                return
            continue
        if c in [']', ] and tag_open:
            tag_close = True            
            buffer[key] = ""
            if cur_pos == len(str_data)-1:
                #print("Added key: %s" % key)
                buffer[key] = value
            else:
                buffer[key] = {}
                make_dict(buffer[key], str_data[cur_pos+1:], value)
                return
            key = ""
            tag_close = False
            tag_open = False
            continue
        key += c
        if cur_pos == len(str_data) - 1:
            if len(key):
                buffer[key] = value

def merge(d1, d2, mode=0):
    if not type(d2) is dict:
        raise Exception("d2 is not a dict")

    if not type(d1) is dict:
        if mode == 0:
            raise Exception("d1 is not a dict")
        return d2

    result = dict(d1)

    for k, v in d2.iteritems():
        if k in result and type(v) is dict:
            result[k] = merge(result[k], v, 1)
        else:
            if mode == 1:
                result.update(d2)
            else:
                result[k] = v
    return result


if __name__ == "__main__":
    data = [
        ('record[unmountcommand]', '=', ''),
        ('record[removablemedia]', '=', '0'),
        ('record[alwaysopen]', '=', '0'),
        ('record[maximumblocksize]', '=', ''),
        ('record[maximumvolumesize]', '=', '321142'),
        ('record[randomaccess]', '=', '0'),
        ('record[maximumfilesize]', '=', '546354654'),
        ('record[autoselect]', '=', '0'),
        ('record[specific_namespace][id]', '=', 'default'),
        ('record[changerdevice]', '=', ''),
        ('record[alertcommand]', '=', ''),
        ('record[blockchecksum]', '=', '0'),
        ('record[requiresmount]', '=', '0'),
        ('record[mountpoint]', '=', ''),
        ('record[specific_namespace][hidden]', '=', 'false'),
        ('record[autochanger]', '=', '0'),
        ('record[changercommand]', '=', ''),
        ('record[mediatype]', '=', ''),
        ('record[maximumchangerwait]', '=', ''),
        ('record[maximumopenwait]', '=', ''),
        ('record[maximumrewindwait]', '=', ''),
        ('record[devicetype][0][text]', '=', 'File'),
        ('record[devicetype][0][id]', '=', 'File'),
        ('record[minimumblocksize]', '=', ''),
        ('record[mountcommand]', '=', ''),
        ('cmd', '=', 'save-record'),
        ('record[name]', '=', 'dsafsd'),
        ('record[archivedevice]', '=', ''),
        ('recid', '=', '0'),
        ('record[specific_enabled]', '=', 'true'),
        ('record[specific_namespace][text]', '=', 'default'),
        ('record[driveindex]', '=', ''),
        ('record[maximumconcurrentjobs]', '=', ''),
    ]
    buffer = {}
    for item in data:  
        key, tmp, value = item
        print(item)
        temp_buf = {}
        make_dict(temp_buf, key, value)
        buffer = merge(buffer, temp_buf)
    print(json.dumps(buffer, indent=4))


