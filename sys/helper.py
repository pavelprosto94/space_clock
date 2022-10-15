from m5stack import power
from math import sqrt
from uiflow import wait
import time
import os
import json

def distance(cord1, cord2):
  c = sqrt((cord2[0]-cord1[0])**2 + (cord2[1]-cord1[1])**2)
  return c
  
def fileExist(path="/"):
  filename=path[path.rfind("/")+1:]
  dirpath=path[:path.rfind("/")]
  if (filename in os.listdir(dirpath)):
    return True
  else:
    return False

def safetyLoadJson(data, key, default=None):
  if key in data:
    return data[key]
  else:
    return default
  
def vibrating(strong=1):
  power.setVibrationEnable(True)
  wait(strong/10)
  power.setVibrationEnable(False)

def pastMinutesOfYear(month=0, days=0, hours=0, minutes=0):
  daysOfMonth = [ 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
  lastDays = 0
  for i in range(0,month-1):
    lastDays+=daysOfMonth[i]
  return lastDays*24*60+days*24*60+hours*60+minutes

def getAlarms():
  alarms=[]
  wAlf=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
  data = {}
  data['alarms'] = []
  if fileExist('/flash/alarm.txt'):
    with open('/flash/alarm.txt', 'r') as json_file:
      data = json.load(json_file)
  if len(data['alarms'])>0:
    for d in data['alarms']:
      if d['enable']:
        l=[]
        l.append(d['hh'])
        l.append(d['mm'])
        weeks=[]
        for i,w in enumerate(wAlf):
          if w in d['weekRepeat'][0]:
            weeks.append(i)
        l.append(weeks)
        l.append(d['lastRun'])
        alarms.append(l)
  return(alarms)

def disableAlarm(hours=0, minutes=0):
  data = {}
  data['alarms'] = []
  if fileExist('/flash/alarm.txt'):
    with open('/flash/alarm.txt', 'r') as json_file:
      data = json.load(json_file)
  if len(data['alarms'])>0:
    for d in data['alarms']:
      if d['enable']:
        if d['hh']==hours and d['mm']==minutes and len(d['weekRepeat'][0])==0:
            d['enable']=False
            break
  with open('/flash/alarm.txt', 'w') as outfile:
    json.dump(data, outfile)
    
def ConfigLoad():
  data = {}
  data['setup'] = []
  MAX_BR, ADAPTIVE_BR, MIN_BR, =100, True, 10  
  UTC_ZONE=3
  ALARM_WAV='res/fallout.wav'
  NOTIFY_WAV, NOTIFY_PERIODIC='res/link.wav', [-1,-1]
  if fileExist('/flash/setup.txt'):
    with open('/flash/setup.txt', 'r') as json_file:
      data = json.load(json_file)
  MAX_BR=safetyLoadJson(data['setup'],'MAX_BR',MAX_BR)
  ADAPTIVE_BR=safetyLoadJson(data['setup'],'ADAPTIVE_BR',ADAPTIVE_BR)
  MIN_BR=safetyLoadJson(data['setup'],'MIN_BR',MIN_BR)
  UTC_ZONE=safetyLoadJson(data['setup'],'UTC_ZONE',UTC_ZONE)
  ALARM_WAV=safetyLoadJson(data['setup'],'ALARM_WAV',ALARM_WAV)
  NOTIFY_WAV=safetyLoadJson(data['setup'],'NOTIFY_WAV',NOTIFY_WAV)
  NOTIFY_PERIODIC=safetyLoadJson(data['setup'],'NOTIFY_PERIODIC',NOTIFY_PERIODIC)
  return MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV, NOTIFY_WAV, NOTIFY_PERIODIC