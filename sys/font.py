import fs_driver
import lvgl as lv
lv.init()
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')

def font_14():
  return lv.font_montserrat_14

def font_18():
  return lv.font_montserrat_18

# def font_14():
#   return lv.font_load("S:fonts/XO_Caliburn_14.bin")

# def font_18():
#   return lv.font_load("S:fonts/XO_Caliburn_18.bin")