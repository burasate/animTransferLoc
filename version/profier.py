# BRS PROFILER
# MAYA VERSION 2018-2019
# PARALLEL MODE

import json, getpass, os, time
from csv import DictWriter
from csv import writer
from datetime import datetime as dt


def getFPSUnit(*_):
    timeUnitSet = {'game': 15, 'film': 24, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}
    timeUnit = cmds.currentUnit(q=True, t=True)
    fps = 0

    if timeUnit in timeUnitSet:
        fps = int(timeUnitSet[timeUnit])
    elif timeUnit.__contains__('fps'):
        fps = str(cmds.currentUnit(q=True, t=True))[:-3]
    elif timeUnit.__contains__('df'):
        fps = str(cmds.currentUnit(q=True, t=True))[:-2]
    fps = int(fps)
    return fps


def getProfiler(*_):
    if cmds.evaluationManager(q=True, mode=True)[0] != 'parallel':
        return None
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    raw_name, extension = os.path.splitext(filename)

    minTime = cmds.playbackOptions(q=True, minTime=True)
    maxTime = cmds.playbackOptions(q=True, maxTime=True)
    fStart = cmds.playbackOptions(q=True, animationStartTime=True)
    fEnd = cmds.playbackOptions(q=True, animationEndTime=True)
    currFrame = cmds.currentTime(q=True)
    frameRange = 5

    for categoryName in cmds.profiler(q=True, ac=True):
        categoryIndex = cmds.profiler(query=True, categoryNameToIndex=categoryName)
    if categoryName == 'Main':
        cmds.profiler(categoryRecording=True, categoryIndex=categoryIndex)
    else:
        cmds.profiler(categoryRecording=False, categoryIndex=categoryIndex)
    cmds.profiler(bufferSize=200, reset=True)
    cmds.profiler(sampling=True)

    for i in range(frameRange):
        cmds.currentTime(i + currFrame - round(frameRange / 2, 0), update=True)

    cmds.profiler(sampling=False)
    cmds.refresh(f=True)

    eventCount = cmds.profiler(q=True, eventCount=True)
    #cmds.currentTime(currFrame, update=True)
    cmds.currentTime(currFrame)
    cmds.playbackOptions(e=True, minTime=minTime, maxTime=maxTime, ast=fStart, aet=fEnd)

    drawCount = 0
    totalDuration = 0
    eventMaxTime = 0
    criticalPath = ''
    timeStart = time.time()
    timeStop = 0.0
    processTime = 0.0
    for i in range(eventCount):
        data = {
            'eventDescription': cmds.profiler(q=True, eventDescription=True, eventIndex=i),
            'eventDuration': cmds.profiler(q=True, eventDuration=True, eventIndex=i),
            'eventCategory': cmds.profiler(q=True, eventCategory=True, eventIndex=i),
            'eventName': cmds.profiler(q=True, eventName=True, eventIndex=i),
            'eventStartTime': cmds.profiler(q=True, eventStartTime=True, eventIndex=i),
        }
        if data['eventName'] == 'SetCurrentTime':
            drawCount += 1
        if eventMaxTime < data['eventDuration'] and data['eventName'] == 'EvaluateNode':
            eventMaxTime = data['eventDuration']
            criticalPath = data['eventDescription']
        totalDuration = data['eventStartTime']

        timeStop = time.time()
        processTime = round(abs(timeStop - timeStart), 0)
        if drawCount > 2 and processTime > 5:
            break

    totalTime = int(totalDuration / 1000)
    refreshTime = int((totalDuration / drawCount) / 1000)
    if refreshTime < 1:
        refreshTime = 1
    frameRate = 1 / (float('{0:.6f}'.format(refreshTime)) / 1000)
    frameRate = round(frameRate, 1)
    eventMaxTime = float('{0:.6f}'.format(eventMaxTime)) / 1000
    eventMaxTime = round(eventMaxTime, 1)

    # convert ms to sec
    totalTime = float('{0:.6f}'.format(totalTime)) / 1000
    refreshTime = float('{0:.6f}'.format(refreshTime)) / 1000
    eventMaxTime = float('{0:.6f}'.format(eventMaxTime)) / 1000

    referenceList = cmds.ls(references=True)
    nameSpaceList = cmds.namespaceInfo(lon=True)

    data = {
        'dateTime': dt.now().strftime('%Y-%m-%d %H:%M:%S'),
        'scene': raw_name,
        'user': getpass.getuser(),
        # 'drawCount': drawCount,
        # 'totalTime': totalTime,
        # 'refreshTime': refreshTime,
        'frameRate': frameRate,
        'timeUnit': getFPSUnit(),
        # 'criticalPath': criticalPath,
        # 'eventMaxTime': eventMaxTime,
        'processTime': processTime,
        'faceCount': cmds.polyEvaluate(cmds.ls(), face=True),
        'dagCount': len(cmds.ls(assemblies=True)),
        'referenceCount': len(referenceList),
        'nameSpaceList': ','.join(nameSpaceList),
        'keyframeCount': cmds.keyframe(q=True, kc=True),
        'frameStart': fStart,
        'frameEnd': fEnd,
        'frameMin': minTime,
        'frameMax': maxTime
    }

    import urllib
    url = 'https://hook.integromat.com/0xhkb9b13gfcccrgv1r8by38nsnvcdrc'
    params = urllib.urlencode(data)
    conn = urllib.urlopen('{}?{}'.format(url, params))
    print(conn.read())
    # print(conn.info())

    print(''.join(['===================\n',
                   'PROFILER ANALYTIC\n',
                   '===================']))
    print('draw count {} frames'.format(drawCount))
    print('total time {} sec'.format(totalTime))
    print('refresh time {} sec'.format(refreshTime))
    print('frame rate {} fps'.format(frameRate))
    print('critical part is \"{}\" used {} sec'.format(criticalPath, eventMaxTime))
    print('processTime {} sec'.format(processTime))
    print('===================')
    cmds.profiler(reset=True)


try:
    getProfiler()
except:
    pass

