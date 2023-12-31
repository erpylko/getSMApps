# getSMApps

_Get applications installed from devices with Meraki Systems Manager_

---

This python program leverages APIs to the Meraki dashboard to pull all the software installed on all the devices. Output can be a list of all the software or a list of software per machine. Filtering can be accomplished by a file that includes applications to ignore (one per line)

## Features

* Progress bar because the querying the dashboard can be slow
* No error checking. Get your command line options right 
* API key can be specified via environment variable, CLI, or variable

## Solution Components

This app leverages the following APIs and packages:
 * meraki v1.34.0 for access to the dashboard
 * plac v1.3.5 for CLI option parsing
 * alive-progress v3.1.4 for progress bar

### Cisco Products / Services

* This uses the Meraki Dashboard and a Systems Manager network

## Usage

usage: getsw.py [-h] [-a APIKEY] [-n NET] [-p PC] [-i IGNORE] {apps,system}

Report apps in a Meraki Systems Manager network

positional arguments:<br>
&emsp;{apps,system}         Sort by apps or system

options:<br>
&emsp;-h, --help                    show this help message and exit<br>
&emsp;-a APIKEY, --apikey APIKEY    Dashboard API KEY<br>
&emsp;-n NET, --net NET             Network ID<br>
&emsp;-p PC, --pc PC                List apps for 1 pc<br>
&emsp;-i IGNORE, --ignore IGNORE    List of apps to ignore<br>

## Installation

Required packages can be installed with pip install -r requirements.txt
