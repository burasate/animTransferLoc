"""
BRS ANIM LOCATOR TRANSFER TOOL
BY BURASATE UTTHA (DEX3D)
"""

import maya.cmds as cmds
import maya.mel as mel

locSuffix = '_BRSSnapLoc'
BRSAnimLocGrp = 'BRSAnimLoc_Grp'
redirectGuide = 'BRSRedirectGuide'

def resetViewport(*_):
    # Redraw viewport On
    cmds.refresh(suspend=False)
    if cmds.ogs(q=True, pause=True) == True:
        cmds.ogs(pause=True)  # Turn on Viewport 2.0

def snap(object, target):
    # snap object to tatget
    snapper = cmds.parentConstraint(target, object, weight=1.0)
    cmds.delete(snapper)

def snapPoint(object, target):
    pointCon = cmds.pointConstraint(target, object, mo=False, weight=1.0)
    cmds.delete(pointCon)

def parentConstraint(object, target):
    # snap object to target
    conList = []
    try:
        pointC = cmds.pointConstraint(target, object, weight=1.0, mo=False)
    except:
        pass
    else : conList.append(pointC)
    try:
        orientC = cmds.orientConstraint(target, object, weight=1.0, mo=False)
    except:
        pass
    else: conList.append(orientC)
    return conList

def createBRSAnimLocGrp(snapObj):
    attr = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
    try:
        cmds.select(BRSAnimLocGrp)
    except:
        cmds.group(n=BRSAnimLocGrp,empty=True)
        cmds.setAttr('{}.rotateOrder'.format(BRSAnimLocGrp),3)
        cmds.setAttr(BRSAnimLocGrp + '.useOutlinerColor', 1)
        cmds.setAttr(BRSAnimLocGrp + '.outlinerColor', 0.7067, 1, 0)
        snapPoint(BRSAnimLocGrp,snapObj)
        for a in attr:
            cmds.setAttr('{}.{}'.format(BRSAnimLocGrp,a),lock=True)

def createRedirectGuide(*_):
    try:
        cmds.delete(redirectGuide)
    except:
        pass
    try:
        cmds.select(BRSAnimLocGrp)
    except:
        pass
    else:
        cmds.spaceLocator(n=redirectGuide)
        cmds.setAttr(redirectGuide + '.overrideEnabled', 1)
        cmds.setAttr(redirectGuide + '.overrideRGBColors', 1)
        cmds.setAttr(redirectGuide + '.overrideColorRGB', 0.0, 0.701, 1)
        cmds.setAttr(redirectGuide + '.useOutlinerColor', 1)
        cmds.setAttr(redirectGuide + '.outlinerColor', 0.0, 0.7, 1)
        cmds.setAttr('{}.localScaleZ'.format(redirectGuide), 2)
        snapPoint(redirectGuide,BRSAnimLocGrp)

def applyRedirectGuide(*_):
    attr = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    try:
        cmds.select([redirectGuide,BRSAnimLocGrp])
    except:
        pass
    else:
        for a in attr:
            cmds.setAttr('{}.{}'.format(BRSAnimLocGrp,a),lock=False)
        selection = cmds.listRelatives(BRSAnimLocGrp, children=True)
        cmds.select(selection)
        objectToLocatorSnap(toGroup=False,forceConstraint=True)
        snap(BRSAnimLocGrp,redirectGuide)
        locatorToObjectSnap()
        cmds.delete(redirectGuide)
        for a in attr:
            cmds.setAttr('{}.{}'.format(BRSAnimLocGrp,a),lock=True)

def getAllKeyframe(objectName):
    minTime = cmds.playbackOptions(q=True, minTime=True)
    maxTime = cmds.playbackOptions(q=True, maxTime=True)
    keyframeList = []
    attrList = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
    if type(objectName)==list:
        objectName = objectName[0]
    for attr in attrList:
        keyList = cmds.keyframe(objectName + '.' + attr, q=True, timeChange=True)
        if keyList != None:
            for k in keyList:
                if not k in keyframeList :
                    keyframeList.append(k)
    keyframeList = sorted(keyframeList)
    #print(keyframeList)
    return keyframeList

