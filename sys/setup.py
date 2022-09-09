from m5stack import *
from m5stack_ui import *
from uiflow import *
from easyIO import *
import os
import sys
import _thread
import wifiCfg
import json
import machine
sys.path.append("/flash/sys")
from helper import *

MAX_BR=100
ADAPTIVE_BR=True
MIN_BR=10
UTC_ZONE=3
ALARM_WAV='res/fallout.wav'
wavFreez = False
      
def ConfigLoad():
  global MAX_BR
  global ADAPTIVE_BR
  global MIN_BR
  global UTC_ZONE
  global ALARM_WAV
  data = {}
  if ('alarm.txt' in os.listdir('/flash')):
    with open('/flash/alarm.txt', 'r') as json_file:
      data = json.load(json_file)
  try:
    MAX_BR=data['setup']['MAX_BR']
    ADAPTIVE_BR=data['setup']['ADAPTIVE_BR']
    MIN_BR=data['setup']['MIN_BR']
    UTC_ZONE=data['setup']['UTC_ZONE']
    ALARM_WAV=data['setup']['ALARM_WAV']
  except Exception as e:
    M5Label(str(e), x=5, y=70, color=0xd80000, font=FONT_MONT_14)
  return MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV

def ConfigSave():
  data = {}
  if ('alarm.txt' in os.listdir('/flash')):
    with open('/flash/alarm.txt', 'r') as json_file:
      data = json.load(json_file)
  data['setup'] = {
                    'MAX_BR': MAX_BR,
                    'ADAPTIVE_BR': ADAPTIVE_BR,
                    'MIN_BR': MIN_BR,
                    'UTC_ZONE': UTC_ZONE,
                    'ALARM_WAV': ALARM_WAV
                    }
  with open('/flash/alarm.txt', 'w') as outfile:
    json.dump(data, outfile)

