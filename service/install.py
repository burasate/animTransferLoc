"""
BRS LOCATOR TRANSFER INSTALLER-UPDATER
"""
import os, base64, sys, datetime
import maya.cmds as cmds
import maya.mel as mel

class lct:
    py_ver = sys.version[0]
    if py_ver == '3':
        write_mode = 'w'
        import urllib.request as uLib
    else:
        write_mode = 'wb'
        import urllib as uLib

    maya_app_dir = mel.eval('getenv MAYA_APP_DIR')
    scripts_dir = maya_app_dir + os.sep + 'scripts'
    main_path_b64 = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2J1cmFzYXRlL2FuaW1UcmFuc2ZlckxvYy9tYXN0ZXIvbWFpbi5weQ=='

    lct_path = scripts_dir + os.sep + 'BRSLocTransfer.py'
    has_file = os.path.exists(lct_path)

    @staticmethod
    def run():
        if lct.has_file:
            st_mtime = os.stat(lct.lct_path).st_mtime
            mdate_str = str(datetime.datetime.fromtimestamp(st_mtime).date())
            today_date_str = str(datetime.datetime.today().date())
            if mdate_str == today_date_str:
                #print(mdate_str == today_date_str)
                return None

        with open(lct.lct_path, lct.write_mode) as f:
            print('lct updating...'),
            u = base64.b64decode(lct.main_path_b64).decode()
            r = lct.uLib.urlopen(u).read()
            f.writelines(r)
            f.close()
            print('finished')

print('\n'*20),
lct.run()

"""
import urllib,os
import maya.cmds as cmds
import maya.mel as mel

def formatPath(path):
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path

mayaAppDir = formatPath(mel.eval('getenv MAYA_APP_DIR'))
scriptsDir = formatPath(mayaAppDir + os.sep + 'scripts')

url = 'https://raw.githubusercontent.com/burasate/animTransferLoc/master/main.py'
if cmds.about(connected=True):
    urlRead = urllib.urlopen(url).read()
    exec (urlRead)

    mainWriter = open(scriptsDir + os.sep + 'BRSLocTransfer.py', 'w')
    mainWriter.writelines(urlRead)
    mainWriter.close()
else :
    try:
        script = open(scriptsDir + os.sep + 'BRSLocTransfer.py', 'r')
        exec (script.read())
        script.close()
    except:
        #print ('Can\'t Load File From Local \"{}\"'.format('BRSLocTransfer.py'))
        cmds.inViewMessage(
            amg='Can\'t Load File From Local\n\"{}\"\nPlease Use Offline Script'.format(scriptsDir + os.sep + 'BRSLocTransfer.py'),
            pos='midCenter', fade=True,
            fit=300, fst=7000, fot=300
        )
"""