def bakeKey(objectList,keyframeList,inTimeline=False):
    at = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
    if inTimeline:
        minKeyframe = round(cmds.playbackOptions(q=True, minTime=True))
        maxKeyframe = round(cmds.playbackOptions(q=True, maxTime=True))
    else:
        minKeyframe = round(min(keyframeList))
        maxKeyframe = round(max(keyframeList))
    #cmds.ogs(pause=True)
    cmds.refresh(suspend=True)
    cmds.bakeResults(objectList, sampleBy=1, disableImplicitControl=True, preserveOutsideKeys=True,
                     sparseAnimCurveBake=False, t=(minKeyframe, maxKeyframe),at=at)
    cmds.filterCurve(objectList)
    cmds.refresh(suspend=False)
    if cmds.ogs(q=True, pause=True) == True:
        cmds.ogs(pause=True)  # Turn on Viewport 2.0

def getMimicLocator(objectName,locName=locSuffix):
    anno = cmds.checkBox(AnnoChk, q=True, value=True)
    LocName = objectName + locName
    # delete exist locator
    try: cmds.delete(LocName)
    except:pass

    # create mimic locator
    locator = cmds.spaceLocator(n=LocName)
    cmds.setAttr(LocName + '.overrideEnabled', 1)
    cmds.setAttr(LocName + '.overrideRGBColors', 1)
    cmds.setAttr(LocName + '.overrideColorRGB', 0.465, 1, 0.0)
    cmds.setAttr(LocName + '.useOutlinerColor', 1)
    cmds.setAttr(LocName + '.outlinerColor', 0.7067, 1, 0)
    parentConstraint(locator, objectName)

    annoText = objectName
    if annoText.__contains__(':'):
        annoText = (annoText.split(':')).pop()
    annotateShape = cmds.annotate(LocName, tx=annoText)
    cmds.pickWalk(d='up')
    annotate = (cmds.ls(sl=True))[0]
    cmds.parent(annotate, LocName)
    cmds.setAttr(annotate + '.overrideEnabled', 1)
    cmds.setAttr(annotate + '.overrideDisplayType', 2)
    cmds.setAttr(annotateShape + '.displayArrow', 0)
    cmds.setAttr(annotate + '.translateX', 0)
    cmds.setAttr(annotate + '.translateY', 0)
    cmds.setAttr(annotate + '.translateZ', 0)
    cmds.setAttr(annotate + '.hiddenInOutliner', True)
    cmds.rename(annotate, objectName + '_annotate')
    if anno == False:
        cmds.delete(objectName + '_annotate')

    return locator

def keepKeyframe(objectList,keyframeList):
    newKeyframeList = []
    for k in keyframeList:
        k = round(k,0)
        newKeyframeList.append(k)
    for k in range(int(min(newKeyframeList)),int(max(newKeyframeList))):
        if not float(k) in newKeyframeList:
            cmds.cutKey(objectList,time=(float(k),float(k)))
    #print (newKeyframeList)

def deleteConstraint(objectName):
    con = cmds.listRelatives(objectName, type='constraint')
    cmds.delete(con)

def statTextUI(text):
    cmds.text(statText,e=True,l=text)
    cmds.refresh()

def objectToLocatorSnap(toGroup=True,forceConstraint=False):
    curTime = cmds.currentTime(query=True)
    bakeK = cmds.checkBox(BakeChk, q=True, value=True)
    cons = cmds.checkBox(ConsChk, q=True, value=True)
    tl = cmds.checkBox(TimelineChk, q=True, value=True)

    if forceConstraint:
        cons = forceConstraint

    selected = cmds.ls(sl=True)
    # print (selected)
    if toGroup:
        createBRSAnimLocGrp(selected)

    for objName in selected:
        #print(objName)
        keyframeList = getAllKeyframe(objName)
        #print(keyframeList)

        if len(keyframeList) > 1:
            statTextUI('get keyframe {} {} - {}'.format(objName, min(keyframeList), max(keyframeList)))
            SnapLoc = getMimicLocator(objName)[0]
            #print(SnapLoc)
            if toGroup:
                cmds.parent(SnapLoc,BRSAnimLocGrp)
            statTextUI('Bake to {}'.format(SnapLoc))
            bakeKey(SnapLoc,keyframeList,inTimeline=tl)
            if bakeK == False:
                keepKeyframe(SnapLoc,keyframeList)
                print ('keepKeyframe')
            deleteConstraint(SnapLoc)
            if cons:
                parentConstraint(objName,SnapLoc)

    # Finish
    cmds.currentTime(curTime)
    cmds.select(selected, r=True)
    resetViewport()
    statTextUI('')
    print ('Create Anim Locator {}'.format(selected))

