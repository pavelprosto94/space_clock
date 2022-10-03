try:
  if str(__file__) == "menu/app.py":
    import machine
    import deviceCfg
    fileA = open('/flash/apps/space_clock.py', 'rb')
    fileB = open('/flash/main.py', 'wb')
    fileB.write(fileA.read())
    fileA.close()
    fileB.close()
    deviceCfg.set_device_mode(2)
    deviceCfg.set_startup_hold(False)
    machine.reset()
except Exception as e:
  print("run clock")
from m5stack import lv, M5Screen
M5Screen().clean_screen()
M5Screen().set_screen_bg_color(0x000000)
style = lv.style_t()
style.init()
style.set_bg_color(0,lv.color_hex(0x000))
style.set_text_color(0,lv.color_hex(0xf0f0f0))
rootLoading = lv.obj()
rootLoading.add_style(0,style)
label = lv.label(rootLoading)
label.align(rootLoading,lv.ALIGN.CENTER, -20, 0)
label.set_text('Loading...')
lv.disp_load_scr(rootLoading)
from uiflow import wait
wait(0.01)
import sys, time, random, _thread
sys.path.append("/flash/sys")
title_font=lv.font_montserrat_18
body_font=lv.font_montserrat_14
from helper import *
from m5stack import rtc, speaker, power, touch
from easyIO import map_value
from math import *
sys.path.append("/flash/apps")
def loadPNG(path):
  try:
    with open(path,'rb') as f:
      png_data = f.read()
  except:
    return None

  img_cogwheel_argb = lv.img_dsc_t({
    'data_size': len(png_data),
    'data': png_data
  })
  return(img_cogwheel_argb)

def getBrightness(hh,mm):
  if hh<6:
    if ADAPTIVE_BR:
      return(10)
    else:
      return(MAX_BR)
  elif hh<12:
    if ADAPTIVE_BR:
      return int((hh-6)*60+mm)/(6*60)*(MAX_BR-MIN_BR)+MIN_BR
    else:
      return(MAX_BR)
  elif hh<18:
    return(MAX_BR)
  else:
    if ADAPTIVE_BR:
      return int(6*60-((hh-18)*60+mm))/(6*60)*(MAX_BR-MIN_BR)+MIN_BR
    else:
      return(MAX_BR)

wavFreez = False
def playAlarm():
  global wavFreez
  wavFreez = True
  wait(0.1)
  while alarm_mode>-1:
    speaker.playWAV(ALARM_WAV)
    wait(0.1)
  wavFreez = False

def drawButtory():
  ch=""
  if (power.getChargeState()):
    ch="ch_"
  but_val=map_value((power.getBatVoltage()), 3.7, 4.1, 0, 3)
  image3.set_src(loadPNG(str("res/space_clock/battery_{}{}.png").format(ch,but_val)))

now = rtc.datetime()
MAX_BR=100
ADAPTIVE_BR=True
MIN_BR=10
ALARM_WAV='res/fallout.wav'
MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV=ConfigLoad()
br=MAX_BR
M5Screen().set_screen_brightness(br)
alarm_mode=-1
alarm_varius=random.randint(0,1)
alarm_mode_old=-1
alarms=getAlarms()

root = lv.obj()
root.add_style(0,style)
label0 = lv.label(root)
label0.set_pos(120,125)
label0.set_style_local_text_font(0,0,lv.font_montserrat_48)
label0.set_text(str("{:02d}:{:02d}").format(now[4],now[5]))
label1 = lv.label(root)
label1.set_pos(125,175)
label1.set_style_local_text_font(0,0,lv.font_montserrat_18)
label1.set_text(str("{:02d}-{:02d}-{:04d}").format(now[2],now[1],now[0]))
label2 = lv.label(root)
label2.set_style_local_text_font(0,0,lv.font_montserrat_18)
label2.set_style_local_text_color(0,0,lv.color_hex(0xf0a010))
label2.set_text("")
label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 216)
star=[]
for i in range(0,7):
  star.append(lv.img(root))
  star[-1].set_pos(random.randint(0, 300), random.randint(0,220))
  star[-1].set_src(loadPNG("res/space_clock/star_"+str(i)+".png"))
image0 = lv.img(root)
image0.set_pos(120,0)
image0.set_src(loadPNG("res/space_clock/background.png"))
image1 = lv.img(root)
image1.set_pos(10,120)
image1.set_src(loadPNG("res/space_clock/cosmonaut_0.png"))
image3 = lv.img(root)
image3.set_pos(0,0)
drawButtory()
x = 10
y = 120
xl = random.randint(-1, 1)
yl = random.randint(-1, 1)
lv.disp_load_scr(root)

