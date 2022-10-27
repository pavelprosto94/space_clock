try:
  if str(__file__) == "menu/app.py":
    import machine
    fileA = open('/flash/apps/Files_explorer.py', 'rb')
    fileB = open('/flash/main.py', 'wb')
    fileB.write(fileA.read())
    fileA.close()
    fileB.close()
    machine.reset()
except Exception as e:
  print("run alarm")
from m5stack import touch, lv, lcd
rootLoading = lv.obj()
label = lv.label(rootLoading)
label.align(rootLoading,lv.ALIGN.CENTER, -20, 0)
label.set_text('Loading...')
lv.disp_load_scr(rootLoading)
from uiflow import wait
wait(0.01)
import os, sys, time, _thread
sys.path.append("/flash/sys")
from helper import vibrating, distance
listDir = []
path = "/flash"
buffer=None  

def loadBMP():
  global buffer
  filename=buffer
  buffer=None
  wait(1)
  lcd.fill(0x222222)
  try:
    with open('{}/{}'.format(path,filename),'rb') as f: data=f.read()
    st = int.from_bytes(data[10:14], "little")
    w = int.from_bytes(data[18:22], "little")
    h = int.from_bytes(data[22:26], "little")
    color_mode = int.from_bytes(data[28:32], "little")
    line_b = int(int.from_bytes(data[34:38], "little")/h)
    r,g,b=0,0,0
    if w<=320 and h<=240 and color_mode==24 and w%4==0 and h%4==0:
      for i,d in enumerate(data[st:]):
        if i%3==0: b=d
        if i%3==1: g=d
        if i%3==2: 
          r,x,y=d,int((i/3))%w,h-int((i/3)/w)
          lcd.pixel(int((320-w)/2)+x, int((240-h)/2)+y, int(r*256*256+g*256+b))
      lcd.print("close", 245, 224, 0xd84949)
    else:
      lcd.print("unsupported BMP format", 0, 0, 0xff0000)
  except Exception as e:
    lcd.print('{}/{}'.format(path,filename), 0, 0, 0xff0000)
    lcd.print(str(e), 0, 16, 0xff0000)

def loadImage(filename):
  global subscreen
  global buffer
  subscreen=lv.obj()
  subscreen.set_style_local_bg_color(0,0,lv.color_hex(0x222222))
  if ".png" != filename[filename.rfind("."):] and ".bmp" != filename[filename.rfind("."):]:
    label_file = lv.label(subscreen)
    label_file.set_style_local_text_color(0,0,lv.color_hex(0xa20000))
    label_file.set_text("{} Just support PNG and BMP file for now".format(lv.SYMBOL.WARNING))
    label_file.align(None,lv.ALIGN.CENTER,0,0)
  elif ".png" == filename[filename.rfind("."):]:
    img = lv.img(subscreen,None)
    with open('{}/{}'.format(path,filename),'rb') as f:
      data = f.read()
    img_dsc = lv.img_dsc_t({
      'data_size': len(data),
      'data': data 
    })
    img.set_src(img_dsc)
    img.align(None,lv.ALIGN.CENTER,0,0)
  label_cl = lv.label(subscreen)
  label_cl.set_pos(238,220)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  lv.disp_load_scr(subscreen)
  if ".bmp" == filename[filename.rfind("."):]:
    buffer=filename
    _thread.start_new_thread(loadBMP,())

def loadText(filename):
  global subscreen
  subscreen=lv.obj()
  data=None
  with open('{}/{}'.format(path,filename),'r') as f:
    data = f.read()
  ta = lv.textarea(subscreen,None)
  ta.set_size(320,220)
  ta.set_text(data)
  label_cl = lv.label(subscreen)
  label_cl.set_pos(238,220)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  lv.disp_load_scr(subscreen)

