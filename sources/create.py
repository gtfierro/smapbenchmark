from ConfigParser import RawConfigParser
from StringIO import StringIO
import sys
import uuid

configfile="""
[report 0]
ReportDeliveryLocation = http://{archiverip}:8079/add/{apikey}

[/]
uuid = {uuid}

[server]
port = 8080

[/fast]
type = {driver}
rate = {rate}
number = {number}
"""

def createdrivers(numdrivers, sourcename, pubrate, endpoints, archiverip, apikey):
    s = StringIO(configfile.format(uuid=str(uuid.uuid1()),driver=sourcename, rate=pubrate, number=endpoints, archiverip=archiverip, apikey=apikey))

    source = RawConfigParser()
    source.optionxform=str
    source.readfp(s)

    for i in xrange(numdrivers):
        print 'creating source at', source.get('server','port')
        port = int(source.get('server','port'))
        source.set('server', 'port', port+1)
        source.set('/','uuid', str(uuid.uuid1()))
        source.write(open('{0}{1}.ini'.format(sourcename.replace('.','_'), i), 'wb'))



if __name__ == '__main__':
    if len(sys.argv) == 1 or len(sys.argv) > 6:
        print '''\
    Usage: python create.py <drivername> <number of drivers> <endpoints per driver> <publish rate> <archiverip> <apikey>
    Example: python create.py sequential.SeqDriver 5 2 .01 127.0.0.1 asdfasdfasdfasdf
    '''
    sourcename = sys.argv[1]
    numdrivers = int(sys.argv[2])
    endpoints = int(sys.argv[3])
    pubrate = float(sys.argv[4])
    archiverip = sys.argv[5]
    apikey = sys.argv[6]
    createdrivers(numdrivers, sourcename, pubrate, endpoints, archiverip, apikey)
