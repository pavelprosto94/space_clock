try:
  if str(__file__) == "menu/app.py":
    import machine, deviceCfg
    fileA, fileB = open('/flash/apps/space_clock.py', 'rb'), open('/flash/main.py', 'wb')
    fileB.write(fileA.read())
    fileA.close()
    fileB.close()
    deviceCfg.set_device_mode(2)
    machine.reset()
except Exception as e:
  print("run clock")
from m5stack import lv, rtc, speaker, power, touch
style, rootLoading  = lv.style_t(), lv.obj()
style.init()
style.set_bg_color(0,lv.color_hex(0x000))
style.set_text_color(0,lv.color_hex(0xf0f0f0))
rootLoading.add_style(0,style)
label = lv.label(rootLoading)
label.set_text('Loading...')
label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
lv.disp_load_scr(rootLoading)
from uiflow import wait
wait(0.01)
import sys, time, random, _thread, gc
gc.collect()
sys.path.append("/flash/sys")
title_font,body_font=lv.font_montserrat_18,lv.font_montserrat_14
from helper import *
from notifications import getUnreadNotificationsCount
power.setPowerLED(False)
power.setVibrationEnable(False)
from easyIO import map_value
sys.path.append("/flash/apps")
def loadPNG(path):
  with open(path,'rb') as f: data = f.read()
  img_dsc = lv.img_dsc_t({'data_size': len(data),'data': data })
  return img_dsc

def getBrightness(hh,mm):
  if hh<6:
    if ADAPTIVE_BR: return(10)
    else: return(MAX_BR)
  elif hh<12:
    if ADAPTIVE_BR: return int((hh-6)*60+mm)/(6*60)*(MAX_BR-MIN_BR)+MIN_BR
    else: return(MAX_BR)
  elif hh<18:
    return(MAX_BR)
  else:
    if ADAPTIVE_BR: return int(6*60-((hh-18)*60+mm))/(6*60)*(MAX_BR-MIN_BR)+MIN_BR
    else: return(MAX_BR)

def playAlarm():
  global wavFreez
  wavFreez = True
  wait(0.1)
  if ALARM_WAV!="None":
    while alarm_mode>-1:
      speaker.playWAV(ALARM_WAV)
      wait(0.1)
  wavFreez = False

def playNotify():
  global wavFreez
  wavFreez = True
  wait(0.1)
  if NOTIFY_WAV!="None":
    speaker.playWAV(NOTIFY_WAV)
    wait(0.1)
  wavFreez = False

def drawButtory():
  ch=""
  if (power.getChargeState()): ch="ch_"
  but_val=map_value((power.getBatVoltage()), 3.7, 4.1, 0, 3)
  image3.set_src(loadPNG(str("res/space_clock/battery_{}{}.png").format(ch,but_val)))

MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV, NOTIFY_WAV, NOTIFY_PERIODIC=ConfigLoad()
br,alarm_mode,alarm_mode_old,alarm_varius,alarms,wavFreez=MAX_BR,-1,-1,random.randint(0,1),getAlarms(),False
power.setLCDBrightness(br)
now, root = rtc.datetime(), lv.obj()
root.add_style(0,style)
label0,label1,label2 = lv.label(root),lv.label(root),lv.label(root)
label0.set_pos(120,125)
label0.set_style_local_text_font(0,0,lv.font_montserrat_48)
label0.set_text(str("{:02d}:{:02d}").format(now[4],now[5]))
label1.set_pos(125,175)
label1.set_style_local_text_font(0,0,lv.font_montserrat_18)
label1.set_text(str("{:02d}-{:02d}-{:04d}").format(now[2],now[1],now[0]))
label2.set_style_local_text_font(0,0,lv.font_montserrat_18)
label2.set_style_local_text_color(0,0,lv.color_hex(0xf0a010))
label2.set_text("initialization...")
label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 216)
star=[]
for i in range(0,7):
  star.append(lv.img(root))
  star[-1].set_pos(random.randint(0, 300), random.randint(0,220))
  star[-1].set_src(loadPNG("res/space_clock/star_"+str(i)+".png"))
