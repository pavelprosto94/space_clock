from m5stack import *
from m5stack_ui import *
from uiflow import *
from easyIO import *
import time
import random
from math import *
import sys
import _thread
sys.path.append("/flash/sys")
from helper import *
from alarm import alarmExplorer
from setup import ConfigLoad, ConfigScreen
from notifications import NotificationsScreen

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

screen = M5Screen()
screen.set_screen_brightness(0)
now = rtc.datetime()
MAX_BR=100
ADAPTIVE_BR=True
MIN_BR=10
ALARM_WAV='res/fallout.wav'
MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV=ConfigLoad()
br=MAX_BR
alarm_mode=-1
alarm_varius=random.randint(0,1)
alarm_mode_old=-1
alarms=getAlarms()
#print(alarms)
screen.clean_screen()

#drow Buttory level start
def getButImg():
  ch=""
  if (power.getChargeState()):
    ch="ch_"
  but_val=map_value((power.getBatVoltage()), 3.7, 4.1, 0, 3)
  return str("res/space_clock/battery_{}{}.png").format(ch,but_val)
#drow Buttory level end

#drow redrow block start    
def redrowClock():
  global x
  global y
  global br
  while wavFreez:
    wait(0.1)
  if alarm_mode>-1:
    screen.set_screen_brightness(0)
    image3.set_hidden(True)
    image1.set_img_src("res/space_clock/cosmonaut_1.png")
    image1.set_pos(x=280, y=100)
    image0.set_img_src("res/space_clock/satellite_{}.png".format(alarm_varius))
    image0.set_pos(x=0, y=176*alarm_varius)
    label2.set_text("Save the cosmonaut!")
    label2.set_pos(x=80, y=216)
    label0.set_text_font(FONT_MONT_26)
    label0.set_text_color(0xff0000)
    label0.set_pos(x=130, y=4)
    label1.set_text_font(FONT_MONT_10)
    label1.set_text_color(0xff0000)
    label1.set_pos(x=130, y=34)
    x=280
    y=100
    br=MAX_BR
    screen.set_screen_brightness(br)
    if wavFreez == False:
      _thread.start_new_thread(playAlarm,())
  else:
    screen.set_screen_brightness(0)
    image3.set_hidden(False)
    label2.set_text("")
    image1.set_pos(x=120, y=125)
    image1.set_img_src("res/space_clock/cosmonaut_0.png")
    image0.set_pos(x=120, y=0)
    image0.set_img_src("res/space_clock/background.png") 
    label0.set_text_font(FONT_MONT_48)
    label0.set_text_color(0xffffff)
    label0.set_pos(x=120, y=125)
    label1.set_text_font(FONT_MONT_18)
    label1.set_text_color(0xffffff)
    label1.set_pos(x=125, y=175)
    x = 10
    y = 120
    br=MAX_BR
    screen.set_screen_brightness(br)
#drow redrow block end

#drow every 0.5sec block start
def drow05sec():
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
  image1.set_pos(x=int(x), y=int(y))
#drow every 0.5sec block end

#drow every 2.5sec block start
def drow25sec():
  global but_state
  label0.set_text(str("{:02d}:{:02d}").format(now[4],now[5]))
  label1.set_text(str("{:02d}-{:02d}-{:04d}").format(now[2],now[1],now[0]))
  if alarm_mode==-1:
    star[random.randint(0, 6)].set_pos(x=random.randint(0, 300), y=random.randint(0,220))
    if (but_state!=power.getChargeState()):
      but_state=power.getChargeState()
      image3.set_img_src(getButImg())
#drow every 2.5sec block end

#drow every 10sec block start
def drow100sec():
  global br
  if alarm_mode==-1:
    br=getBrightness(now[4],now[5]) #adaptive brightness
    screen.set_screen_brightness(br) #set brightness

    image3.set_img_src(getButImg()) #update buttory image
#drow every 10sec block end

#init drowing block start
screen.set_screen_bg_color(0x000000)
star=[]
label0 = M5Label(str("{:02d}:{:02d}").format(now[4],now[5]), x=120, y=125, color=0xffffff, font=FONT_MONT_48)
label1 = M5Label(str("{:02d}-{:02d}-{:04d}").format(now[2],now[1],now[0]), x=125, y=175, color=0xffffff, font=FONT_MONT_18)
label2 = M5Label("", x=80, y=216, color=0xff0000, font=FONT_MONT_18)
for i in range(0,7):
  star.append(M5Img("res/space_clock/star_"+str(i)+".png", x=random.randint(0, 300), y=random.randint(0,220)))
image0 = M5Img("res/space_clock/background.png", x=120, y=0)
image1 = M5Img("res/space_clock/cosmonaut_0.png", x=10, y=120)
image3 = M5Img(getButImg(), x=0, y=0)
screen.set_screen_brightness(br)
x = 10
y = 120
xl = random.randint(-1, 1)
yl = random.randint(-1, 1)
#init drowing block end

fix_update=0
run = True
but_state=power.getChargeState()
touched_pos=None
touched_time = 0
touched_cord = None
while run:
  if fix_update%5==0:
    if (alarm_mode!=alarm_mode_old):
      alarm_mode_old=alarm_mode
      redrowClock()
      screen.set_screen_brightness(MAX_BR)
    drow05sec()
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
      drow25sec()
      if fix_update==100:
        drow100sec()
        step=0
  #logic touch
  if touch.status():
    if touched_time==0:
      touched_time=time.ticks_ms()
      touched_cord = touch.read()
      if (touch.read()[0]>=x-4) and (touch.read()[0]<=x+46) and (touch.read()[1]>=y-4) and (touch.read()[1]<=y+46):
        touched_pos=touch.read()
        label2.set_pos(x=60, y=216)
        label2.set_text("Move it to the spaceship!")
      if br!=MAX_BR:
        br=MAX_BR
        screen.set_screen_brightness(br)
        fix_update=0
        vidro()
    elif touched_time!=-1 and alarm_mode==-1:
      if time.ticks_ms()-touched_time>1000:
        if distance(touched_cord,touch.read())<3:
          touched_time=-1
          if (touch.read()[1]) > 240:
            if (touch.read()[0])<315 and (touch.read()[0])>225:
              #print("3 but hold")
              vidro()
              screen0 = screen.get_act_screen()
              screen1=ConfigScreen(screen)
              screen.load_screen(screen0)
              screen.del_screen(screen1)
              MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV=ConfigLoad()
              pass
            elif (touch.read()[0])<215 and (touch.read()[0])>115:
              #print("2 but hold")
              vidro()
              screen0 = screen.get_act_screen()
              screen1=alarmExplorer(screen)
              screen.load_screen(screen0)
              screen.del_screen(screen1)
              alarms=getAlarms()
              pass
            elif (touch.read()[0])<105 and (touch.read()[0])>5:
              #print("1 but hold")
              vidro()
              screen0 = screen.get_act_screen()
              screen1=NotificationsScreen(screen)
              screen.load_screen(screen0)
              screen.del_screen(screen1)
              pass
  else:
    if touched_time>0 and touched_time!=-1:
      if touched_pos!=None:
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
          label2.set_pos(x=80, y=216)
    touched_time=0
  fix_update+=1
  wait(0.1)