def ConfigScreen(screen):
  global ALARM_WAV
  screen0 = screen.get_new_screen()
  screen.load_screen(screen0)
  screen.set_screen_brightness(MAX_BR)
  ConfigLoad()
  
  obj=[[],[],[],[]]
  ind_tab=0
  tab = M5Tabview(0,0)
  tab.add_tab("Time")
  tab.add_tab("Screen")
  tab.add_tab("Audio")
  tab.add_tab("System")
  
  def getUTC():
    ans=""
    if UTC_ZONE>0:
      ans="UTC +{}".format(UTC_ZONE)
    else:
      ans="UTC {}".format(UTC_ZONE)
    while len(ans)<7:
      ans=" "+ans
    return ans

  def syncRTC():
    wait(0.5)
    obj[0][2].set_text("Try connect...")
    if not wifiCfg.wlan_sta.isconnected():
      wait(0.5)
      screen0 = screen.get_act_screen()
      wait(0.5)
      wifiCfg.autoConnect()
      wait(1)
      screen.load_screen(screen0)
    if wifiCfg.wlan_sta.isconnected():
      rtc.settime('ntp', host='cn.pool.ntp.org', tzone=UTC_ZONE)
      obj[0][2].set_text("New RTC time:\n"+str(rtc.printRTCtime()))
    else:
      obj[0][2].set_text("Error sync!\nTry later...")
  
  def clickSync():
    obj[0][0].set_hidden(True)
    vidro()
    _thread.start_new_thread(syncRTC,())
  
  def onUTCChange(value):
    global UTC_ZONE
    UTC_ZONE=value
    obj[0][-2].set_text(getUTC())
  
  def tab0Create():
    obj[0].append(M5Btn(text='Sync', x=210, y=80, w=80, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=screen0))
    obj[0][-1].pressed(clickSync)
    obj[0].append(M5Line(x1=5, y1=135, x2=315, y2=135, color=0xa0a0a0, width=1, parent=screen0))
    obj[0].append(M5Label('You can synchronize\n the RTC chip\n from an online server', x=20, y=75, color=0x000, font=FONT_MONT_14, parent=screen0))
    obj[0].append(M5Label('Choose your UTC time zone', x=20, y=150, color=0x000, font=FONT_MONT_14, parent=screen0))
    obj[0].append(M5Label(getUTC(), x=65, y=173, color=0x000, font=FONT_MONT_14, parent=screen0))
    obj[0].append(M5Slider(x=130, y=175, w=160, h=12, min=-12, max=14, bg_c=0xa0a0a0, color=0x08A2B0, parent=screen0))
    obj[0][-1].set_value(UTC_ZONE)
    obj[0][-1].changed(onUTCChange)
  
  def onMaxBrightnessChange(value):
    global MAX_BR
    obj[1][1].set_text(str(value))
    MAX_BR=value
  
  def onMinBrightnessChange(value):
    global MIN_BR
    obj[1][-2].set_text(str(value))
    MIN_BR=value
  
  def onAdaptibeBrChange():
    global ADAPTIVE_BR
    ADAPTIVE_BR=not ADAPTIVE_BR
    for ob in obj[1][5:]:
      ob.set_hidden(not ADAPTIVE_BR)
  
  def tab1Create():
    obj[1].append(M5Label('Set the maximum brightness:', x=20, y=70, color=0x000, font=FONT_MONT_14, parent=screen0))
    obj[1].append(M5Label(str(MAX_BR), x=100, y=92, color=0x000, font=FONT_MONT_14, parent=screen0))
    obj[1].append(M5Slider(x=130, y=95, w=160, h=12, min=60, max=100, bg_c=0xa0a0a0, color=0x08A2B0, parent=screen0))
    obj[1][-1].set_value(MAX_BR)
    obj[1][-1].changed(onMaxBrightnessChange)
    obj[1].append(M5Label('Adaptive mode:', x=20, y=130, color=0x000, font=FONT_MONT_14, parent=screen0))
    obj[1].append(M5Switch(160,125,))
    if ADAPTIVE_BR:
      obj[1][-1].set_on()
    obj[1][-1].on(onAdaptibeBrChange)
    obj[1][-1].off(onAdaptibeBrChange)
    obj[1].append(M5Label('Set the minimum brightness:', x=20, y=165, color=0x000, font=FONT_MONT_14, parent=screen0))
    if not ADAPTIVE_BR:
      obj[1][-1].set_hidden(True)
    obj[1].append(M5Label(str(MIN_BR), x=100, y=188, color=0x000, font=FONT_MONT_14, parent=screen0))
    if not ADAPTIVE_BR:
      obj[1][-1].set_hidden(True)
    obj[1].append(M5Slider(x=130, y=190, w=160, h=12, min=0, max=40, bg_c=0xa0a0a0, color=0x08A2B0, parent=screen0))
    if not ADAPTIVE_BR:
      obj[1][-1].set_hidden(True)
    obj[1][-1].set_value(MIN_BR)
    obj[1][-1].changed(onMinBrightnessChange)
  
  wavs=[]
  for filename in os.listdir('/flash/res'):
    if ".wav" in filename:
      wavs.append(filename)
  wavs_ind=-1
  for i,d in enumerate(wavs):
    if d in ALARM_WAV:
      wavs_ind=i
      break

  def playAlarm():
    global wavFreez
    wavFreez = True
    wait(0.1)
    obj[2][2].set_released_img("res/play_icon_press.png", 30, 30)
    wait(0.1)
    speaker.playWAV(ALARM_WAV)
    wait(0.1)
    obj[2][2].set_released_img("res/play_icon.png", 30, 30)
    wavFreez = False
  
  def playPress():
    global ALARM_WAV
    try:
      if wavFreez == False:
        wavs_ind = obj[2][1].get_sel_index()
        ALARM_WAV = "res/{}".format(wavs[wavs_ind])
        _thread.start_new_thread(playAlarm,())
    except Exception as e:
      M5Label(str(e), x=5, y=280, color=0xd80000, font=FONT_MONT_14)
    
  def tab2Create():
    obj[2].append(M5Label("Alarm clock melody:", x=20, y=70, color=0x000, font=FONT_MONT_14, parent=screen0))
    obj[2].append(M5Dropdown(x=30, y=90, w=230, h=30, parent=screen0))
    obj[2][-1].set_options(wavs)
    obj[2][-1].set_sel_index(wavs_ind)
    obj[2].append(M5Imgbtn("res/play_icon.png",x=270,y=90,w=30,h=30,parent=screen0))
    obj[2][-1].pressed(playPress)
  
  def debugModePress():
    M5Screen().clean_screen()
    M5Screen().set_screen_bg_color(0x000000)
    M5Label('Restart...', x=117, y=111, color=0xffffff, font=FONT_MONT_18, parent=None)
    vidro()
    machine.reset()
      
  def tab3Create():
    obj[3].append(M5Btn(text='Restart device', x=20, y=80, w=280, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=screen0))
    obj[3][-1].pressed(debugModePress)

  def tabHide():
    for i in range(0,len(obj[ind_tab])):
      obj[ind_tab][-(1+i)].set_hidden(True)
  
  def tabShow():
    for i in range(0,len(obj[ind_tab])):
      if ind_tab!=1 or i<5:
        obj[ind_tab][i].set_hidden(False)
      elif ADAPTIVE_BR:
        obj[ind_tab][i].set_hidden(False)

  tab0Create()
  M5Label("save", x=140, y=224, color=0xd84949, font=FONT_MONT_14, parent=screen0)
  M5Label("close", x=238, y=224, color=0xd84949, font=FONT_MONT_14, parent=screen0)
  MAX_BR_old=MAX_BR
  run=True
  touched_time = 0
  touched_cord = None
  vidro()
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
                if len(obj[2])>1:
                  wavs_ind = obj[2][1].get_sel_index()
                ALARM_WAV="res/{}".format(wavs[wavs_ind])
                ConfigSave()
                run=False
    else:
      if (touched_time>0):
        if (touch.read()[1]) < 57:
          tabHide()
          vidro()
          ind=int(touch.read()[0]/(320/4))
          if len(obj[ind])==0:
            if ind==1: tab1Create()
            elif ind==2: tab2Create()
            elif ind==3: tab3Create()
          ind_tab=ind
          tabShow()
        elif MAX_BR_old!=MAX_BR:
          MAX_BR_old=MAX_BR
          screen.set_screen_brightness(MAX_BR)
      touched_time=0
  ConfigLoad()
  vidro()
  screen0 = screen.get_act_screen()
  return screen0

# screen = M5Screen()
# screen.clean_screen()
# ConfigScreen(screen)