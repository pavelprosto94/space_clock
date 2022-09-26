try:
  if str(__file__) == "menu/app.py":
    import machine
    fileA = open('/flash/apps/WiFi.py', 'rb')
    fileB = open('/flash/main.py', 'wb')
    fileB.write(fileA.read())
    fileA.close()
    fileB.close()
    machine.reset()
except Exception as e:
  print("run WiFi manager")
import lvgl as lv      
rootLoading = lv.obj()
label = lv.label(rootLoading)
label.align(rootLoading,lv.ALIGN.CENTER, -20, 0)
label.set_text('Loading...')
lv.disp_load_scr(rootLoading)
from uiflow import wait
wait(0.01)
from m5stack import touch
import os, sys, time, wifiCfg, _thread, json
sys.path.append("/flash/sys")
from helper import vibrating, distance, fileExist

def getWiFiinfo():
  ans="\n"
  d=wifiCfg.wlan_sta.ifconfig()
  ans+="ip: {}\n".format(d[0])
  ans+="mask: {}\n".format(d[1])
  ans+="mac: {:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}\n".format(*wifiCfg.wlan_sta.config('mac'))
  ans+="DNS: {}\n".format(d[2])
  return ans

def showStat():
  if not wifiCfg.wlan_sta.isconnected():
    label_st.set_text("{} WiFi not connected".format(lv.SYMBOL.WIFI))
    btn1.set_hidden(False)
  else:
    label_st.set_text("{} Connected to {}\n{}".format(lv.SYMBOL.WIFI, str(wifiCfg._connect_ssid),getWiFiinfo()))
    btn1.set_hidden(True)
    
def autoConnect():
  wait(0.1)
  wifiCfg.autoConnect()
  wait(0.5)
  btn1_label.set_text(" Try autoConnect ")
  lv.disp_load_scr(root)
  showStat()
    
def doConnect():
  list_f.set_hidden(True)
  label_sub.set_hidden(True)
  label_cl.set_hidden(True)
  label_st.set_text("{} Connecting to {}".format(lv.SYMBOL.WIFI, SSID))
  preload.set_hidden(False)
  wait(0.1)
  wifiCfg.connect(SSID,PASS,5000,block=True)
  lv.disp_load_scr(root)
  preload.set_hidden(True)
  label_sub.set_hidden(False)
  label_cl.set_hidden(False)
  if not wifiCfg.wlan_sta.isconnected():
    label_st.set_text("{} ERROR connect to {}".format(lv.SYMBOL.WIFI, SSID))  
    list_f.set_hidden(False)
  else:
    showStat()

def event_keybHandler(obj, event):
  global subscreen
  global PASS
  obj.def_event_cb(event)
  if event == lv.EVENT.CANCEL:
    lv.disp_load_scr(root)
    subscreen.delete()
    subscreen=None
  elif event == lv.EVENT.APPLY:
    lv.disp_load_scr(root)
    PASS=str(obj.get_textarea().get_text())
    subscreen.delete()
    subscreen=None
    _thread.start_new_thread(doConnect,())

btn2_label=None    
def event_handler_hiden(obj,evt):
  if evt == lv.EVENT.CLICKED:
    if obj.get_pwd_mode():
      obj.set_pwd_mode(False)
      btn2_label.set_text(lv.SYMBOL.EYE_OPEN)
    else:
      obj.set_pwd_mode(True)
      btn2_label.set_text(lv.SYMBOL.EYE_CLOSE)

def showKeyb():
  global subscreen
  global btn2_label
  subscreen=lv.obj()
  lbl = lv.label(subscreen)
  lbl.set_pos(10,5)
  lbl.set_text("Enter password from {}:".format(SSID))
  ta=lv.textarea(subscreen,None)
  ta.set_accepted_chars("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@$%^&*()~`_-=[]}{\\|;':\"<>?,./")
  ta.set_size(300,35)
  ta.set_pos(10,22)
  ta.set_text("")
  ta.set_pwd_mode(True)
  ta.set_event_cb(event_handler_hiden)
  btn2_label=lv.label(ta,None)
  btn2_label.set_text(lv.SYMBOL.EYE_CLOSE)
  btn2_label.align(ta,lv.ALIGN.IN_RIGHT_MID,-10,0)  
  keyb = lv.keyboard(subscreen,None)
  keyb.set_cursor_manage(True)
  keyb.set_event_cb(event_keybHandler)
  keyb.set_textarea(ta)
  keyb.set_pos(0,70)
  keyb.set_size(320,170)
  lv.disp_load_scr(subscreen)
  
def event_handler(obj,evt):
  global SSID
  if evt == lv.EVENT.CLICKED:
    if obj == btn1:
      btn1_label.set_text("Connect...")
      _thread.start_new_thread(autoConnect,())
    elif obj == sw1:
      pass
    else:
      list_btn = lv.list.__cast__(obj)
      SSID=list_btn.get_btn_text()
      showKeyb()
      
def scanWiFi():
  btn1.set_hidden(True)
  list_f.set_hidden(False)
  label_st.set_text("{} Scaning...".format(lv.SYMBOL.WIFI))
  wifiCfg.wlan_sta.active(True)
  otv=wifiCfg.wlan_sta.scan()
  label_st.set_text("{} Choose Wi-Fi to connect:".format(lv.SYMBOL.WIFI))
  vibrating()
  try:
    list_f.clean()
  except Exception as e: 
    pass
  for l in otv:
    btn_new=list_f.add_btn(lv.SYMBOL.WIFI,bytes.decode(l[0]))
    btn_new.set_event_cb(event_handler)
