from m5stack import touch,lv
from uiflow import wait
import sys, time, wifiCfg, _thread
sys.path.append("/flash/sys")
from helper import vibrating, distance
from weather import GetWeather, getCity
from notifications import readNotifications, seenNotifications, removeNotification, clearNotifications
notifications_data,notification_ind,subscreen,body_font,title_font,label_shadow_style=None,-1,None,None,None,None
def openPNG(path):
  with open(path,'rb') as f: data = f.read()
  return lv.img_dsc_t({'data_size': len(data),'data': data })
def loadWeather(img_w,label_c):
  label_c.set_text(" ...")
  if wifiCfg.wlan_sta.isconnected():
    wait(0.01)
    label_c.set_text(" .:.")
    w_data=GetWeather(getCity())
    try:
      label_c.set_text(w_data[2])
      img_w.set_src(openPNG(w_data[3]))
    except Exception as e: 
      pass
def viewerNotification():
  global subscreen
  subscreen = lv.obj()
  subscreen.set_style_local_text_font(0,0,body_font)
  page, label_cl,label_sub = lv.page(subscreen,None),lv.label(subscreen),lv.label(subscreen)
  page.set_size(320,215)
  label_cl.set_pos(238,220)
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label_sub.set_pos(130,220)
  label_sub.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_sub.set_text(lv.SYMBOL.TRASH+" Delete")
  d=notifications_data['tree'][::-1]
  d=d[notification_ind]
  label = lv.label(page, None)
  label.set_long_mode(lv.label.LONG.BREAK)
  label.set_recolor(True)         
  label.set_width(lv.page.get_width_fit(page))
  label.set_text("{}08a2b0 From: {}{}\n{}08a2b0 Body:{} {}".format(chr(35),d['from'],chr(35),chr(35),d['body'],chr(35)))
  lv.disp_load_scr(subscreen)
  pass
def event_handler(obj, event):
  global notification_ind
  if event == lv.EVENT.CLICKED:
    list_obj = obj.get_parent().get_parent()
    notification_ind=list_obj.get_btn_index(obj)
    if notification_ind!=-1:
      _thread.start_new_thread(viewerNotification,())
def showNotifications(list_f,label_sub):
  global notifications_data
  try:
    list_f.clean()
  except Exception as e: 
    pass
  notifications_data=readNotifications()
  list_f.set_hidden(False)
  try:
    for d in notifications_data['tree'][::-1]:
      l="{}: {}".format(d['from'],d['body'])
      if len(l)>36:
        l=l[:33]+"..."
      btn_new=list_f.add_btn(lv.SYMBOL.BELL,l)
      btn_new.set_event_cb(event_handler)
    if len(notifications_data['tree'])>0:
      label_sub.set_hidden(False)
    else:
      label_sub.set_hidden(True)
      btn_new=list_f.add_btn(lv.SYMBOL.BELL,"No notifications")
  except Exception as e:
    print("ERROR notifications"+str(e))
def notificationsExplorer(_body_font=lv.font_montserrat_14,_title_font=lv.font_montserrat_18):
  global subscreen, body_font, title_font, label_shadow_style,notification_ind
  body_font,title_font,root,label_shadow_style=_body_font,_title_font,lv.obj(),lv.style_t()
  root.set_style_local_text_font(0,0,body_font)
  label_shadow_style.init()
  label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
  label_cl,label_sub,page = lv.label(root),lv.label(root),lv.obj(root)
  label_cl.set_pos(238,220)
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label_sub.set_pos(130,220)
  label_sub.set_hidden(True)
  label_sub.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_sub.set_text(lv.SYMBOL.TRASH+" clear all")
  page.set_pos(220,0)
  page.set_style_local_text_color(0,0,lv.color_hex(0xa0a0a0))
  page.set_style_local_bg_color(0,0,lv.color_hex(0x48484a))
  page.set_size(100,50)
  label_c,img_w = lv.label(page),lv.img(page)
  label_c.set_pos(42,14)
  label_c.set_style_local_text_font(0,0,title_font)
  label_c.set_text(" ..")
  img_w.set_src(openPNG("/flash/res/weather/error.png"))
  label_h,list_f = lv.label(root),lv.list(root)
  label_h.set_pos(14,10)
  label_h.set_style_local_text_font(0,0,title_font)
  label_h.set_style_local_text_color(0,0,lv.color_hex(0x226577))
  label_h.set_text(lv.SYMBOL.BELL+"Notifications")
  list_f.set_size(320, 165)
  list_f.set_style_local_text_font(0,0,body_font)
  list_f.set_pos(0,50)
  lv.disp_load_scr(root)
  showNotifications(list_f,label_sub)
  vibrating()
  _thread.start_new_thread(loadWeather,(img_w,label_c))
  run,touched_time,touched_cord=True,0,None
  while run:
    if touch.status():
      if (touch.read()[1]) > 230:
        if touched_time==0:
          touched_time,touched_cord=time.ticks_ms(),touch.read()
        elif touched_time!=-1:
          if time.ticks_ms()-touched_time>250:
            if distance(touched_cord,touch.read())<3:
              touched_time=-1
              if (touch.read()[0])<315 and (touch.read()[0])>225:
                if subscreen!=None:
                  vibrating()
                  lv.disp_load_scr(root)
                  subscreen.delete()
                  subscreen=None
                elif label_cl.is_visible():
                  vibrating()
                  list_f.set_hidden(True)
                  label_cl.set_hidden(True)
                  label_sub.set_hidden(True)
                  seenNotifications()
                  run=False
              elif (touch.read()[0])<215 and (touch.read()[0])>115:
                if subscreen!=None:
                  list_f.set_hidden(True)
                  vibrating()
                  lv.disp_load_scr(root)
                  subscreen.delete()
                  subscreen=None
                  if notification_ind!=-1:
                    d=notifications_data['tree'][::-1]
                    noty_id=d[notification_ind]['id']
                    removeNotification(noty_id)
                  notification_ind=-1
                  showNotifications(list_f,label_sub)
                elif label_sub.is_visible():
                  vibrating()
                  list_f.set_hidden(True)
                  label_cl.set_hidden(True)
                  label_sub.set_hidden(True)
                  clearNotifications()
                  run=False
    else:
      touched_time=0
    wait(0.2)
  vibrating()
  return root