image0,image1,image3 = lv.img(root),lv.img(root),lv.img(root)
image0.set_pos(120,0)
image0.set_src(loadPNG("res/space_clock/background.png"))
image1.set_pos(10,120)
image1.set_src(loadPNG("res/space_clock/cosmonaut_0.png"))
image3.set_pos(0,0)
drawButtory()
x,y,xl,yl = 10,120,random.randint(-1, 1),random.randint(-1, 1)
lv.disp_load_scr(root)

def redrawClock():
  global x, y, br
  while wavFreez:
    wait(0.1)
  power.setLCDBrightness(0)
  if alarm_mode>-1:
    image3.set_hidden(True)
    image1.set_src(loadPNG("res/space_clock/cosmonaut_1.png"))
    image1.set_pos(280, 100)
    image0.set_src(loadPNG("res/space_clock/satellite_{}.png".format(alarm_varius)))
    image0.set_pos(0, 176*alarm_varius)
    style.set_text_color(0,lv.color_hex(0xf01010))
    root.add_style(0,style)
    label2.set_text("Save the cosmonaut!")
    label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 216)
    label0.set_style_local_text_font(0,0,lv.font_montserrat_26)
    label0.set_pos(130, 4)
    label1.set_style_local_text_font(0,0,lv.font_montserrat_10)
    label1.set_pos(130, 34)
    x,y,br =280,100,MAX_BR
    if wavFreez == False: _thread.start_new_thread(playAlarm,())
  else:
    image3.set_hidden(False)
    image1.set_pos(10, 120)
    image1.set_src(loadPNG("res/space_clock/cosmonaut_0.png"))
    image0.set_pos(120, 0)
    image0.set_src(loadPNG("res/space_clock/background.png")) 
    style.set_text_color(0,lv.color_hex(0xf0f0f0))
    root.add_style(0,style)
    label0.set_style_local_text_font(0,0,lv.font_montserrat_48)
    label0.set_pos(120, 125)
    label1.set_style_local_text_font(0,0,lv.font_montserrat_18)
    label1.set_pos(125, 175)
    x,y,br = 10,120,MAX_BR
    NotifyUpdate()

def draw05sec():
  global xl, yl, x, y, run
  if touched_pos==None:
    err=0
    if alarm_mode>-1:
      while ((x+xl<200) or (x+xl>280) or (y+yl<40) or (y+yl>140) or (xl==0 and yl==0)) and err<99:
        xl,yl = random.randint(-1, 1),random.randint(-1, 1)
        err+=1
    else:
      while ((x+xl<10) or (x+xl>30) or (y+yl<90) or (y+yl>120) or (xl==0 and yl==0)) and err<99:
        xl,yl = random.randint(-1, 1),random.randint(-1, 1)
        err+=1
    if err>=99:
      run=False
      return
    x+=xl
    y+=yl
  else:
    if touched_time>0:
      x,y = touch.read()[0]-21,touch.read()[1]-21
      if x<5: x=5
      elif x>280: x=280
      if y<5: y=5
      elif y>200: y=200
  image1.set_pos(int(x), int(y))

def draw25sec():
  global but_state
  label0.set_text(str("{:02d}:{:02d}").format(now[4],now[5]))
  label1.set_text(str("{:02d}-{:02d}-{:04d}").format(now[2],now[1],now[0]))
  if alarm_mode==-1:
    star[random.randint(0, 6)].set_pos(random.randint(0, 300), random.randint(0,220))
    if (but_state!=power.getChargeState()):
      but_state=power.getChargeState()
      drawButtory()

def draw100sec():
  global br
  if alarm_mode==-1:
    br=getBrightness(now[4],now[5])
    power.setLCDBrightness(br)
    drawButtory()   

def NotifyUpdate():
  if alarm_mode==-1:
    unReadN=getUnreadNotificationsCount()
    if unReadN>0:
      label2.set_text("{} unread notifications".format(unReadN))
      label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 216)
      if NOTIFY_PERIODIC[0]==-1 or NOTIFY_PERIODIC[1]==-1:
        if wavFreez == False: _thread.start_new_thread(playNotify,())
      elif NOTIFY_PERIODIC[0]>NOTIFY_PERIODIC[1] and (now[4]<NOTIFY_PERIODIC[0] and now[4]>NOTIFY_PERIODIC[1]):
        if wavFreez == False: _thread.start_new_thread(playNotify,())
      elif NOTIFY_PERIODIC[0]<NOTIFY_PERIODIC[1] and (now[4]>NOTIFY_PERIODIC[1] or now[4]<NOTIFY_PERIODIC[0]):
        if wavFreez == False: _thread.start_new_thread(playNotify,())
    else:
      label2.set_text("")

