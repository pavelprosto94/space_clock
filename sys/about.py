from m5stack import *
from m5stack_ui import *
from uiflow import *
import sys
sys.path.append("/flash/sys")
from helper import vidro

def AboutScreen(screen):
  screen0 = screen.get_new_screen()
  screen.load_screen(screen0)
  M5Img("res/space_clock/cosmonaut_0.png", x=110, y=20, parent=screen0)
  M5Label('Space clock', x=95, y=129, color=0x000, font=FONT_MONT_22, parent=screen0)
  M5Label('v1.0', x=225, y=129, color=0x0288fb, font=FONT_MONT_14, parent=screen0)
  M5Label('Created by Pavel Prosto', x=75, y=158, color=0x000, font=FONT_MONT_14, parent=screen0)
  M5Label('https://github.com/pavelprosto94/space_clock', x=40, y=182, color=0x034c76, font=FONT_MONT_10, parent=screen0)
  M5Label("close", x=238, y=224, color=0xd84949, font=FONT_MONT_14, parent=screen0)
  run=True
  touched_time=1
  while run:
    if touch.status():
      if touched_time==0:
        if (touch.read()[1]) > 240:
          touched_time=1
          vidro()
          run=False
    else:
      if touched_time>0:
        touched_time=0