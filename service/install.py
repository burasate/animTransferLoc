"""
BRS LOCATOR TRANSFER INSTALLER-UPDATER
"""
import os, base64, sys, datetime, getpass
import maya.cmds as cmds
import maya.mel as mel

class brs:
    py_ver = sys.version[0]
    if py_ver == '3':
        write_mode = 'w'
        import urllib.request as uLib
    else:
        write_mode = 'w'
        import urllib as uLib

    maya_app_dir = mel.eval('getenv MAYA_APP_DIR')
    scripts_dir = maya_app_dir + os.sep + 'scripts'
    main_path_b64 = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2J1cmFzYXRlL2FuaW1UcmFuc2ZlckxvYy9tYXN0ZXIvbWFpbi5weQ=='

    lct_path = scripts_dir + os.sep + 'BRSLocTransfer.py'
    has_file = os.path.exists(lct_path)

    @staticmethod
    def run():
        if brs.has_file:
            st_mtime = os.stat(brs.lct_path).st_mtime
            mdate_str = str(datetime.datetime.fromtimestamp(st_mtime).date())
            today_date_str = str(datetime.datetime.today().date())
            if mdate_str == today_date_str:
                print('updated')
                return None

        with open(brs.lct_path, brs.write_mode) as f:
            print('brs updating...'),
            u = base64.b64decode(brs.main_path_b64).decode()
            r = brs.uLib.urlopen(u).read().replace('$usr_orig$', getpass.getuser())
            f.writelines(r)
            f.close()
            print('finished')

    @staticmethod
    def shelf():
        top_shelf = mel.eval('$nul = $gShelfTopLevel')
        current_shelf = cmds.tabLayout(top_shelf, q=1, st=1)
        command = '''
#------------------------------------
# BRS LOCATOR TRANSFER
#------------------------------------
import imp;import BRSLocTransfer;imp.reload(BRSLocTransfer)
#------------------------------------
'''.format(brs.lct_path.replace('\\','/'))
        cmds.shelfButton(stp='python', iol='LocTransfer', parent=current_shelf,
                         ann='BRS LOCATOR TRANSFER', i='pythonFamily.png', c=command)
        cmds.confirmDialog(title='BRS LOCATOR TRANSFER', message='Installation Successful.', button=['OK'])
        exec(command)
#--------------------
#AUTO RUN
try:
    brs.run()
except:
    pass
#--------------------