def change_boot():
  dat1="""from machine import SDCard
from machine import Pin 
import os
try:
  sd = SDCard(slot=3, miso=Pin(38), mosi=Pin(23), sck=Pin(18), cs=Pin(4))
  sd.info()
  os.mount(sd, '/sd')
  print(\"SD card mounted at \\\"/sd\\\"\")
except (KeyboardInterrupt, Exception) as e:
  # print('SD mount caught exception {} {}'.format(type(e).__name__, e))
  pass"""
  if sw1.get_state():
    dat1="""from machine import SDCard
from machine import Pin 
import os, wifiCfg
try:
  sd = SDCard(slot=3, miso=Pin(38), mosi=Pin(23), sck=Pin(18), cs=Pin(4))
  sd.info()
  os.mount(sd, '/sd')
  print(\"SD card mounted at \\\"/sd\\\"\")
except (KeyboardInterrupt, Exception) as e:
  # print('SD mount caught exception {} {}'.format(type(e).__name__, e))
  pass
    
wifiCfg.autoConnect(lcdShow=False)"""
  with open('/flash/boot.py', 'wb') as fileB:
    fileB.write(dat1)
    
def saveWifi():
  data = {}
  try:
    if fileExist('/flash/wpa_supplicant.conf'):
        with open('/flash/wpa_supplicant.conf', 'r') as json_file:
          data = json.load(json_file)
  except Exception as e: 
    label_st.set_text(str(e))
  try:
    data['autoconnect'] = sw1.get_state()
    data['network'] = {
                        'ssid': SSID,
                        'psk': PASS
                        }
    with open('/flash/wpa_supplicant.conf', 'w') as outfile:
      json.dump(data, outfile)
  except Exception as e: 
    label.set_text(str(e))
  if AUTOCONNECT!=sw1.get_state(): change_boot()
    
def loadWifi():
  global AUTOCONNECT
  global SSID
  global PASS
  data = {}
  if fileExist('/flash/wpa_supplicant.conf'):
    try:
      with open('/flash/wpa_supplicant.conf', 'r') as json_file:
        data = json.load(json_file)
      AUTOCONNECT=data['autoconnect']
      SSID=data['network']['ssid']
      PASS=data['network']['psk']
    except Exception as e: 
      pass
SSID=""
PASS="" 
AUTOCONNECT=False 
loadWifi()
subscreen=None
root = lv.obj()
sw1=lv.switch(root)
if AUTOCONNECT:
  sw1.on(lv.ANIM.OFF)
sw1.set_event_cb(event_handler)
sw1.set_pos(240,160)
label_sw1 = lv.label(root)
label_sw1.set_pos(5,165)
label_sw1.set_size(230,14)
label_sw1.set_text("autoConnect on boot")
label_sw1.set_style_local_text_color(0,0,lv.color_hex(0x446f73))
label_sw1.align(sw1,lv.ALIGN.IN_BOTTOM_RIGHT,-55,-5)
label_shadow_style = lv.style_t()
label_shadow_style.init()
label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
label_cl = lv.label(root)
label_cl.set_pos(238,220)
label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
label_cl.set_text(lv.SYMBOL.CLOSE+" close")
label_sub = lv.label(root)
label_sub.set_pos(128,220)
label_sub.add_style(lv.label.PART.MAIN, label_shadow_style)
label_sub.set_text(lv.SYMBOL.REFRESH+" scan")
label_st = lv.label(root)
label_st.set_style_local_text_font(0,0,lv.font_montserrat_18)
label_st.set_pos(5,5)
label_st.set_text("init...")
list_f = lv.list(root)
list_f.set_size(320, 180)
list_f.set_pos(0,35)
list_f.set_hidden(True)
btn1 = lv.btn(root,None)
btn1.set_event_cb(event_handler)
btn1_label=lv.label(btn1,None)
btn1_label.set_text(" Try autoConnect ")
btn1.align(None,lv.ALIGN.CENTER,0,0)
btn1.set_hidden(True)
preload = lv.spinner(root, None)
preload.set_size(100, 100)
preload.align(None, lv.ALIGN.CENTER, 0, 0)
preload.set_hidden(True)
lv.disp_load_scr(root)
showStat()
vibrating()
run=True
touched_time = 0
touched_cord = None
while run:
  if touch.status():
    if (touch.read()[1]) > 230:
      if touched_time==0:
        touched_time=time.ticks_ms()
        touched_cord = touch.read()
      elif touched_time!=-1:
        if time.ticks_ms()-touched_time>500:
          if distance(touched_cord,touch.read())<3:
            touched_time=-1
            if (touch.read()[0])<315 and (touch.read()[0])>225:
              if label_cl.is_visible():
                vibrating()
                if subscreen!=None:
                  lv.disp_load_scr(root)
                  subscreen.delete()
                  subscreen=None
                elif list_f.is_visible():
                  list_f.set_hidden(True)
                  showStat()
                else:
                  saveWifi()
                  run=False
            elif (touch.read()[0])<215 and (touch.read()[0])>115:
              if subscreen==None and label_sub.is_visible():
                vibrating()
                scanWiFi()
  else:
    touched_time=0
  wait(0.2)
label.set_text('')
lv.disp_load_scr(rootLoading)