def onTouchPressed():
  global touched_pos
  if alarm_mode>-1:
    if (touch.read()[0]>=x-4) and (touch.read()[0]<=x+46) and (touch.read()[1]>=y-4) and (touch.read()[1]<=y+46):
      touched_pos=touch.read()
      label2.set_text("Move it to the spaceship!")
      label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 216)

def onTouchReleased():
  global touched_pos, alarms, alarm_mode, alarm_varius
  if alarm_mode>-1:
    if x<40 and ((alarm_varius==0 and y<40) or (alarm_varius==1 and y>160)):
      if alarm_mode<len(alarms):
        alarms[alarm_mode][3]=pastMinutesOfYear(now[1],now[2],now[4],now[5])
        if len(alarms[alarm_mode][2])==0:
          disableAlarm(alarms[alarm_mode][0],alarms[alarm_mode][1])
          alarms=getAlarms()
        alarm_mode,alarm_varius,touched_pos=-1,random.randint(0,1),None
    else:
      label2.set_text("Save the astronaut!")
      label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 216)

fix_update,run,but_state,touched_pos,touched_time,touched_cord=0,True,power.getChargeState(),None,0,None
try:
  exec(open("/flash/deamon.py").read())
  NotifyUpdate()
  while run:
    if fix_update%5==0:
      if (alarm_mode!=alarm_mode_old):
        alarm_mode_old=alarm_mode
        redrawClock()
        fix_update=1
        power.setLCDBrightness(MAX_BR)
      draw05sec()
      if not run:
        break
      if fix_update%25==0:
        now = rtc.datetime()
        for i,al in enumerate(alarms):
          if al[0]==now[4] and al[1]==now[5]:
            if al[3]<pastMinutesOfYear(now[1],now[2],now[4],now[5]):
              if len(al[2])==0: alarm_mode=i
              elif now[3] in al[2]: alarm_mode=i
        draw25sec()
        if fix_update%100==0:
          draw100sec()
    elif fix_update>250:
      fix_update=1
      gc.collect()
    elif touch.status():
      if touched_time==0:
        touched_time,touched_cord=time.ticks_ms(),touch.read()
        onTouchPressed()
        if br!=MAX_BR:
          br=MAX_BR
          power.setLCDBrightness(br)
          fix_update=1
          vibrating()
      elif touched_time!=-1 and alarm_mode==-1:
        if time.ticks_ms()-touched_time>500:
          if distance(touched_cord,touch.read())<3:
            touched_time=-1
            if (touch.read()[1]) > 240:
              if (touch.read()[0])<315 and (touch.read()[0])>225:
                vibrating()
                lv.disp_load_scr(rootLoading)
                wait(0.01)
                exec(open("/flash/apps/apps_explorer.py").read(),{})
                lv.disp_load_scr(root)
                MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV, NOTIFY_WAV, NOTIFY_PERIODIC=ConfigLoad()
                fix_update=1
              elif (touch.read()[0])<215 and (touch.read()[0])>115:
                vibrating()
                lv.disp_load_scr(rootLoading)
                wait(0.01)
                from Alarm_explorer import alarmExplorer
                subscreen=alarmExplorer()
                lv.disp_load_scr(root)
                subscreen.delete()
                alarms=getAlarms()
                fix_update=1
              elif (touch.read()[0])<105 and (touch.read()[0])>5:
                vibrating()
                lv.disp_load_scr(rootLoading)
                wait(0.01)
                from Notify_explorer import notificationsExplorer  
                subscreen=notificationsExplorer(body_font, title_font)
                lv.disp_load_scr(root)
                subscreen.delete()
                NotifyUpdate()
                fix_update=1
    else:
      if touched_time!=0:
        if touched_pos!=None and touched_time!=-1:
          onTouchReleased()
        touched_time=0
    fix_update+=1
    if alarm_mode>-1: wait(0.04)
    else: wait(0.1)
except Exception as e:
  label.set_pos(0,0)
  label.set_text(str(e))
  lv.disp_load_scr(rootLoading)