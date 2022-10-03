try:
  if str(__file__) == "menu/app.py":
    import machine
    fileA = open('/flash/apps/Alarm_explorer.py', 'rb')
    fileB = open('/flash/main.py', 'wb')
    fileB.write(fileA.read())
    fileA.close()
    fileB.close()
    machine.reset()
except Exception as e:
  print("run alarm")
from m5stack import M5Screen, rtc, power, touch
from m5stack_ui import *
from uiflow import wait
from math import *
import sys
import json
import time
import os
sys.path.append("/flash/sys")
from helper import vibrating, distance, fileExist, pastMinutesOfYear

def alarmEditor(screen,hh=-1,mm=-1,weekRepeat=None):
  now = rtc.datetime()
  val=[]
  ans=[]
  if hh>-1 and mm>-1:
    val=[hh,mm]
  else:
    val = [now[4],now[5]]
  wAlf=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
  WeekVal=[False]*7
  if weekRepeat!=None:
    for i,w in enumerate(wAlf):
      if w in weekRepeat:
        WeekVal[i]=True
  
  num_max=[23,59]
  numbo=[[],[]]
  numbx=[[],[]]
  numbi=[[],[]]
  numbv=[[],[]]
  numVal=[]
  
  screen1 = screen.get_new_screen()
  screen.load_screen(screen1)
  M5Label("Set the hours:", x=10, y=12, color=0x226577, font=FONT_MONT_14, parent=screen1)
  M5Label("Set the minutes:", x=10, y=82, color=0x226577, font=FONT_MONT_14, parent=screen1)
  M5Label("Choose the need to repeat:", x=10, y=152, color=0x226577, font=FONT_MONT_14, parent=screen1)
  M5Label("save", x=142, y=224, color=0xd84949, font=FONT_MONT_14, parent=screen1)
  M5Label("cancel", x=238, y=224, color=0xd84949, font=FONT_MONT_14, parent=screen1)
  for k in range(0,2):
    for i in range(0,7):
      tmp_val=val[k]+(i-3)
      if tmp_val<0:
        tmp_val=num_max[k]+tmp_val+1
      elif tmp_val>num_max[k]:
        tmp_val=tmp_val-num_max[k]-1
      numbo[k].append(M5Label(str("{:02d}").format(tmp_val), x=i*40+25, y=70*k+40, color=0x788290, font=FONT_MONT_18, parent=screen1))
      numbx[k].append(i*40+10)
      numbi[k].append(tmp_val)
      numbv[k].append(i!=3)
      if i==3:
        numbo[k][i].set_hidden(True)
    numVal.append(M5Label(str("{:02d}").format(val[k]), x=138, y=70*k+32, color=0x000000, font=FONT_MONT_30, parent=screen1))
  
  def col_WeekBut(i):
    tmp_cl=0x404b5a
    tmp_cl_b=0xe8e9ed
    if i>=5:
      tmp_cl=0xf05050
    if WeekVal[i]:
      tmp_cl_b=0x39bdbf
      tmp_cl=0xffffff
      if i>=5:
        tmp_cl=0xffe1c5
    return tmp_cl,tmp_cl_b
        
  def pressed_WeekBut(i):
    WeekVal[i]=not WeekVal[i]
    tmp_cl,tmp_cl_b=col_WeekBut(i)
    WeekBut[i].set_bg_color(tmp_cl_b)
    WeekBut[i].set_btn_text_color(tmp_cl)
    vibrating()

  WeekBut=[]
  for i in range(0,7):
    tmp_cl,tmp_cl_b=col_WeekBut(i)
    WeekBut.append(M5Btn(wAlf[i],i*45+5,175,40,40,tmp_cl_b,tmp_cl,FONT_MONT_14, parent=screen1))

  run=True
  old_x=-1
  k=-1
  touched_time = 0
  touched_cord = None
  while run:
    if touch.status():
      if touched_time==0:
        touched_time=time.ticks_ms()
        touched_cord = touch.read()
      elif touched_time!=-1:
        if time.ticks_ms()-touched_time>500:
          if distance(touched_cord,touch.read())<3:
            touched_time=-1
            if (touch.read()[1]) > 240:
              if (touch.read()[0])<315 and (touch.read()[0])>225:
                vibrating()
                run=False
                screen1 = screen.get_act_screen()
                return screen1,None
              elif (touch.read()[0])<215 and (touch.read()[0])>115:
                vibrating()
                run=False
                for i,w in enumerate(wAlf):
                  if WeekVal[i]:
                    ans.append(w)
                val.append(ans)
                screen1 = screen.get_act_screen()
                return screen1,val
      if old_x==-1:
        old_x=touch.read()[0]
        y=touch.read()[1]
        k=-1
        if y>20:
          if y<100:
            k=0
          elif y<160:
            k=1
          elif y>170 and y<200:
            i=0
            if old_x>50:
              i=int((old_x-50)/45)+1
              if i<0:
                i=0
            pressed_WeekBut(i)
      else:
        if k!=-1:
          alfa_x=touch.read()[0]-old_x
          old_x=touch.read()[0]
          for i in range(0,7):
            new_x=numbx[k][i]+alfa_x
            vec=0
            while new_x<0:
              new_x+=7*40
              vec=+1
            while new_x>7*40:
              new_x-=7*40
              vec=-1
            numbx[k][i]=new_x
            numbo[k][i].set_pos(x=numbx[k][i]+15, y=70*k+40)
            if vec!=0:
              ind=i-vec
              if ind>6:
                ind=0
              elif ind<0:
                ind=6
              numbi[k][i]=numbi[k][ind]+vec
              if numbi[k][i]<0:
                numbi[k][i]=num_max[k]
              elif numbi[k][i]>num_max[k]:
                numbi[k][i]=0
              numbo[k][i].set_text(str("{:02d}").format(numbi[k][i]))
            if (new_x>110 and new_x<150) != numbv[k][i]:
              numbv[k][i]=not numbv[k][i]
              if numbv[k][i]:
                val[k]=numbi[k][i]
                numVal[k].set_text(str("{:02d}").format(val[k]))
              numbo[k][i].set_hidden(numbv[k][i])
    else:
      touched_time=0
      if old_x!=-1:
        old_x=-1
        if k!=-1:
          power.setVibrationEnable(True)
          for i in range(0,7):
            tmp_val=val[k]+(i-3)
            if tmp_val<0:
              tmp_val=num_max[k]+tmp_val+1
            elif tmp_val>num_max[k]:
              tmp_val=tmp_val-num_max[k]-1
            numbo[k][i].set_text(str("{:02d}").format(tmp_val))
            numbo[k][i].set_pos(x=i*40+25, y=70*k+40)
            numbx[k][i]=i*40+10
            numbi[k][i]=tmp_val
            numbv[k][i]=(i==3)
            numbo[k][i].set_hidden(numbv[k][i])
          k=-1
          wait(0.01)
          power.setVibrationEnable(False)
    wait(0.01)


