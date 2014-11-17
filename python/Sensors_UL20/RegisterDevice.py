#!/usr/bin/env python

# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
# 
# This file is part of FIGWAY software (a set of tools for FIWARE Orion ContextBroker and IDAS2.6).
#
# FIGWAY is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as 
# published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# FIGWAY is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with FIGWARE. 
# If not, see http://www.gnu.org/licenses/
#
# For those usages not covered by the GNU Affero General Public License please contact with: Carlos Ralli Ucendo [ralli@tid.es] 
# Developed by Carlos Ralli Ucendo (@carlosralli), Nov 2014.


import requests, json
import ConfigParser
import io
import sys

CONFIG_FILE = "../config.ini"

NUM_ARG=len(sys.argv)
COMMAND=sys.argv[0] 

if NUM_ARG==3:
   SENSOR_TYPE=sys.argv[1]
   SENSOR_NAME=sys.argv[2]
else:
   print 'Usage: '+COMMAND+' [DEV_TYPE] [DEV_NAME]'
   print '  Where DEV_TYPE = Any of the available Device Models shown with DiscoverModels.py'
   print '        DEV_NAME is any short name  to identify this particular device. Examples: Temp-kitchen, 4in-1EricRoom, etc.'
   print '        However, in the FIWARE Cloud your device will be identified with host_id:DEV_NAME (host_id of the config.ini file).'
   sys.exit(2)

# Load the configuration file
with open(CONFIG_FILE,'r+') as f:
    sample_config = f.read()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))

IDAS_HOST=config.get('idas', 'host')
IDAS_ADMIN_PORT=config.get('idas', 'adminport')
IDAS_UL20_PORT=config.get('idas', 'ul20port')

IDAS_AAA=config.get('idas', 'OAuth')
if IDAS_AAA == "yes":
   TOKEN=config.get('user', 'token')
else:
   TOKEN="NULL"

HOST_ID=config.get('local', 'host_id')
f.close()

URL = "http://"+IDAS_HOST+":"+IDAS_ADMIN_PORT+'/m2m/v2/services/OpenIoT/assets'
PAYLOAD = '{   \
  "name": "'+HOST_ID+':'+SENSOR_NAME+'", \
  "model": "'+SENSOR_TYPE+'", \
  "asset": {  \
     "name": "asset-'+HOST_ID+':'+SENSOR_NAME+'", \
     "description": "asset model protocol" \
   } \
}'

HEADERS = {'content-type': 'application/json' , 'X-Auth-Token' : TOKEN}

print "* Asking to "+URL
print "* Headers: "+str(HEADERS)
print "* Sending PAYLOAD: "
print json.dumps(json.loads(PAYLOAD), indent=4)
print
print "..."
r = requests.post(URL, data=PAYLOAD, headers=HEADERS)
print
print "* Status Code: "+str(r.status_code)
print "* Response: "
print r.text
print