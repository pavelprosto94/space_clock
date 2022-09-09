from m5stack import *
from m5stack_ui import *
from uiflow import *
from math import *
import time
import os
import json

def distance(cord1, cord2):
  c = sqrt((cord2[0]-cord1[0])**2 + (cord2[1]-cord1[1])**2)
  return c

def vidro():
  power.setVibrationEnable(True)
  wait(0.1)
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
  if ('alarm.txt' in os.listdir('/flash')):
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
  if ('alarm.txt' in os.listdir('/flash')):
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