def PasteDialog():
  global subscreen
  global buffer
  label_sub.set_hidden(True)
  subscreen=lv.obj()
  label_cl = lv.label(subscreen)
  label_cl.set_pos(238,220)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  label_cl.set_hidden(True)
  f_name=buffer[buffer.rfind("/")+1:]
  f_do=buffer[:buffer.rfind(":")]
  f_path=buffer[buffer.rfind(":")+1:buffer.rfind("/")]
  buffer=None
  label_file = lv.label(subscreen)
  label_file.set_style_local_text_font(0,0,lv.font_montserrat_18)
  label_file.set_style_local_text_color(0,0,lv.color_hex(0x08a2b0))
  label_file.set_text("{} {} file {}".format(lv.SYMBOL.PASTE,f_do,f_name))
  label_file.align(None,lv.ALIGN.CENTER,0,-60)
  label_path = lv.label(subscreen)
  label_path.set_pos(25,75)
  label_path.set_style_local_text_font(0,0,lv.font_montserrat_14)
  label_path.set_style_local_text_color(0,0,lv.color_hex(0x707070))
  label_path.set_text("from: {}".format(f_path))
  label_path_to = lv.label(subscreen)
  label_path_to.set_pos(25,90)
  label_path_to.set_style_local_text_font(0,0,lv.font_montserrat_14)
  label_path_to.set_style_local_text_color(0,0,lv.color_hex(0x707070))
  label_path_to.set_text("to: {}".format(path))
  bar1 = lv.bar(subscreen,None)
  bar1.set_size(250,20)
  bar1.align(None,lv.ALIGN.CENTER,0,0)
  label_e=lv.label(subscreen)
  label_e.set_style_local_text_font(0,0,lv.font_montserrat_14)
  label_e.set_style_local_text_color(0,0,lv.color_hex(0x707070))
  lv.disp_load_scr(subscreen)
  if f_path!=path:
    try:
      fileA = open('{}/{}'.format(f_path,f_name), 'rb')
      fileB = open('{}/{}'.format(path,f_name), 'wb')
      length=os.stat('{}/{}'.format(f_path,f_name))[6]
      i=0
      block_size=1024
      while True:
        chunk = fileA.read(block_size)
        if chunk == b"":
            break
        bar1.set_value(int(i/length*100),lv.ANIM.ON)
        label_e.set_text("{}/{}".format(i,length))
        label_e.align(None,lv.ALIGN.CENTER,0,20)
        fileB.write(chunk)
        i+=block_size
        wait(0.2)
      fileA.close()
      fileB.close()
      if(f_do=="Cut"):
        os.remove('{}/{}'.format(f_path,f_name))
    except Exception as e:
      label_file.set_style_local_text_color(0,0,lv.color_hex(0xa20000))
      label_file.set_text("ERROR {} {} file {}".format(lv.SYMBOL.WARNING,f_do,f_name))
      label_file.align(None,lv.ALIGN.CENTER,0,-60)
      label_e.set_style_local_text_color(0,0,lv.color_hex(0xa20000))
      label_e.set_text(str(e))
      label_e.align(None,lv.ALIGN.CENTER,0,20)
      label_cl.set_hidden(False)
    else:
      bar1.set_value(100,lv.ANIM.ON)
      label_e.set_text("Success!")
      label_e.align(None,lv.ALIGN.CENTER,0,20)
      label_cl.set_hidden(False)
      printDir()

def event_delete_handler(obj, event):
  global buffer
  global subscreen
  if event == lv.EVENT.VALUE_CHANGED:
    if obj.get_active_btn_text()=="Yes":
      os.remove('{}/{}'.format(path,buffer))
      printDir()
    buffer=None
    obj.start_auto_close(0)

def DeleteDialog():
  btns = ["Yes", "No", ""]
  mbox1 = lv.msgbox(root)
  mbox1.set_text("Are you sure you want to delete the file {}?".format(buffer));
  mbox1.add_btns(btns)
  mbox1.set_width(250)
  mbox1.set_event_cb(event_delete_handler)
  mbox1.align(None, lv.ALIGN.CENTER, 0, 0)
  
def getType(filename):
  if filename=="..":
    return lv.SYMBOL.NEW_LINE
  elif os.stat('{}/{}'.format(path,filename))[0] == 0x4000:
    return lv.SYMBOL.DIRECTORY
  else:
    exp=filename[filename.rfind("."):]
    if exp==".py" or exp==".txt" or exp==".js" or exp==".json":
      return lv.SYMBOL.EDIT
    elif exp==".png" or exp==".jpg" or exp==".bmp" or exp==".gif":
      return lv.SYMBOL.IMAGE
    elif exp==".wav":
      return lv.SYMBOL.AUDIO
    else:
      return lv.SYMBOL.FILE

def fileOpen(filename):
  global path
  if filename=="..":
    path=path[:path.rfind("/")]
    printDir()
  elif getType(filename)==lv.SYMBOL.DIRECTORY:
    path='{}/{}'.format(path,filename)
    printDir()
  elif getType(filename)==lv.SYMBOL.IMAGE:
    loadImage(filename)
  elif getType(filename)==lv.SYMBOL.EDIT:
    loadText(filename)

def event_keybHandler(obj, event):
  global subscreen
  global ta
  global buffer
  obj.def_event_cb(event)
  if event == lv.EVENT.CANCEL:
    lv.disp_load_scr(root)
    subscreen.delete()
    subscreen=None
    buffer=None
  elif event == lv.EVENT.APPLY:
    lv.disp_load_scr(root)
    newname=str(obj.get_textarea().get_text())
    if len(newname)>0:
      if newname!=buffer:
        os.rename('{}/{}'.format(path,buffer),'{}/{}'.format(path,newname))
        printDir()
    subscreen.delete()
    subscreen=None
    buffer=None

def showKeyb():
  global subscreen
  global buffer
  subscreen=lv.obj()
  lbl = lv.label(subscreen)
  lbl.set_pos(10,5)
  lbl.set_text("Set new name:")
  ta=lv.textarea(subscreen,None)
  ta.set_accepted_chars("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz._-")
  ta.set_size(300,35)
  ta.set_pos(10,22)
  ta.set_text(buffer)        
  keyb = lv.keyboard(subscreen,None)
  keyb.set_cursor_manage(True)
  keyb.set_event_cb(event_keybHandler)
  keyb.set_textarea(ta)
  keyb.set_pos(0,70)
  keyb.set_size(320,170)
  lv.disp_load_scr(subscreen)
    
