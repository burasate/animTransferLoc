"""
---------------------
Anim Locator Transfer
Support Service
---------------------
"""
import getpass,os,time,urllib,sys
from time import gmtime, strftime
import datetime as dt
from maya import mel
import maya.cmds as cmds

filepath = cmds.file(q=True, sn=True)
filename = os.path.basename(filepath)
raw_name, extension = os.path.splitext(filename)
minTime = cmds.playbackOptions(q=True, minTime=True)
maxTime = cmds.playbackOptions(q=True, maxTime=True)
referenceList = cmds.ls(references=True)
nameSpaceList = cmds.namespaceInfo(lon=True)

data = {
    'dateTime' : dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'timezone' : str( strftime('%z', gmtime()) ),
    'year' : dt.datetime.now().strftime('%Y'),
    'month' : dt.datetime.now().strftime('%m'),
    'day' : dt.datetime.now().strftime('%d'),
    'hour' : dt.datetime.now().strftime('%H'),
    'user' : getpass.getuser(),
    'maya' : str(cmds.about(version=True)),
    'ip' : str(urllib.urlopen('https://v4.ident.me').read().decode('utf8')),
    'scene' : raw_name,
    'timeUnit' : cmds.currentUnit(q=True, t=True),
    'timeMin' : minTime,
    'timeMax' : maxTime,
    'duration' : maxTime - minTime,
    'referenceCount': len(referenceList),
    'nameSpaceList': ','.join(nameSpaceList),
    'os' : str(cmds.about(operatingSystem=True))
}

#url = 'https://hook.integromat.com/k9ura85kw05vf1cuiakcasxm7uw2y2vj'
#params = urllib.urlencode(data)
#conn = urllib.urlopen('{}?{}'.format(url, params))

#print(conn.read())
#print(conn.info())

# Supporter Coding
