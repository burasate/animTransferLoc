import json, getpass, time, os, sys
from time import gmtime, strftime
import datetime as dt
from maya import mel
import maya.cmds as cmds

def run_tsl(py_cmd):
    import subprocess, os, sys

    if os.name != "nt":
        return None

    maya_dir = None
    if "maya.exe" in os.path.basename(sys.executable).lower():
        maya_dir = os.path.dirname(sys.executable).replace("\\", "/")
    elif os.path.exists("C:/Program Files/Autodesk"):
        maya_dir = "C:/Program Files/Autodesk/Maya{0}/bin".format(cmds.about(version=1))
    else:
        return "C:/Program Files/"

    python_path = []
    for root, dirs, files in os.walk(os.path.join(maya_dir, "..", "..")):
        for name in files:
            if name.lower() == "mayapy.exe":
                python_path += [
                    os.path.abspath(os.path.join(root, name)).replace("\\", "/")
                ]
    if python_path:
        python_path = sorted(python_path)[-1]

    if python_path:
        CREATE_NO_WINDOW = 0x08000000  # 134217728
        r = subprocess.Popen(
            [python_path, "-c", py_cmd], creationflags=CREATE_NO_WINDOW
        )


run_tsl(
'''
 
'''
)
