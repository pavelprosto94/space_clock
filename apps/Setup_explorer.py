from m5stack import lv, rtc, speaker, power, touch
rootLoading = lv.obj()
label = lv.label(rootLoading)
label.set_text('Loading...')
label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
lv.disp_load_scr(rootLoading)
from uiflow import wait
wait(0.01)
if not 'body_font' in dir(): body_font=lv.font_montserrat_14
if not 'title_font' in dir(): title_font=lv.font_montserrat_18
import os, sys, _thread, wifiCfg, json, machine, time, deviceCfg
sys.path.append("/flash/sys")
from helper import vibrating, distance, ConfigLoad, fileExist
from slidertime import SliderTime

def ConfigSave():
  data = {}
  if fileExist('/flash/setup.txt'):
    with open('/flash/setup.txt', 'r') as json_file:
      data = json.load(json_file)
  data['setup'] = { 'MAX_BR': MAX_BR,
                    'ADAPTIVE_BR': ADAPTIVE_BR,
                    'MIN_BR': MIN_BR,
                    'UTC_ZONE': UTC_ZONE,
                    'ALARM_WAV': ALARM_WAV,
                    'NOTIFY_WAV': NOTIFY_WAV,
                    'NOTIFY_PERIODIC': NOTIFY_PERIODIC,}
  with open('/flash/setup.txt', 'w') as outfile:
    json.dump(data, outfile)

def getUTC():
    ans=""
    if UTC_ZONE>0: ans="UTC +{}".format(UTC_ZONE)
    else: ans="UTC {}".format(UTC_ZONE)
    while len(ans)<7: ans=" "+ans
    return ans

def loadPNG(path):
  with open(path,'rb') as f: data = f.read()
  img_dsc = lv.img_dsc_t({'data_size': len(data),'data': data })
  return img_dsc

def showTime():
  global subscreen
  def event_slider_handler(source,evt):
    global UTC_ZONE
    if evt == lv.EVENT.VALUE_CHANGED:
      UTC_ZONE=slider.get_value()
      slider_label.set_text(getUTC())
  def syncRTC():
    btn1.set_hidden(True)
    vibrating()
    wait(0.5)
    label_RTC.set_text("Try connect...")
    wait(0.1)
    if not wifiCfg.wlan_sta.isconnected():
      wait(0.5)
      wifiCfg.autoConnect()
      wait(1)
      lv.disp_load_scr(subscreen)
    if wifiCfg.wlan_sta.isconnected():
      rtc.settime('ntp', host='cn.pool.ntp.org', tzone=UTC_ZONE)
      label_RTC.set_text("New RTC time:\n"+str(rtc.printRTCtime()))
    else:
      label_RTC.set_text("Error sync!\nTry later...")
    btn1.set_hidden(False)
  def event_RTC_handler(obj, event):
    if event == lv.EVENT.CLICKED:
      _thread.start_new_thread(syncRTC,())
  vibrating()
  subscreen = lv.obj()
  subscreen.set_style_local_text_font(0,0,body_font)
  page,label_cl, = lv.obj(subscreen),lv.label(subscreen)
  page.set_size(320,215)
  page.set_click(False)
  label_cl.set_pos(238,220)
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close") 
  btn1 = lv.btn(page,None)
  btn1.set_event_cb(event_RTC_handler)
  btn1.set_pos(180, 18)
  label=lv.label(btn1,None)
  label.set_text(lv.SYMBOL.LOOP+' Sync')
  label_RTC=lv.label(page,None)
  label_RTC.set_text('You can synchronize\n the RTC chip\n from an online server')
  label_RTC.set_pos(10, 15)
  line1 = lv.line(page)
  line1.set_points([{"x":5, "y":80},{"x":315, "y":80}], 2)
  line1.add_style(lv.line.PART.MAIN, style_line)
  label=lv.label(page,None)
  label.set_text('Choose your UTC time zone')
  label.set_pos(10, 100)
  slider_label=lv.label(page,None)
  slider_label.set_text(getUTC())
  slider_label.set_pos(64, 123)
  slider = lv.slider(page,None)
  slider.set_width(160)
  slider.set_pos(130,125)
  slider.set_event_cb(event_slider_handler)
  slider.set_range(-12, 14)
  slider.set_value(UTC_ZONE,lv.ANIM.OFF)
  lv.disp_load_scr(subscreen)

