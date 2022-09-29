try:
  if str(__file__) == "menu/app.py":
    import machine
    fileA = open('/flash/apps/Notifications_explorer.py', 'rb')
    fileB = open('/flash/main.py', 'wb')
    fileB.write(fileA.read())
    fileA.close()
    fileB.close()
    machine.reset()
except Exception as e:
  print("run Notifications apps")
import lvgl as lv
from uiflow import wait
from m5stack import touch
import os, sys, time, wifiCfg, _thread
sys.path.append("/flash/sys")
from helper import vibrating, distance
from weather import GetWeather, getCity
from notifications import readNotifications, seenNotifications

def openPNG(path):
  with open(path,'rb') as f: data = f.read()
  return lv.img_dsc_t({'data_size': len(data),'data': data })

def loadWeather(img_w,label_c):
  label_c.set_text(" ...")
  wait(0.01)
  if not wifiCfg.wlan_sta.isconnected():
    wifiCfg.autoConnect(lcdShow=False)
  if wifiCfg.wlan_sta.isconnected():
    label_c.set_text(" .:.")
    w_data=GetWeather(getCity())
    try:
      label_c.set_text(w_data[2])
      img_w.set_src(openPNG(w_data[3]))
    except Exception as e: 
      pass

def event_handler(obj, event):
  if event == lv.EVENT.LONG_PRESSED:
    pass
    # l=obj.get_child(None)
    # otv=l.get_text()
    # if lv.SYMBOL.CLOSE+" close" == otv:
    #   vibrating()

def showNotifications(list_f,label_sub):
  try:
    list_f.clean()
  except Exception as e: 
    pass
  notification=readNotifications()
  try:
    for d in notification['tree'][::-1]:
      l="{}: {}".format(d['from'],d['body'])
      if len(l)>128:
        l=l[:128]
      btn_new=list_f.add_btn(lv.SYMBOL.BELL,l)
      #btn_new.set_event_cb(event_handler)
    if len(notification['tree'])>0:
      label_sub.set_hidden(False)
    else:
      label_sub.set_hidden(True)
      btn_new=list_f.add_btn(lv.SYMBOL.BELL,"No notifications")
  except Exception as e:
    print("ERROR notifications"+str(e))

def notificationsExplorer(body_font=lv.font_montserrat_14,title_font=lv.font_montserrat_18):
  subscreen=None
  root = lv.obj()
  root.set_style_local_text_font(0,0,body_font)
  label_shadow_style = lv.style_t()
  label_shadow_style.init()
  label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
  label_cl = lv.label(root)
  label_cl.set_pos(238,220)
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label_sub = lv.label(root)
  label_sub.set_pos(130,220)
  label_sub.set_hidden(True)
  label_sub.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_sub.set_text(lv.SYMBOL.TRASH+" clear")
  page = lv.obj(root)
  page.set_pos(220,0)
  page.set_style_local_text_color(0,0,lv.color_hex(0xa0a0a0))
  page.set_style_local_bg_color(0,0,lv.color_hex(0x48484a))
  page.set_size(100,50)
  label_c = lv.label(page)
  label_c.set_pos(42,14)
  label_c.set_style_local_text_font(0,0,title_font)
  label_c.set_text(" ..")
  img_w = lv.img(page)
  img_w.set_src(openPNG("/flash/res/weather/error.png"))
  label_h = lv.label(root)
  label_h.set_pos(14,10)
  label_h.set_style_local_text_font(0,0,title_font)
  label_h.set_style_local_text_color(0,0,lv.color_hex(0x226577))
  label_h.set_text(lv.SYMBOL.BELL+"Notifications")
  list_f = lv.list(root)
  list_f.set_size(320, 165)
  list_f.set_style_local_text_font(0,0,body_font)
  list_f.set_pos(0,50)
  lv.disp_load_scr(root)
  showNotifications(list_f,label_sub)
  vibrating()
  _thread.start_new_thread(loadWeather,(img_w,label_c))
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
                  if subscreen!=None:
                    lv.disp_load_scr(root)
                    subscreen.delete()
                    subscreen=None
                  else:
                    vibrating()
                    list_f.set_hidden(True)
                    label_cl.set_hidden(True)
                    label_sub.set_hidden(True)
                    seenNotifications()
                    run=False
              elif (touch.read()[0])<215 and (touch.read()[0])>115:
                if subscreen==None and label_sub.is_visible():
                  vibrating()
                  run=False
    else:
      touched_time=0
    wait(0.2)
  vibrating()
  return root

try:
  if str(__file__) == "flow/m5ucloud.py":
    rootLoading = lv.obj()
    label = lv.label(rootLoading)
    label.set_text('Loading...')
    label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
    lv.disp_load_scr(rootLoading)
    wait(0.01)
    notificationsExplorer()
    label.set_text("")
    label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
    lv.disp_load_scr(rootLoading)
except Exception as e:
  pass