def eventFiles_handler(obj, event):
  global buffer
  global subscreen
  if event == lv.EVENT.CLICKED:
    list_btn = lv.list.__cast__(obj)
    do=list_btn.get_btn_text()
    if do=="Open":
      lv.disp_load_scr(rootLoading)
      subscreen.delete()
      subscreen=None
      fileOpen(buffer)
      buffer=None
    elif do=="Copy" or do=="Cut":
      lv.disp_load_scr(root)
      subscreen.delete()
      subscreen=None
      buffer="{}:{}/{}".format(do,path,buffer)
      label_sub.set_text(lv.SYMBOL.PASTE+" paste")
      label_sub.set_hidden(False)
    elif do=="Rename":
      lv.disp_load_scr(root)
      subscreen.delete()
      subscreen=None
      showKeyb()
    elif do=="Delete":
      lv.disp_load_scr(root)
      subscreen.delete()
      subscreen=None
      DeleteDialog()

def filesMenu(filename):
  global subscreen
  global buffer
  label_sub.set_hidden(True)
  subscreen=lv.obj()
  buffer=filename
  list1 = lv.list(subscreen)
  list1.set_size(200, 220)
  list1.align(None, lv.ALIGN.CENTER, -50, 0)
  if getType(filename)!=lv.SYMBOL.FILE:
    list_btn = list1.add_btn(lv.SYMBOL.DIRECTORY, "Open")
    list_btn.set_event_cb(eventFiles_handler)
  if path!="":
    list_btn = list1.add_btn(lv.SYMBOL.EDIT, "Rename")
    list_btn.set_event_cb(eventFiles_handler)
    if getType(filename)!=lv.SYMBOL.DIRECTORY:
      list_btn = list1.add_btn(lv.SYMBOL.COPY, "Copy")
      list_btn.set_event_cb(eventFiles_handler)
      list_btn = list1.add_btn(lv.SYMBOL.CUT, "Cut")
      list_btn.set_event_cb(eventFiles_handler)
      list_btn = list1.add_btn(lv.SYMBOL.TRASH, "Delete")
      list_btn.set_event_cb(eventFiles_handler)
  label_cl = lv.label(subscreen)
  label_cl.set_pos(238,220)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  lv.disp_load_scr(subscreen)
  
def event_handler(obj, event):
  if subscreen==None:
    if event == lv.EVENT.LONG_PRESSED:
      list_btn = lv.list.__cast__(obj)
      if (list_btn.get_btn_text()!=".."):
        vibrating()
        filesMenu(list_btn.get_btn_text())
    elif event == lv.EVENT.CLICKED:
      list_btn = lv.list.__cast__(obj)
      fileOpen(list_btn.get_btn_text())

def printDir():
  global listDir
  global path
  vibrating()
  try:
    list_f.clean()
  except Exception as e: 
    pass
  if path=="":
    listDir = ["flash","sd"]
    for l in listDir:
      btn_new=list_f.add_btn(lv.SYMBOL.DIRECTORY,l)
      btn_new.set_event_cb(event_handler)
  else:
    try:
      listDir = os.listdir(path)
    except Exception as e: 
      label.set_pos(0,0)
      label.set_text(str(e))
      lv.disp_load_scr(rootLoading)
    else:
      listDir.insert(0,"..")
      for l in listDir:
        btn_new=list_f.add_btn(getType(l),l)
        btn_new.set_event_cb(event_handler)

root = lv.obj()
subscreen=None
label_shadow_style = lv.style_t()
label_shadow_style.init()
label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
label_close = lv.label(root)
label_close.set_pos(238,220)
label_close.add_style(lv.label.PART.MAIN, label_shadow_style)
label_close.set_text(lv.SYMBOL.CLOSE+" close")
label_sub = lv.label(root)
label_sub.set_pos(130,220)
label_sub.add_style(lv.label.PART.MAIN, label_shadow_style)
label_sub.set_hidden(True)
label_sub.set_text(lv.SYMBOL.PASTE+" paste")
list_f = lv.list(root)
list_f.set_size(320, 220)
list_f.set_pos(0,0)
printDir()
lv.disp_load_scr(root)

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
              vibrating()
              if subscreen!=None:
                lv.disp_load_scr(root)
                subscreen.delete()
                subscreen=None
                buffer=None
              elif buffer!=None and subscreen==None:
                buffer=None
                label_sub.set_hidden(True)
              else:
                run=False
            elif (touch.read()[0])<215 and (touch.read()[0])>115:
              if buffer!=None and subscreen==None:
                vibrating()
                PasteDialog()
              pass
  else:
    touched_time=0
  wait(0.2)
label.set_text('')
lv.disp_load_scr(rootLoading)