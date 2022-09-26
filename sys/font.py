import fs_driver
import lvgl as lv
lv.init()
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')

def XO_Caliburn_12():
  return lv.font_load("S:fonts/XO_Caliburn_12.bin")

def XO_Caliburn_14():
  return lv.font_load("S:fonts/XO_Caliburn_14.bin")

def XO_Caliburn_16():
  return lv.font_load("S:fonts/XO_Caliburn_16.bin")

def XO_Caliburn_20():
  return lv.font_load("S:fonts/XO_Caliburn_20.bin")