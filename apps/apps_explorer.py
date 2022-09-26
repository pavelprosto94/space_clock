try:
  if str(__file__) == "menu/app.py":
    import machine
    fileA = open('/flash/apps/apps_explorer.py', 'rb')
    fileB = open('/flash/main.py', 'wb')
    fileB.write(fileA.read())
    fileA.close()
    fileB.close()
    machine.reset()
except Exception as e:
  print("run list apps")
import lvgl as lv
rootLoading = lv.obj()
label = lv.label(rootLoading)
label.align(rootLoading,lv.ALIGN.CENTER, -20, 0)
label.set_text('Loading...')
lv.disp_load_scr(rootLoading)
from uiflow import wait
wait(0.01)
from m5stack import touch
import os, sys, time
sys.path.append("/flash/sys")
from helper import vibrating, distance, fileExist
root = lv.obj()
label_shadow_style = lv.style_t()
label_shadow_style.init()
label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
label_close = lv.label(root)
label_close.set_pos(238,220)
label_close.add_style(lv.label.PART.MAIN, label_shadow_style)
label_close.set_text(lv.SYMBOL.CLOSE+" close")
page = lv.page(root,None)
page.set_size(320,220)
lv.disp_load_scr(root)
apps=os.listdir("/flash/apps")
ignore=["_clock","apps_explorer"]
for l in ignore:
  i=0
  while i<len(apps):
    if l in apps[i]: apps.pop(i)
    i+=1 
ind_run=-1
def event_handler(obj, event):
  global ind_run
  if event == lv.EVENT.CLICKED:
    ind_run=int((obj.get_x()-3)/74)+int((obj.get_y()-5)/94)*4
for i,l in enumerate(apps):
  app_icon="/flash/res/programm.png"
  if fileExist("/flash/res/{}.png".format(l)):
    app_icon="/flash/res/{}.png".format(l)
  img = lv.imgbtn(page,None)
  img.set_pos(3+74*(i%4),5+int(i/4)*94)
  with open(app_icon,'rb') as f: data = f.read()
  img_dsc = lv.img_dsc_t({'data_size': len(data),'data': data })
  img.set_src(lv.btn.STATE.RELEASED,img_dsc)
  img.set_checkable(True)
  img.set_event_cb(event_handler)
  lbl = lv.label(page)
  lbl.set_hidden(True)
  lbl.set_pos(3+74*(i%4),74+int(i/4)*94)
  lbl.set_long_mode(lv.label.LONG.SROLL_CIRC)
  lbl.set_align(lv.label.ALIGN.CENTER)
  lbl.set_hidden(False)
  txt=l[:l.rfind(".")]
  if "_explorer" in txt:
    txt=txt[:txt.rfind("_explorer")]
  lbl.set_text(txt)
  lbl.set_size(64,18)
run=True
touched_time = 0
touched_cord = None
while run:
  if ind_run>-1:
    vibrating()
    lv.disp_load_scr(rootLoading)
    wait(0.01)
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
      exec(open("/flash/apps/{}".format(apps[ind_run])).read(),{})
    lv.disp_load_scr(root)
    ind_run=-1
  elif touch.status():
    if (touch.read()[1]) > 240:
      if touched_time==0:
        touched_time=time.ticks_ms()
        touched_cord = touch.read()
      elif touched_time!=-1:
        if time.ticks_ms()-touched_time>500:
          if distance(touched_cord,touch.read())<3:
            touched_time=-1
            if (touch.read()[0])<315 and (touch.read()[0])>225:
              vibrating()
              run=False
  else:
    touched_time=0
  wait(0.2)
label.set_text('')
lv.disp_load_scr(rootLoading)