def showScreen():
  global subscreen
  def event_slider_handler(obj,evt):
    global MAX_BR
    global MIN_BR
    global ADAPTIVE_BR
    if evt == lv.EVENT.VALUE_CHANGED:
      if obj==slider:
        MAX_BR=slider.get_value()
        label_BR.set_text(str(MAX_BR))
      elif obj==sw1:
        ADAPTIVE_BR=obj.get_state()
        showBR()
      elif obj==slider2:
        MIN_BR=slider2.get_value()
        label_MIN_BR.set_text(str(MIN_BR))
  def showBR():
    if ADAPTIVE_BR:
      label2.set_hidden(False)
      label_MIN_BR.set_hidden(False)
      slider2.set_hidden(False)
    else:
      label2.set_hidden(True)
      label_MIN_BR.set_hidden(True)
      slider2.set_hidden(True)
  vibrating()
  subscreen = lv.obj()
  subscreen.set_style_local_text_font(0,0,body_font)
  page, label_cl = lv.obj(subscreen), lv.label(subscreen)
  page.set_size(320,215)
  page.set_click(False)
  label_cl.set_pos(238,220)
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label=lv.label(page,None)
  label.set_text('Set the maximum brightness:')
  label.set_pos(10, 20)
  label_BR,label,label2=lv.label(page,None),lv.label(page,None),lv.label(page,None)
  label_BR.set_text(str(MAX_BR))
  label_BR.set_pos(100, 42)
  slider,slider2 = lv.slider(page,None), lv.slider(page,None)
  slider.set_width(160)
  slider.set_pos(130,45)
  slider.set_event_cb(event_slider_handler)
  slider.set_range(60, 100)
  slider.set_value(MAX_BR,lv.ANIM.OFF)
  label.set_text('Adaptive mode:')
  label.set_pos(10, 80)
  sw1 = lv.switch(page, None)
  sw1.set_pos(160, 75)
  sw1.set_event_cb(event_slider_handler)
  if ADAPTIVE_BR:
    sw1.on(lv.ANIM.OFF)
  label2.set_text('Set the minimum brightness:')
  label2.set_pos(10, 120)
  label_MIN_BR=lv.label(page,None)
  label_MIN_BR.set_text(str(MIN_BR))
  label_MIN_BR.set_pos(100, 142)
  slider2.set_width(160)
  slider2.set_pos(130,145)
  slider2.set_event_cb(event_slider_handler)
  slider2.set_range(0, 40)
  slider2.set_value(MIN_BR,lv.ANIM.OFF)
  showBR()
  lv.disp_load_scr(subscreen)

def showAudio():
  global subscreen
  def playAlarm():
    global wavFreez
    wavFreez = True
    imgbtn1.set_src(lv.btn.STATE.RELEASED, loadPNG("res/play_icon_press.png"))
    wait(0.1)
    if ALARM_WAV!="None": speaker.playWAV(ALARM_WAV)
    wait(0.1)
    imgbtn1.set_src(lv.btn.STATE.RELEASED, loadPNG("res/play_icon.png"))
    wavFreez = False
  def event_handler(obj, event):
    global NOTIFY_PERIODIC
    if event == lv.EVENT.CLICKED:
      if wavFreez == False:  
        if imgbtn1==obj:
          _thread.start_new_thread(playAlarm,())
  def event_list_handler(obj, event):
    global ALARM_WAV
    global NOTIFY_WAV
    if event == lv.EVENT.VALUE_CHANGED:
      if wavFreez == False:  
        if ddlist==obj:
          ALARM_WAV = "res/{}".format(wavs[obj.get_selected()])
          _thread.start_new_thread(playAlarm,())
  vibrating()
  subscreen = lv.obj()
  subscreen.set_style_local_text_font(0,0,body_font)
  page, label_cl = lv.obj(subscreen), lv.label(subscreen)
  page.set_size(320,215)
  page.set_click(False)
  label_cl.set_pos(238,220)
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label=lv.label(page,None)
  label.set_text("Alarm clock melody:")
  label.set_pos(10, 20)
  wavs=[]
  for filename in os.listdir('/flash/res'):
    if ".wav" in filename:
      wavs.append(filename)
  wavs_ind=-1
  for i,d in enumerate(wavs):
    if d in ALARM_WAV:
      wavs_ind=i
      break
  ddlist,imgbtn1 = lv.dropdown(page),lv.imgbtn(page, None) 
  ddlist.set_options("\n".join(wavs))
  ddlist.set_pos(30,45)
  ddlist.set_size(210,30)
  ddlist.set_selected(wavs_ind)
  ddlist.set_event_cb(event_list_handler)
  imgbtn1.set_src(lv.btn.STATE.RELEASED, loadPNG("res/play_icon.png"))
  imgbtn1.set_checkable(True)
  imgbtn1.set_pos(255, 45)
  imgbtn1.set_event_cb(event_handler)
  lv.disp_load_scr(subscreen)
  