def alarmExplorer(screen=None):
  if screen==None:
    screen = M5Screen()
  screen0 = screen.get_new_screen()
  screen.load_screen(screen0)
  val=[]
  data = {}
  labels_t=[]
  labels_w=[]
  btn_del=[]
  btn_enbl=[]
  lines=[]
  label0=M5Label("The alarm list is empty.\nPress \"+add\" to add a new.", x=10, y=12, color=0x226577, font=FONT_MONT_14)
  label1=M5Label("+ add", x=140, y=224, color=0xd84949, font=FONT_MONT_14, parent=screen0)
  M5Label("cancel", x=238, y=224, color=0xd84949, font=FONT_MONT_14, parent=screen0)
  
  def onSwitch():
    ind=int(touched_cord[1]/55)
    data['alarms'][ind]['enable']=not data['alarms'][ind]['enable']
  
  def displayAlarms():
    if len(data['alarms'])==0:
      label0.set_hidden(False)
    else:
      label0.set_hidden(True)
      if len(data['alarms'])>=4:
        label1.set_hidden(True)
      else:
        label1.set_hidden(False)
      for i,d in enumerate(data['alarms']):
        wl=""
        if len(d['weekRepeat'][0])>0:
          for k,iw in enumerate(d['weekRepeat'][0]):
            lbl=""
            if len(d['weekRepeat'][0])>1 and k<len(d['weekRepeat'][0])-1:
              lbl=", "
            wl+=str(iw)+lbl
        if i>=len(labels_t):
          labels_t.append(M5Label(str("{:02d}:{:02d}").format(d['hh'],d['mm']), x=20, y=55*i+5, color=0x000000, font=FONT_MONT_30, parent=screen0))
          labels_w.append(M5Label(str(wl), x=24, y=55*i+35, color=0x788290, font=FONT_MONT_10, parent=screen0))
          lines.append(M5Line(1, 55*i+55, 319, 55*i+55, 0xa9a9a9, 1))
          btn_del.append(M5Img("res/trash_can_icon.png",280,55*i+12,30,30))
          btn_enbl.append(M5Switch(220,55*i+14,))
          btn_enbl[-1].on(onSwitch)
          btn_enbl[-1].off(onSwitch)
          if (d['enable']):
            btn_enbl[-1].set_on()
          else:
            btn_enbl[-1].set_off()
        else:
          labels_t[i].set_text(str("{:02d}:{:02d}").format(d['hh'],d['mm']))
          labels_t[i].set_hidden(False)
          labels_w[i].set_text(str(wl))
          labels_w[i].set_hidden(False)
          lines[i].set_hidden(False)
          btn_del[i].set_hidden(False)
          btn_enbl[i].set_hidden(False)
          if (d['enable']):
            btn_enbl[i].set_on()
          else:
            btn_enbl[i].set_off()
    for i in range(len(data['alarms']),len(labels_t)):
      labels_t[i].set_hidden(True)
      labels_w[i].set_hidden(True)
      lines[i].set_hidden(True)
      btn_del[i].set_hidden(True)
      btn_enbl[i].set_hidden(True)

  data['alarms'] = []
  if fileExist('/flash/alarm.txt'):
    with open('/flash/alarm.txt', 'r') as json_file:
      data = json.load(json_file)
    displayAlarms()

  run=True
  touched_time = 0
  touched_cord = None
  vibrating()
  while run:
    if touch.status():
      if touched_time==0:
        touched_time=time.ticks_ms()
        touched_cord = touch.read()
      elif touched_time!=-1:
        if time.ticks_ms()-touched_time>500:
          if distance(touched_cord,touch.read())<3:
            touched_time=-1
            if (touch.read()[1]) > 240:
              if (touch.read()[0])<315 and (touch.read()[0])>225:
                run=False
              elif (touch.read()[0])<215 and (touch.read()[0])>115:
                if len(data['alarms'])<4:
                  vibrating()
                  screen0 = screen.get_act_screen()
                  screen1,ans=alarmEditor(screen)
                  screen.load_screen(screen0)
                  screen.del_screen(screen1)
                  if ans!=None:
                    wR=[]
                    if len(ans)>2:
                      for w in ans[2:]:
                        wR.append(w)
                    data['alarms'].append({
                        'hh': ans[0],
                        'mm': ans[1],
                        'lastRun': 0,
                        'enable': True,
                        'weekRepeat': wR
                    })
                    displayAlarms()
    else:
      if (touched_time>0):
        if distance(touched_cord,touch.read())<3:
          if (touch.read()[1]) < 55*4:
            ind=int(touched_cord[1]/55)
            if ind<len(data['alarms']):
              if (touch.read()[0]) > 280:
                Msgbox = M5Msgbox()
                Msgbox.add_btns(["Yes","No"])
                Msgbox.set_text("Do you want to delete the alarm?\n{:02d}:{:02d}".format(data['alarms'][ind]['hh'],data['alarms'][ind]['mm']))
                ans=Msgbox.get_active_btn_text()
                vibrating()
                while ans==None:
                  ans=Msgbox.get_active_btn_text()
                if ans=="Yes":
                  data['alarms'].pop(ind)
                  displayAlarms()
              elif (touch.read()[0]) < 200:
                vibrating()
                screen0 = screen.get_act_screen()
                screen1,ans=alarmEditor(screen,data['alarms'][ind]['hh'],data['alarms'][ind]['mm'],data['alarms'][ind]['weekRepeat'][0])
                screen.load_screen(screen0)
                screen.del_screen(screen1)
                if ans!=None:
                  wR=[]
                  if len(ans)>2:
                    for w in ans[2:]:
                      wR.append(w)
                  data['alarms'].pop(ind)
                  data['alarms'].insert(ind,{
                        'hh': ans[0],
                        'mm': ans[1],
                        'lastRun': 0,
                        'enable': True,
                        'weekRepeat': wR
                      })
                  displayAlarms()
      touched_time=0
  vibrating()
  now = rtc.datetime()
  for d in data['alarms']:
    d['lastRun']=pastMinutesOfYear(now[1],now[2],now[4],now[5])
  with open('/flash/alarm.txt', 'w') as outfile:
      json.dump(data, outfile)
  screen0 = screen.get_act_screen()
  return screen0

try:
  if str(__file__) == "flow/m5ucloud.py":
    screen = M5Screen()
    alarmExplorer(screen)
except Exception as e:
  import machine
  machine.reset()