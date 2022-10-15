from m5stack import touch, lv
rootLoading = lv.obj()
label = lv.label(rootLoading)
label.align(rootLoading,lv.ALIGN.CENTER, -20, 0)
label.set_text('Loading...')
lv.disp_load_scr(rootLoading)
from uiflow import wait
wait(0.01)
if not 'body_font' in dir(): body_font=lv.font_montserrat_14
if not 'title_font' in dir(): title_font=lv.font_montserrat_18
import os, sys, time
sys.path.append("/flash/sys")
from helper import vibrating, distance, fileExist
def event_handler(obj, event):
  global ind_run
  if event == lv.EVENT.CLICKED:
    list_btn = lv.list.__cast__(obj)
    for i,l in enumerate(apps):
      txt=l[:l.rfind(".")]
      if "_explorer" in txt: txt=txt[:txt.rfind("_explorer")]
      if list_btn.get_btn_text()==txt:
        ind_run=i
        break
root,label_shadow_style = lv.obj(),lv.style_t()
root.set_style_local_text_font(0,0,body_font)
label_shadow_style.init()
label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
label_close,list1 = lv.label(root),lv.list(root)
label_close.set_pos(238,220)
label_close.add_style(lv.label.PART.MAIN, label_shadow_style)
label_close.set_text(lv.SYMBOL.CLOSE+" close")
ind_run,apps,_ignore=-1,os.listdir("/flash/apps"),["_clock","apps_explorer"]
for l in _ignore:
  i=0
  while i<len(apps):
    if l in apps[i]: apps.pop(i)
    i+=1
list1.set_size(320, 215)
list1.set_style_local_text_font(0,0,title_font)
for i,l in enumerate(apps):
  app_icon="/flash/res/programm.png"
  if fileExist("/flash/res/{}.png".format(l)):
    app_icon="/flash/res/{}.png".format(l)
  with open(app_icon,'rb') as f: data = f.read()
  img_dsc = lv.img_dsc_t({'data_size': len(data),'data': data })
  txt=l[:l.rfind(".")]
  if "_explorer" in txt: txt=txt[:txt.rfind("_explorer")]
  list_btn = list1.add_btn(img_dsc,txt)
  list_btn.set_event_cb(event_handler)
lv.disp_load_scr(root)
run,touched_time,touched_cord,protect_mode=True,0,[0,0],False
while run:
  if ind_run>-1:
    lv.disp_load_scr(rootLoading)
    wait(0.01)
    vibrating()
    if apps[ind_run]=="Alarm_explorer.py":
      sys.path.append("/flash/apps")
      from Alarm_explorer import alarmExplorer
      subscreen=alarmExplorer(None)
      lv.disp_load_scr(root)
      subscreen.delete()
    elif apps[ind_run]=="Notify_explorer.py":
      sys.path.append("/flash/apps")
      from Notify_explorer import notificationsExplorer
      subscreen=notificationsExplorer()
      lv.disp_load_scr(root)
      subscreen.delete()
    else:
      fdata=open("/flash/apps/{}".format(apps[ind_run]), 'r')
      data=fdata.read()
      fdata.close()
      if not "while run:" in data:
        protect_mode=True
        label_close.set_parent(rootLoading)
        label.set_text('')
      try:
        exec(data,{"__file__":"Apps",'body_font':body_font, 'title_font':title_font})
      except Exception as e:
        rootLoading = lv.obj()
        label = lv.label(rootLoading)
        label.set_text(str(e))
        label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
        lv.disp_load_scr(rootLoading)
    if not protect_mode: lv.disp_load_scr(root)
    ind_run=-1
  elif touch.status():
    if touched_time==0: touched_time,touched_cord=time.ticks_ms(),touch.read()
    elif (touch.read()[1]) > 240:
      if touched_time!=-1:
        if time.ticks_ms()-touched_time>250:
          if distance(touched_cord,touch.read())<3:
            touched_time=-1
            if (touch.read()[0])<315 and (touch.read()[0])>225:
              vibrating()
              if not protect_mode: run=False
              else:
                protect_mode,rootLoading=False,lv.obj()
                label = lv.label(rootLoading)
                label.set_text('Loading...')
                label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
                label_close = lv.label(root)
                label_close.set_pos(238,220)
                label_close.add_style(lv.label.PART.MAIN, label_shadow_style)
                label_close.set_text(lv.SYMBOL.CLOSE+" close")
                lv.disp_load_scr(root)
  elif touched_time!=0: touched_time=0
  wait(0.1)
label.set_text('')
lv.disp_load_scr(rootLoading)