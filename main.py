from ScreenWrapper import ScreenWrapper
from MonkeyWrapper import MonkeyWrapper
import sys
def sprint(message):#print the same line so terminal doesnt get spammed
	sys.stdout.write("\r\x1b[K"+message.__str__())
	sys.stdout.flush()
#drop_rate depends on what is done in the loop:
#	1 for no drops to only display screen and/or save screenshots
#	5 is good for looping all pixels of the screen(what is possibly more than we have to do if we do it right)
#if delay gets bigger while streaming, the drop_rate is too low!
#normal delay in same network should be <1s!
#but bigger drop_rate => lower fps.
#i think drop_rate 5 could be acceptable for production, i get 1-2 fps with drop_rate 5
drop_rate = 5
#monkey_wrapper = MonkeyWrapper()# not used by now
save_screen = False#save screenshots to 'screen_capture'
show_screen = True#show screen in a window
screen_wrapper = ScreenWrapper('http://192.168.178.163:8080/stream.mjpeg',drop_rate,save_screen,show_screen)
succ = True
while succ:
	succ, out = screen_wrapper.get_information()
	sprint(out)