def locatorToObjectSnap(*_):
    curTime = cmds.currentTime(query=True)
    bakeK = cmds.checkBox(BakeChk, q=True, value=True)
    at = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']

    selected = cmds.ls(sl=True)
    # print (selected)
    for objName in selected:
        SnapLoc = objName+locSuffix
        print(SnapLoc)

        try:
            keyframeList = getAllKeyframe(SnapLoc)
            cmds.select(SnapLoc)
        except:
            pass
        else:
            cmds.cutKey(objName, cl=True, at=at,time=(min(keyframeList),max(keyframeList)))
            deleteConstraint(objName)
            parentConstraint(objName,SnapLoc)
            statTextUI('Bake to {}'.format(objName))
            bakeKey(objName, keyframeList)
            keepKeyframe(objName,keyframeList)
            cmds.delete(SnapLoc)

            if cmds.listRelatives(BRSAnimLocGrp,children=True) == None:
                cmds.delete(BRSAnimLocGrp)

    # Fixing Unsnap Keyframe
    cmds.snapKey(selected, timeMultiple=1.0)

    # Finish
    cmds.currentTime(curTime)
    cmds.select(selected, r=True)
    resetViewport()
    statTextUI('')
    print ('Apply Anim Locator {}'.format(selected))

"""
-----------------------------------------------------------------------
UI
-----------------------------------------------------------------------
"""
version = '1.05'
winID = 'BRSLOCTRANSFER'
winWidth = 200

colorSet = {
    'bg': (.2, .2, .2),
    'red': (0.8, 0.4, 0),
    'green': (0.7067,1,0),
    'blue': (0, 0.4, 0.8),
    'yellow': (1, 0.8, 0),
    'shadow': (.15, .15, .15),
    'highlight': (.3, .3, .3)
}

if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)
cmds.window(winID, t='BRS Locator Transfer' + ' - ' + version,
            w=winWidth, sizeable=True,
            retain=True, bgc=colorSet['bg'])

cmds.columnLayout(adj=False, w=winWidth)
cmds.text(l='BRS Locator Transfer' + ' - ' + version, fn='boldLabelFont', h=20, w=winWidth, bgc=colorSet['green'])
statText = cmds.text(l='', fn='smallPlainLabelFont', h=15, w=winWidth, bgc=colorSet['shadow'])
cmds.text(l='   Anim Locator', fn='boldLabelFont', al='left', h=25, w=winWidth)
cmds.rowLayout(numberOfColumns=2, columnWidth2=(winWidth * 0.5, winWidth * 0.5), columnAlign2=['center', 'center'])
ConsChk = cmds.checkBox(label='Constraint', align='center',v=True)
AnnoChk = cmds.checkBox(label='Annotation', align='center',v=True)
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=2, columnWidth2=(winWidth * 0.5, winWidth * 0.5), columnAlign2=['center', 'center'])
BakeChk = cmds.checkBox(label='Bake Keyframe', align='center')
TimelineChk = cmds.checkBox(label='In Timeline', align='center')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=1, columnWidth1=winWidth-1)
cmds.button(l='Create Anim Locator', h=25 ,w=winWidth-4 ,
            c=lambda arg: objectToLocatorSnap(toGroup=True,forceConstraint=False), bgc=colorSet['highlight'])
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=1, columnWidth1=winWidth-1)
cmds.button(l='Apply Anim Locator', h=25 ,w=winWidth-4, c=locatorToObjectSnap, bgc=colorSet['highlight'])
cmds.setParent('..')

cmds.text(l='   Redirection', fn='boldLabelFont', al='left', h=25, w=winWidth)
cmds.rowLayout(numberOfColumns=1, columnWidth1=winWidth-1)
cmds.button(l='Create Redirection Guide', h=25 ,w=winWidth-4, bgc=colorSet['highlight'], c=createRedirectGuide)
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=1, columnWidth1=winWidth-1)
cmds.button(l='Apply Redirection', h=25 ,w=winWidth-4, bgc=colorSet['highlight'], c=applyRedirectGuide)
cmds.setParent('..')

cmds.text(l='Created by Burasate Uttha', h=20, al='left', fn='smallPlainLabelFont')

def BRSLocTransferUI(*_):
    cmds.showWindow(winID)
    resetViewport()
    
BRSLocTransferUI()