def showNotify():
  global subscreen
  def playAlarm2():
    global wavFreez
    wavFreez = True
    imgbtn2.set_src(lv.btn.STATE.RELEASED, loadPNG("res/play_icon_press.png"))
    wait(0.1)
    if NOTIFY_WAV!="None": speaker.playWAV(NOTIFY_WAV)
    wait(0.1)
    imgbtn2.set_src(lv.btn.STATE.RELEASED, loadPNG("res/play_icon.png"))
    wavFreez = False
  def event_handler(obj, event):
    global NOTIFY_PERIODIC
    if event == lv.EVENT.CLICKED:
      if wavFreez == False:  
        if imgbtn2==obj:
          _thread.start_new_thread(playAlarm2,())
        elif obj==sw1:
          if obj.get_state():
            NOTIFY_PERIODIC=[slt1.value,slt2.value]
            slt1.set_hidden(False)
            slt2.set_hidden(False)
            label_slt1.set_hidden(False)
            label_slt2.set_hidden(False)
          else:
            NOTIFY_PERIODIC=[-1,-1]
            slt1.set_hidden(True)
            slt2.set_hidden(True)
            label_slt1.set_hidden(True)
            label_slt2.set_hidden(True)
  def event_list_handler(obj, event):
    global NOTIFY_WAV
    if event == lv.EVENT.VALUE_CHANGED:
      if wavFreez == False:  
        if ddlist2==obj:
          NOTIFY_WAV = "res/{}".format(wavs[obj.get_selected()])
          _thread.start_new_thread(playAlarm2,())
  vibrating()
  subscreen = lv.obj()
  subscreen.set_style_local_text_font(0,0,body_font)
  page, label_cl = lv.obj(subscreen), lv.label(subscreen)
  page.set_size(320,215)
  page.set_click(False)
  label_cl.set_pos(238,220)
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label,ddlist2,imgbtn2=lv.label(page,None),lv.dropdown(page),lv.imgbtn(page, None)
  label.set_text("Notification melody:")
  label.set_pos(10, 10)
  wavs=["None"]
  for filename in os.listdir('/flash/res'):
    if ".wav" in filename:
      wavs.append(filename)
  wavs_ind=-1
  for i,d in enumerate(wavs):
    if d in NOTIFY_WAV:
      wavs_ind=i
      break
  ddlist2.set_options("\n".join(wavs))
  ddlist2.set_pos(30,35)
  ddlist2.set_size(210,30)
  ddlist2.set_selected(wavs_ind)
  ddlist2.set_event_cb(event_list_handler)
  imgbtn2.set_src(lv.btn.STATE.RELEASED, loadPNG("res/play_icon.png"))
  imgbtn2.set_checkable(True)
  imgbtn2.set_pos(255, 35)
  imgbtn2.set_event_cb(event_handler)
  sw1,label,label_slt1,label_slt2=lv.switch(page, None),lv.label(page,None),lv.label(page,None),lv.label(page,None)
  label.set_text('Do not disturb mode:')
  label.set_pos(10, 70)
  sw1.set_pos(240, 70)
  sw1.set_event_cb(event_handler)
  label_slt1.set_text("Notify disable start:")
  label_slt1.set_pos(10, 98)
  label_slt2.set_text("Notify disable end:")
  label_slt2.set_pos(10, 159)
  if NOTIFY_PERIODIC[0]!=-1 and NOTIFY_PERIODIC[1]!=-1:
    slt1=SliderTime(page,0,114,NOTIFY_PERIODIC[0],23,title_font,body_font)
    slt2=SliderTime(page,0,176,NOTIFY_PERIODIC[1],23,title_font,body_font)
    sw1.on(lv.ANIM.OFF)
  else:
    slt1=SliderTime(page,0,114,0,23,title_font,body_font)
    slt2=SliderTime(page,0,176,8,23,title_font,body_font)
    slt1.set_hidden(True)
    slt2.set_hidden(True)
    label_slt1.set_hidden(True)
    label_slt2.set_hidden(True)
  lv.disp_load_scr(subscreen)

