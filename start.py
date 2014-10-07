from configobj import ConfigObj
from sources import create
import sys
config = ConfigObj('config.ini')

globalconfig = config['global']
scenarioconfig = config[globalconfig['scenario']]

print scenarioconfig
if scenarioconfig['driverlocation'] == 'local':
    sourcename = scenarioconfig['driver']
    pubrate = float(scenarioconfig['pubrate'])
    endpoints = int(scenarioconfig['endpoints_per_driver'])
    archiverip = scenarioconfig['archiverip']
    apikey = scenarioconfig['apikey']
    numdrivers = int(scenarioconfig['number_drivers'])
    create.createdrivers(numdrivers, sourcename, pubrate, endpoints, archiverip, apikey)
else:
    print 'ec2 not implemented yet'
    sys.exit(0)
