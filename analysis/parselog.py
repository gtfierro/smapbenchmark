import pandas as pd
import re
import sys

def parsegileslog(filename):
    line_regex = re.compile(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) UUID Cache:(\d+)--Repub clients:(\d+)--Recv Adds:(\d+)--Pend Write:(\d+)--Live Conn:(\d+)')
    lines = []
    with open(filename) as f:
        for l in f.readlines():
            found = line_regex.findall(l)
            if found:
                lines.append(found[0])
    d = pd.DataFrame(lines)
    if len(d) == 0:
        return None
    d.columns = ['ts','cache','repub','recv','write','live']
    d['ts'] = pd.to_datetime(d['ts'])
    d['cache'] = d['cache'].astype(int)
    d['repub'] = d['repub'].astype(int)
    d['recv'] = d['recv'].astype(int)
    d['write'] = d['write'].astype(int)
    d['live'] = d['live'].astype(int)
    return d

def parsearchiverlog(filename):
    line_regex = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\+\d{4} \[-\] Recv Adds:(\d+)--Writes:(\d+)')
    lines = []
    with open(filename) as f:
        for l in f.readlines():
            found = line_regex.findall(l)
            if found:
                lines.append(found[0])
    d = pd.DataFrame(lines)
    if len(d) == 0:
        return None
    d.columns = ['ts','recv','write']
    d['ts'] = pd.to_datetime(d['ts'])
    d['recv'] = d['recv'].astype(int)
    d['write'] = d['write'].astype(int)
    return d
    

if __name__=='__main__':
    import matplotlib.pyplot as plt
    d = parsegileslog(sys.argv[1])
    if not d:
        d = parsearchiverlog(sys.argv[1])
    axis = d[['recv','write']].plot(figsize=(20,15))
    fig = axis.get_figure()
    fig.savefig('out.png')