def showWiFi():
  vibrating()
  lv.disp_load_scr(rootLoading)
  wait(0.01)
  try:
    exec(open('/flash/apps/WiFi.py', 'r').read(),{'__file__':'Apps', 'body_font':body_font, 'title_font':title_font})
  except Exception as e:
    label.set_text(str(e))
    label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
    lv.disp_load_scr(rootLoading)
    wait(2)
  label.set_text('Loading...')
  lv.disp_load_scr(root)

def showSystem():
  global subscreen
  def cl_reboot():
    label.set_text('Restart...')
    label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
    lv.disp_load_scr(rootLoading)
    wait(5)
    machine.reset()
  def cl_about():
    from about import AboutScreen
    AboutScreen()
    lv.disp_load_scr(subscreen)
  def cl_debug():
    exec(open('/flash/apps/Debug.py', 'r').read(),{})
  def event_handler(obj,evt):
    if evt == lv.EVENT.CLICKED:
      l=obj.get_child(None).get_text()
      if l==lv.SYMBOL.REFRESH+' Restart device':
        _thread.start_new_thread(cl_reboot,()) 
      elif l==lv.SYMBOL.BELL+' About':
        _thread.start_new_thread(cl_about,()) 
      elif l==lv.SYMBOL.WARNING+' Debug mode':
        _thread.start_new_thread(cl_debug,()) 
  def event_slider_handler(obj,evt):
    if evt == lv.EVENT.VALUE_CHANGED:
      if obj==sw1:
        deviceCfg.set_startup_beep(obj.get_state())
      elif obj==sw2:
        deviceCfg.set_power_led(obj.get_state())
        #_thread.start_new_thread(setLed,()) 
  vibrating()
  subscreen = lv.obj()
  subscreen.set_style_local_text_font(0,0,body_font)
  page, label_cl = lv.obj(subscreen), lv.label(subscreen)
  page.set_size(320,215)
  page.set_click(False)
  label_cl.set_pos(238,220)
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  btn1 = lv.btn(page,None)
  btn1.set_event_cb(event_handler)
  btn1.set_pos(20, 15)
  btn1.set_size(280,35)
  label=lv.label(btn1,None)
  label.set_text(lv.SYMBOL.REFRESH+' Restart device')
  btn1 = lv.btn(page,None)
  btn1.set_event_cb(event_handler)
  btn1.set_pos(20, 55)
  btn1.set_size(280,35)
  label=lv.label(btn1,None)
  label.set_text(lv.SYMBOL.BELL+' About') 
  btn1 = lv.btn(page,None)
  btn1.set_event_cb(event_handler)
  btn1.set_pos(20, 95)
  btn1.set_size(280,35)
  label=lv.label(btn1,None)
  label.set_text(lv.SYMBOL.WARNING+' Debug mode') 
  label=lv.label(page,None)
  label.set_text('Enable the startup ringtone:')
  label.set_pos(10, 145)
  sw1 = lv.switch(page, None)
  sw1.set_pos(250, 140)
  sw1.set_event_cb(event_slider_handler)
  if deviceCfg.get_startup_beep():
    sw1.on(lv.ANIM.OFF)
  label=lv.label(page,None)
  label.set_text('Bluetooth LED indicator:')
  label.set_pos(10, 180)
  sw2 = lv.switch(page, None)
  sw2.set_pos(250, 175)
  sw2.set_event_cb(event_slider_handler)
  if deviceCfg.get_power_led_mode():
    sw2.on(lv.ANIM.OFF)
  lv.disp_load_scr(subscreen)

