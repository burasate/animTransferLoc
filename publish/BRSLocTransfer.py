"""
BRS LOCATOR TRANSFER
create mimic translate and rotate animation
"""

import urllib,os
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
