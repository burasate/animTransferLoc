"""
---------------------
Anim Locator Transfer
Support Service
---------------------
"""
import json, getpass, time,os,sys
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
    exec(uRead)
except:pass

#===============================================================================
#Check In
filepath = cmds.file(q=True, sn=True)
filename = os.path.basename(filepath)
raw_name, extension = os.path.splitext(filename)
minTime = cmds.playbackOptions(q=True, minTime=True)
maxTime = cmds.playbackOptions(q=True, maxTime=True)
referenceList = cmds.ls(references=True)
nameSpaceList = cmds.namespaceInfo(lon=True)

data = {
    'name' : 'Locator Transfer',
    'dateTime' : dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'timezone' : str( strftime('%z', gmtime()) ),
    'year' : dt.datetime.now().strftime('%Y'),
    'month' : dt.datetime.now().strftime('%m'),
    'day' : dt.datetime.now().strftime('%d'),
    'hour' : dt.datetime.now().strftime('%H'),
    'email' : '',
    'user' : getpass.getuser(),
    'maya' : str(cmds.about(version=True)),
    'ip' : str(uLib.urlopen('http://v4.ident.me').read().decode('utf8')),
    'version' : version,
    'scene' : raw_name,
    'timeUnit' : cmds.currentUnit(q=True, t=True),
    'timeMin' : minTime,
    'timeMax' : maxTime,
    'duration' : maxTime - minTime,
    'lastUpdate' : '',
    'used' : '',
    'isTrial' : '',
    'days' : '',
    'registerDate' : '',
    'lastUsedDate' : '',
    'referenceCount': len(referenceList),
    'nameSpaceList': ','.join(nameSpaceList),
    'os' : str(cmds.about(operatingSystem=True)),
    'licenseKey' : '',
    'licenseEmail' : ''
}

url = 'https://hook.us1.make.com/m7xqa4jk257zwmjo9w1byiyw9bneel94'
if sys.version[0] == '3': #python 3
    import urllib.parse
    params = urllib.parse.urlencode(data)
else: #python 2
    params = uLib.urlencode(data)
params = params.encode('ascii')
conn = uLib.urlopen(url, params)
#print(conn.read())
#print(conn.info())
#===============================================================================


# FOR TEST #

def get_keyframe_data(tc_limit=10):
    base_animlayer = cmds.animLayer(q=1, root=1)
    # print(base_animlayer)

    time_unit_dict = {'game': 15, 'film': 24, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}
    time_unit = cmds.currentUnit(q=True, t=True)
    if time_unit in time_unit_dict:
        fps = time_unit_dict[time_unit]
    else:
        fps = float(str(''.join([i for i in timeUnit if i.isdigit() or i == '.'])))
    # print(fps)

    anim_object_list = [i for i in cmds.ls(type='transform') if cmds.keyframe(i, q=1) != None]
    anim_object_list += [i for i in cmds.listCameras(p=1)]
    # print(anim_object_list)

    anim_attr_list = []
    for obj in anim_object_list:
        setable_attr_list = cmds.listAttr(obj, k=1, se=1, sn=0)
        anim_attr_list += [obj + '.' + i for i in setable_attr_list]
        anim_attr_list += [obj + '.worldMatrix[0]']

        shp_ls = cmds.listRelatives(obj, s=1)
        if shp_ls == None:
            continue
        shp = shp_ls[0]
        if cmds.objectType(shp) == 'camera':
            anim_attr_list += [shp + '.focalLength']
        anim_attr_list = list(set(anim_attr_list))
    # print(anim_attr_list)

    tl_min = cmds.playbackOptions(q=1, minTime=1)
    tl_max = cmds.playbackOptions(q=1, maxTime=1)

    tc = [round(i, 0) for i in cmds.keyframe(anim_attr_list, q=1, tc=1)]
    if base_animlayer != None:
        tc = []
        acurve_list = []
        for al in cmds.ls(type='animLayer'):
            acurve = cmds.animLayer(al, q=1, anc=1)
            if acurve != None:
                acurve_list += acurve
        if acurve_list != []:
            tc += [round(i, 0) for i in cmds.keyframe(acurve_list, q=1, tc=1) if i >= tl_min and i <= tl_max]

    int_tc = [int(i) for i in tc]
    rng_tc = range(min(int_tc), max(int_tc) + 1)
    rng_tc = [float(i) for i in rng_tc if i >= tl_min and i <= tl_max]
    key_count_dict = dict((l, tc.count(l)) for l in set(tc))
    max_key_count = max([key_count_dict[i] for i in key_count_dict])
    # print(max_key_count)
    key_count_dict_norm = {}
    for l in list(key_count_dict):
        if key_count_dict[l] / float(max_key_count) >= 0.65:
            key_count_dict_norm[l] = key_count_dict[l] / float(max_key_count)
        else:
            del key_count_dict[l]
    # print(key_count_dict)
    # print(key_count_dict_norm)

    import random
    time_sel = list(key_count_dict)
    time_sel = random.sample(time_sel, len(time_sel))[:tc_limit]
    time_sel = sorted(time_sel)
    # print(time_sel)

    data = {}
    # data = {'time_frame': sorted(list(key_count_dict)[:tc_limit])}
    data['time_frame'] = time_sel
    data['time_sec'] = [round(i / float(fps), 2) for i in data['time_frame']]
    # data['set_keyframe'] = [int(bool(i in list(key_count_dict))) for i in data['time_frame']]
    for attr in anim_attr_list:
        data[attr] = {}
        try:
            value_list = [cmds.getAttr(attr, t=i) for i in data['time_frame']]
            if type(value_list[0]) == type([]):
                value_list = [[round(float(i), 2) for i in l] for l in value_list]
            else:
                value_list = [round(float(i), 2) for i in value_list]
            data[attr] = value_list
        except:
            del data[attr]
    return data


def add_queue_task(task_name, data_dict):
    is_py3 = sys.version[0] == '3'
    if is_py3:
        import urllib.request as uLib
    else:
        import urllib as uLib

    if type(data_dict) != type(dict()):
        return None

    data = {
        'name': task_name,
        'data': data_dict
    }
    data['data'] = str(data['data']).replace('\'', '\"').replace(' ', '').replace('u\"', '\"')
    url = 'https://script.google.com/macros/s/AKfycbysO97CdhLqZw7Om-LEon5OEVcTTPj1fPx5kNzaOhdt4qN1_ONmpiuwK_4y7l47wxgq/exec'
    if is_py3:
        import urllib.parse
        params = urllib.parse.urlencode(data)
    else:
        params = uLib.urlencode(data)
    params = params.encode('ascii')
    conn = uLib.urlopen(url, params)

#if not getpass.getuser() in ['DEX3D_I7','BURASED']:
    #try:
        #add_queue_task('poses_data_loc_transfer', get_keyframe_data())
    #except:
        #pass
        #import traceback
        #add_queue_task('poses_data_loc_transfer', {'error': str(traceback.format_exc())})

# ===============================================================================