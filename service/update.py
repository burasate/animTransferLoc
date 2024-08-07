import json,getpass,time,os,sys,getpass
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

# ================ CHECK PYC ==================
if os.path.exists(script_path.replace('.pyc','py')):
    script_path = script_path.replace('.pyc','py')

def update_run(script_path):
    global uLib,getpass,os
    if script_path == None:
        return None
    url = 'https://raw.githubusercontent.com/burasate/animTransferLoc/master/main.py'
    u_read = uLib.urlopen(url).read().decode('utf-8')
    u_read = u_read.replace('$usr_orig$', getpass.getuser())
    with open(script_path, 'w') as f:
        f.writelines(u_read)
        f.close()
        print('loaded... {}'.format(os.path.abspath(script_path)))

update_run(script_path)