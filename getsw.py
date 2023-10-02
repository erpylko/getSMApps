#!/usr/bin/env python3

"""
Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

#
# an app to return all the programs on a Meraki Systems Manager network
#
# you need an API key as well as network ID for a systems manager network
# 
import meraki
import plac
from alive_progress import alive_it
import os
import time


#
# The API key and network ID can be used multiple ways.
#
#   - specified as environment variable
#   - specified on cli
#   - specified in app
#
# That list is least relevant to most relevant. If both an environment
# variable is set and the API_KEY variable is set, the program will use
# the locally set variable
#
#API_KEY = ''
#NET_ID  = ''

#
# only print things if quiet has not been set
#
def qprint(quiet, text):
    if not quiet:
        print(text)

#
# read in the app names to ignore
# file has one app name/line
#
def ignoreList(textfile):
    appList = set()

    ignore = open(textfile, 'r')

    for app in ignore:
        appList.add(app.strip())

    ignore.close()

    return (appList)

#
# API keys and network IDs can be specified through environment variables,
# global variables, or the CLI. Most specific to least specific is:
# CLI -> Global Variable -> environment variable
#
def setKey(key):
    g = globals()
  
    if key in g:
        return g[key]
    else:
        return os.environ.get(key)

#
# command line options/descriptions
#
@plac.pos('SORT',   "Sort by apps or system", choices=['apps', 'system'])
@plac.opt('apikey', "Dashboard API KEY",      type=str)
@plac.opt('net',    "Network ID",             type=str)
@plac.opt('pc',     "List apps for 1 pc",     type=str)
@plac.opt('ignore', "List of apps to ignore", type=str)
@plac.flg('quiet',  "Only output apps"                )
def main(SORT, apikey, net, pc, ignore, quiet):
    """Report apps in a Meraki Systems Manager network"""
    
    if apikey is None:
        apikey = setKey('API_KEY')

    if apikey is None:
        print("Need to set APIKEY. Exiting.")
        exit ()

    if net is None:
        net = setKey('NET_ID')

    if net is None:
        print("Need to set NET_ID. Exiting.")
        exit ()

    if ignore is None:
        sysapps = set()
    else:
        sysapps = ignoreList(ignore)

    # create dashboard object
    qprint(quiet, "Connecting to Meraki Dashboard...")
    dashboard = meraki.DashboardAPI(apikey, output_log=False, suppress_logging=True)
  
    # get a list of all devices

    qprint(quiet, "Gathering devices...")
    device_list = dashboard.sm.getNetworkSmDevices(net)

    # create a list that includes device name, id, apps
    devices=[]

    # aggregate all software into one set (no dups in sets)
    all_software = set()

    # iterate through all devices, build the list of all software in the net
    for device in alive_it(device_list, length=25, title='Processing PC', disable=quiet):
        name = device['name']

        # skip all the machines except the one specified on the command line
        if pc is not None:
            if pc != name:
                continue

        # create a set of software for a given device
        id = device['id']
        pcsw = set()

        # get the installed software for a host
        softwares = dashboard.sm.getNetworkSmDeviceSoftwares(net, id)

        # iterate through all the software and add it to the device list and all s/w seen
        for software in softwares:
            swname = software['name']
            pcsw.add(swname)
            all_software.add(swname)

        # add the device, id, and list of software to the device list for easier printing
        devices.append((name, id, pcsw))

    # use set math to easily remove apps that we don't want to see (if any)
    if SORT == 'apps':
        qprint (quiet, "Apps on systems")
        for app in sorted(all_software - sysapps):
            print("  ",app)
    else:
        for (name,id,pcsw) in sorted(devices):
            qprint(quiet, name)
            for item in sorted(pcsw - sysapps):
              print("  ",item)

    pass

if __name__ == '__main__':
    plac.call(main)

