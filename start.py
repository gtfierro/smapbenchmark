from configobj import ConfigObj
from sources import create
import argparse
import sys
import shutil
import subprocess
import glob
import os
import time

parser = argparse.ArgumentParser(description="Configure and start sMAP benchmark")
action = parser.add_mutually_exclusive_group()
action.add_argument('-c','--create-sources',action="store_true")
action.add_argument('-s','--start-sources',action="store_true")
action.add_argument('-d','--cleanup',action="store_true")
args = parser.parse_args()

config = ConfigObj('config.ini')

globalconfig = config['global']
scenarioconfig = config[globalconfig['scenario']]

if args.create_sources:
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
elif args.start_sources:
    print 'starting sources'
    FNULL = open(os.devnull, 'w')
    inis = glob.glob('sources_*.ini')
    inis = [x.split('.')[0] for x in inis]

    print inis

    processes = []
    for ini in inis:
        time.sleep(1)
        command = "twistd --pidfile {0}.pid -n smap {0}.ini".format(ini)
        p = subprocess.Popen(command, shell=True, stdout=FNULL)
        processes.append(p)
    try:
        raw_input()
    except:
        for p in processes:
            print "killing",p
            p.terminate()
elif args.cleanup:
    print "removing..."
    inis = glob.glob('sources_*.ini')
    for ini in inis:
        print ini
        ini_conf = ConfigObj(ini)
        ini_uuid = ini_conf['/']['uuid']
        os.remove(ini)
        if os.path.exists(ini_uuid):
            os.remove(ini_uuid)
            shutil.rmtree(ini_uuid+"-reports")
        if os.path.exists(ini_uuid+'.tmp'):
            os.remove(ini_uuid+".tmp")
