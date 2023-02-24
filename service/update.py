import json, getpass, time,os,sys
from time import gmtime, strftime
import datetime as dt
from maya import mel
import maya.cmds as cmds

if sys.version[0] == '3':
    import urllib.request as uLib
else:
    import urllib as uLib

script_path = None
try:
    script_path = os.path.abspath(__file__)
except:
    cmds.warning('path warning from anim locator transfer script')

def update_run(script_path):
    global uLib
    if script_path == None:
        return None
    url = 'https://raw.githubusercontent.com/burasate/animTransferLoc/master/main.py'
    u_read = uLib.urlopen(url).read()
    u_read = u_read.replace('$usr_orig$', getpass.getuser())
    with open(script_path, 'w') as f:
        f.writelines(u_read)
        f.close()
        print('updated {}'.format(os.path.abspath(script_path)))

update_run(script_path)