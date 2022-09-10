from m5stack import *
from m5stack_ui import *
from uiflow import *
import sys
sys.path.append("/flash/sys")
from helper import vidro

def NotificationsScreen(screen):
  screen0 = screen.get_new_screen()
  screen.load_screen(screen0)
  M5Label('coming soon...', x=108, y=113, color=0x717171, font=FONT_MONT_14, parent=screen0)
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