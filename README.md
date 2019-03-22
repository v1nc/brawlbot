# brawlbot
- pip2.7 install -r requirements.txt
- install android sdk and add '../Android/Sdk/tools/bin' to $PATH(or change path in MonkeyWrapper)
- install [app](https://play.google.com/store/apps/details?id=info.dvkr.screenstream) to stream screen over http
- set 20% resize and 100% compression in app settings
- connect phone or emulator via adb
- start screen sharing and edit url in main.py
- python2.7 main.py

## todo:
- port to python3
- process monkeyrunner stdout
- add monkeyrunner methods for character movement
- get information from the screen
