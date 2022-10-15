# Space Clock
[![Donate Bitcoin](https://img.shields.io/badge/donate-bitcoin-orange.svg)](https://github.com/pavelprosto94/space_clock/#user-content-you-can-support-me-too)

 Turn your M5Stack into a space clock
![preview](resources/help.jpg)

## What can they do:
- Animated space wallpaper with a flying astronaut
- Adaptive backlight mode will set the brightness depending on the time of day (Bright screen during the day and dim at night).
- Add up to 4 alarm clocks. You can set up a repeat by day of the week.
- Disable and activate alarms using the alarm clock manager.
- Get notifications from your phone via Bluetooth.
- Using the settings menu, you can synchronize your watch with the time from the Internet, adjust the brightness of the screen, select an alarm ringtone.
- Connect to Wi-Fi using Wi-Fi Manager(No need to reboot your device)
- View the weather using OpenWeather API
- Run the any *.py scripts from app directory(Calculator, Timer, Weather and etc.).
- You can enter debug mode directly from the watch menu.

## I plan to add:
- App store. Download applications from the Internet and run them from an SD card.
- Localization

## Installation
- Using M5 Burner, install the current version of UIFlow_Core 2 (If you have a new device)
- Restart your device
- Select Flow > Wi-Fi
- Go to M5Flow (https://flow.m5stack.com /)
- Specify your "API KEY" and device type "Core2"
- Switch to Python mode
- Copy and paste the code to set the clock from the file (https://github.com/pavelprosto94/space_clock/blob/main/install.py )
- Click the Run button
![preview](resources/help_1.jpg)
- Wait for the installation to finish. All necessary files will be copied from the GitHub repository
- After restart the device
- Select App > space_clock.py > Run

A bug may occur, the clock is not drawn, and the Run button is lit blue. Don't worry, M5Stack has already specified this file as the default execution.
- Don't press anything and wait 10 seconds
- After that, the clock will start itself

## Update device
- Restart your device
- Select Flow > Wi-Fi
- Go to M5Flow (https://flow.m5stack.com /)
- Specify your "API KEY" and device type "Core2"
- Switch to Python mode
- Copy and paste **New install** code from the file (https://github.com/pavelprosto94/space_clock/blob/main/install.py )
- Click the Run button
![preview](resources/help_1.jpg)
- Wait for the installation to finish. All necessary files will be copied from the GitHub repository
- After restart the device
- Select App > space_clock.py > Run

## Bluetooth support
Using this service, you will be able to connect your **M5Stack** via **Bluetooth** and receive notifications on it.

### on M5Stack device:
- Go to App List(hold down right button)
- Go to Bluetooth
- Enable service
- Save and Restart device
If you need an indication of the connection process, then turn on the "Bluetooth LED indicator".With this option, the green LED will light up when connected. If there is no connection, the LED will start flashing. Important, do not connect to the device until the clock is fully incilized (let the "Incilization..." disappear)

### on Android device:
Use **Gadgetbridge** to link your device and receive notifications.
Get it on [**F-Droid**](https://f-droid.org/ru/packages/nodomain.freeyourgadget.gadgetbridge/)
![](https://f-droid.org/repo/nodomain.freeyourgadget.gadgetbridge/en-US/phoneScreenshots/1-MainScreen.png)
- At the first launch, the application will request a set of necessary extensions. Provide them. Without them, it is impossible to forward notifications from the phone to the device.
- Click on the plus sign to add it. By default, the application does not support M5Stack.
- Click "Discovery and pairing options"
- Set "Discover unsupported devices"
- Run the scan again
- hold "M5Stack Core2"
- select the device type "Bangle.js (Espruino)"
- If your notifications are not in English. Then enable Transliteration of notifications. Click on the device settings and select the required language for Transliteration.

### Other device:
You can connect to the device via Bluetooth serial.
The form of the sent messages has the form:
**GB({t:"notify",id:"1234",body:"text notify",src:"title"})**

## You can support me too.
I accept donation via [Webmoney](https://www.wmtransfer.com/).<br />
My Webmoney(WMZ) wallet: **Z803753663501** <br />
Bitcoin wallet: [**1HyvAY4r8S82KdJwiy6igwHEY49ExHtZjs**](bitcoin:1HyvAY4r8S82KdJwiy6igwHEY49ExHtZjs?amount=0.0002) <br />
![](https://chart.googleapis.com/chart?chs=250x250&cht=qr&chl=1HyvAY4r8S82KdJwiy6igwHEY49ExHtZjs) <br />
