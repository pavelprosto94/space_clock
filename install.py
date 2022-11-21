from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg, _thread, urequests, os

def mkDir(path):
  try:
    os.mkdir("/flash/"+path[:path.rfind("/")])
  except Exception as e: 
    return ""
  return "/flash/"+path[:path.rfind("/")]

def rmdir(dir):
    for i in os.listdir(dir):
        os.remove('{}/{}'.format(dir,i))
    os.rmdir(dir)

url="https://api.github.com/repos/pavelprosto94/space_clock/git/trees/main?recursive=1"
animation_enable = -1

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

M5Img("img/setup_bar_320_40.png", x=0, y=0, parent=None)
image0 = M5Img("img/wifi_config_ap_connect.png", x=128, y=64, parent=None)
label0 = M5Label('Checking Wi-Fi connection.', x=10, y=165, color=0x000, font=FONT_MONT_14, parent=None)
label1 = M5Label('', x=10, y=194, color=0xff0000, font=FONT_MONT_14, parent=None)
bar0 = M5Bar(x=64, y=145, w=192, h=12, min=0, max=100, bg_c=0xa0a0a0, color=0x08A2B0, parent=None)
if not wifiCfg.wlan_sta.isconnected():
  wait(0.5)
  screen0 = screen.get_act_screen()
  wait(0.5)
  wifiCfg.autoConnect()
  wait(1)
  screen.load_screen(screen0)

if wifiCfg.wlan_sta.isconnected():
  image0.set_network_img_src("https://raw.githubusercontent.com/pavelprosto94/space_clock/main/resources/install_download.png")
  label0.set_text("Initialization")
  try:
    os.remove('apps/RGB-Color-Pick.py')
  except Exception as e:
    label0.set_text(str(e))
  try:
    rmdir('emojiImg')
  except Exception as e:
    label0.set_text(str(e))
  def playAlarm():
    global animation_enable
    img=[]
    for i in range(0,3):
      img.append(M5Img("https://raw.githubusercontent.com/pavelprosto94/space_clock/main/resources/install_download_pr_{}.png".format(i), x=128, y=64, parent=None))
    wait(0.1)
    animation_enable = 3
    while animation_enable>-1:
      if animation_enable < 3:
        img[animation_enable].set_hidden(False)
        animation_enable+=1
      elif animation_enable<6:
        img[animation_enable-6].set_hidden(True)
        animation_enable+=1
      else:
        animation_enable=0
      wait(1)       
        
  _thread.start_new_thread(playAlarm,())
  while animation_enable==-1:
    wait(1)
  installing=False
  label0.set_text("Connecting to git...")
  try:
    ignore=[
      "README.md",
      "install.py"
    ]
    data = urequests.request(method="GET", url=url, headers={ 'User-Agent': 'M5Stack'})
    data = data.json()
    if not "tree" in data:
      if "message" in data:
        label0.set_text(str(data["message"]))
      else:
        label0.set_text("Error 0")
    else:
      bar0.set_range(0, len(data["tree"]))
      for i,d in enumerate(data["tree"]):
        bar0.set_value(i)
        if d["type"]=="blob":
          path=d["path"]
          if not (path in ignore) and path[0]!="." and path[:path.find("/")]!="resources":
            label0.set_text("Writing...\n{}".format(path))
            if "/" in path:
              ans=mkDir(path)
              if ans!="":
                label0.set_text("Made path:\n{}".format(path))
            file_d = urequests.request(method="GET", url="https://raw.githubusercontent.com/pavelprosto94/space_clock/main/{}".format(path), headers={ 'User-Agent': 'M5Stack'})
            if (path[path.rfind(".")])==".py" or (path[path.rfind(".")])==".txt":
              with open("/flash/"+path, 'w') as f:
                f.write(file_d.text) 
            else:
              with open("/flash/"+path, 'wb') as f:
                f.write(file_d.content) 
      installing=True
  except Exception as e: 
    label1.set_text(str(e))
  else:
    if installing:
      import deviceCfg
      fileA = open('/flash/apps/space_clock.py', 'rb')
      fileB = open('/flash/main.py', 'wb')
      fileB.write(fileA.read())
      fileA.close()
      fileB.close()
      deviceCfg.set_device_mode(2)
      deviceCfg.random_new_apikey()
      #deviceCfg.save_wifi("","")
      label0.set_text("Installation is complete.\nRestart your device now.")
  animation_enable = -1
else:
  image0.set_img_src("img/wifi_config_sta_fail.png")
  label0.set_text("No connection to Wi-Fi.\nRestart your device and try again")