def redrawClock():
  global x
  global y
  global br
  while wavFreez:
    wait(0.1)
  if alarm_mode>-1:
    M5Screen().set_screen_brightness(0)
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
    x=280
    y=100
    br=MAX_BR
    M5Screen().set_screen_brightness(br)
    if wavFreez == False:
      _thread.start_new_thread(playAlarm,())
  else:
    M5Screen().set_screen_brightness(0)
    image3.set_hidden(False)
    label2.set_text("")
    label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 216)
    image1.set_pos(10, 120)
    image1.set_src(loadPNG("res/space_clock/cosmonaut_0.png"))
    image0.set_pos(120, 0)
    image0.set_src(loadPNG("res/space_clock/background.png")) 
    style.set_text_color(0,colorWhite)
    root.add_style(0,style)
    label0.set_style_local_text_font(0,0,lv.font_montserrat_48)
    label0.set_pos(120, 125)
    label1.set_style_local_text_font(0,0,lv.font_montserrat_18)
    label1.set_pos(125, 175)
    x = 10
    y = 120
    br=MAX_BR
    M5Screen().set_screen_brightness(br)

def draw05sec():
  global xl
  global yl
  global x
  global y
  global run
  if touched_pos==None:
    err=0
    if alarm_mode>-1:
      while ((x+xl<200) or (x+xl>280) or (y+yl<40) or (y+yl>140) or (xl==0 and yl==0)) and err<99:
        xl = random.randint(-1, 1)
        yl = random.randint(-1, 1)
        err+=1
    else:
      while ((x+xl<10) or (x+xl>30) or (y+yl<90) or (y+yl>120) or (xl==0 and yl==0)) and err<99:
        xl = random.randint(-1, 1)
        yl = random.randint(-1, 1)
        err+=1
    if err>=99:
      run=False
      return
    x+=xl
    y+=yl
  else:
    if touched_time>0:
      x=touch.read()[0]-21
      y=touch.read()[1]-21
      if x<5:
        x=5
      elif x>280:
        x=280
      if y<5:
        y=5
      elif y>200:
        y=200
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
    M5Screen().set_screen_brightness(br)
    drawButtory()   

def onTouchPressed():
  global touched_pos
  if alarm_mode>-1:
    if (touch.read()[0]>=x-4) and (touch.read()[0]<=x+46) and (touch.read()[1]>=y-4) and (touch.read()[1]<=y+46):
      touched_pos=touch.read()
      label2.set_text("Move it to the spaceship!")
      label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 216)

def onTouchReleased():
  global touched_pos
  global alarms
  global alarm_mode
  global alarm_varius
  if alarm_mode>-1:
    if x<40 and ((alarm_varius==0 and y<40) or (alarm_varius==1 and y>160)):
      if alarm_mode<len(alarms):
        alarms[alarm_mode][3]=pastMinutesOfYear(now[1],now[2],now[4],now[5])
        if len(alarms[alarm_mode][2])==0:
          disableAlarm(alarms[alarm_mode][0],alarms[alarm_mode][1])
          alarms=getAlarms()
        alarm_mode=-1
        alarm_varius=random.randint(0,1)
        touched_pos=None
    else:
      label2.set_text("Save the astronaut!")
      label2.align(root,lv.ALIGN.IN_TOP_MID, 0, 216)

fix_update=0
run = True
but_state=power.getChargeState()
touched_pos=None
touched_time = 0
touched_cord = None
try:
  while run:
    if fix_update%5==0:
      if (alarm_mode!=alarm_mode_old):
        alarm_mode_old=alarm_mode
        redrawClock()
        M5Screen().set_screen_brightness(MAX_BR)
      draw05sec()
      if not run:
        break
      if fix_update%25==0:
        now = rtc.datetime()
        for i,al in enumerate(alarms):
          if al[0]==now[4] and al[1]==now[5]:
            if al[3]<pastMinutesOfYear(now[1],now[2],now[4],now[5]):
              if len(al[2])==0:
                alarm_mode=i
              elif now[3] in al[2]:
                alarm_mode=i
        draw25sec()
        if fix_update%100==0:
          draw100sec()
          fix_update=1
    if touch.status():
      if touched_time==0:
        touched_time=time.ticks_ms()
        touched_cord = touch.read()
        onTouchPressed()
        if br!=MAX_BR:
          br=MAX_BR
          M5Screen().set_screen_brightness(br)
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
                MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV=ConfigLoad()
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
                fix_update=1
    else:
      if touched_time>0 and touched_time!=-1:
        if touched_pos!=None:
          onTouchReleased()
      touched_time=0
    fix_update+=1
    if alarm_mode>-1:
      wait(0.04)
    else:
      wait(0.1)
except Exception as e:
  label.set_pos(0,0)
  label.set_text(str(e))
  lv.disp_load_scr(rootLoading)