def event_handler(obj, event):
  if event == lv.EVENT.CLICKED:
    list_btn = lv.list.__cast__(obj)
    if list_btn.get_btn_text()=="Time":
      _thread.start_new_thread(showTime,())
    elif list_btn.get_btn_text()=="Screen":
      _thread.start_new_thread(showScreen,())
    elif list_btn.get_btn_text()=="Audio":
      _thread.start_new_thread(showAudio,())
    elif list_btn.get_btn_text()=="Notification":
      _thread.start_new_thread(showNotify,())
    elif list_btn.get_btn_text()=="WiFi":
      _thread.start_new_thread(showWiFi,())
    elif list_btn.get_btn_text()=="System":
      _thread.start_new_thread(showSystem,())

subscreen=None
MAX_BR, ADAPTIVE_BR, MIN_BR, UTC_ZONE, ALARM_WAV, NOTIFY_WAV, NOTIFY_PERIODIC=ConfigLoad()
wavFreez = False
showEnbl = False
root = lv.obj()
root.set_style_local_text_font(0,0,body_font)
label_shadow_style, style_line = lv.style_t(), lv.style_t()
label_shadow_style.init()
label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
style_line.init()
style_line.set_line_width(lv.STATE.DEFAULT, 1)
style_line.set_line_color(lv.STATE.DEFAULT, lv.color_hex(0xa0a0a0))
style_line.set_line_rounded(lv.STATE.DEFAULT, True)
label_cl, label_sub, list1 = lv.label(root), lv.label(root), lv.list(root)
label_cl.set_pos(238,220)
label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
label_cl.set_text(lv.SYMBOL.CLOSE+" close")
label_sub.set_pos(130,220)
label_sub.add_style(lv.label.PART.MAIN, label_shadow_style)
label_sub.set_text(lv.SYMBOL.SAVE+" save")
list1.set_size(320, 215)
list1.set_style_local_text_font(0,0,title_font)
tabs = [[lv.SYMBOL.BELL, "Time"],
        [lv.SYMBOL.CHARGE, "Screen"],
        [lv.SYMBOL.AUDIO, "Audio"],
        [lv.SYMBOL.AUDIO, "Notification"],
        [lv.SYMBOL.WIFI, "WiFi"],
        [lv.SYMBOL.SETTINGS, "System"],]
for i in range(0,6):
  list_btn = list1.add_btn(tabs[i][0],tabs[i][1])
  list_btn.set_event_cb(event_handler)
lv.disp_load_scr(root)

run,touched_time,touched_cord,MAX_BR_old=True,0,None,MAX_BR
vibrating()
while run:
  if touch.status():
    if touched_time==0:
      touched_time=time.ticks_ms()
      touched_cord = touch.read()
    elif touched_time!=-1:
      if time.ticks_ms()-touched_time>250:
        if distance(touched_cord,touch.read())<3:
          touched_time=-1
          if (touch.read()[1]) > 240:
            if (touch.read()[0])<315 and (touch.read()[0])>225:
              if subscreen!=None:
                vibrating()
                lv.disp_load_scr(root)
                subscreen.delete()
                subscreen=None
              elif lv.scr_act()==root:
                run=False
            elif (touch.read()[0])<215 and (touch.read()[0])>115:
              if lv.scr_act()==root:
                label.set_text('Saving...')
                lv.disp_load_scr(rootLoading)
                wait(1)
                ConfigSave()
                run=False
  else:
    if touched_time!=0:
      if MAX_BR_old!=MAX_BR:
        MAX_BR_old=MAX_BR
        power.setLCDBrightness(MAX_BR)
      touched_time=0
vibrating()
label.set_text('')
lv.disp_load_scr(rootLoading)