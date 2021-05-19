import json, getpass, os, time
from csv import DictWriter
from csv import writer
from datetime import datetime as dt

filepath = cmds.file(q=True, sn=True)
filename = os.path.basename(filepath)
raw_name, extension = os.path.splitext(filename)

minTime = cmds.playbackOptions(q=True, minTime=True)
maxTime = cmds.playbackOptions(q=True, maxTime=True)
fStart = cmds.playbackOptions(q=True, animationStartTime=True)
fEnd = cmds.playbackOptions(q=True, animationEndTime=True)
currFrame = cmds.currentTime(q=True)
frameRange = 10

cmds.playbackOptions(e=True, minTime=currFrame - 10.0,
                     maxTime=currFrame + float(frameRange - 10))

cmds.profiler(bufferSize=200,reset=True)
cmds.profiler(sampling=True)

# cmds.play(wait=True,playSound=False,record=True)
for i in range(frameRange):
    cmds.currentTime(i + currFrame - 10, update=True)

cmds.profiler(sampling=False)
cmds.refresh(f=True)

eventCount = cmds.profiler(q=True, eventCount=True)
cmds.currentTime(currFrame, update=True)
cmds.playbackOptions(e=True, minTime=minTime, maxTime=maxTime, ast=fStart, aet=fEnd)

rec = []
drawCount = 0
totalDuration = 0
eventMaxTime = 0
criticalPath = ''
timeStart = time.time()
for i in range(eventCount):
    data = {
        'eventDescription': cmds.profiler(q=True, eventDescription=True, eventIndex=i),
        'eventDuration': cmds.profiler(q=True, eventDuration=True, eventIndex=i),
        'eventCategory': cmds.profiler(q=True, eventCategory=True, eventIndex=i),
        'eventName': cmds.profiler(q=True, eventName=True, eventIndex=i),
        'eventStartTime': cmds.profiler(q=True, eventStartTime=True, eventIndex=i),
    }
    if data['eventDescription'] == '':
        continue
    if data['eventDescription'] == 'EvaluationGraph_Normal':
        drawCount += 1
    if eventMaxTime < data['eventDuration'] and data['eventName'] == 'EvaluateNode':
        eventMaxTime = data['eventDuration']
        criticalPath = data['eventDescription']
    totalDuration = data['eventStartTime']
    # rec.append(data)
# json.dump(rec, open('S:/Animation training/Kaofang/test.json', 'w'), indent=4)

totalTime = int(totalDuration / 1000)
refreshTime = int((totalDuration / drawCount) / 1000)
if refreshTime < 1:
    refreshTime = 1
frameRate = 1 / (float('{0:.6f}'.format(refreshTime)) / 1000)
frameRate = round(frameRate, 1)
eventMaxTime = float('{0:.6f}'.format(eventMaxTime)) / 1000
eventMaxTime = round(eventMaxTime, 1)
timeStop = time.time()
processTime = round(abs(timeStop - timeStart), 0)

data = {
    'dateTime': dt.now().strftime('%Y-%m-%d %H:%M:%S'),
    'scene': raw_name,
    'user': getpass.getuser(),
    'drawCount': drawCount,
    'totalTime': totalTime,
    'refreshTime': refreshTime,
    'frameRate': frameRate,
    'criticalPath': criticalPath,
    'eventMaxTime': eventMaxTime,
    'processTime': processTime
}
header = list(data)
print(''.join(['===================\n',
               'PROFILER ANALYTIC\n',
               '===================']))
print (list(data))
print('draw count {} frames'.format(drawCount))
print('total time {} ms'.format(totalTime))
print('refresh time {} ms'.format(refreshTime))
print('frame rate {} fps'.format(frameRate))
print('critical part is \"{}\" used {} ms'.format(criticalPath, eventMaxTime))
print('processTime {} sec'.format(processTime))
print('===================')

dataPath = 'S:/Animation training/Kaofang/ogs_profier.csv'
# dataPath = 'C:/Users/DEX3D_I7/Desktop/ogs_profier.csv'
try:
    with open(dataPath, 'a') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=header)
        dictwriter_object.writerow(data)
        f_object.close()
except:
    pass
else:
    print('profiler data is recorded')
