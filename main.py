from ScreenWrapper import ScreenWrapper
from MonkeyWrapper import MonkeyWrapper
import sys, time
def sprint(message):#print the same line so terminal doesnt get spammed
	sys.stdout.write("\r\x1b[K"+message.__str__())
	sys.stdout.flush()
def collect_rewards():#collect rewards
	monkey_wrapper.collect_reward()
	monkey_wrapper.action('box1')
	wait_reward = True
	while wait_reward:
		wait_reward = screen_wrapper.wait_for_game()
		monkey_wrapper.touch()
	while wait_reward:
		wait_reward = screen_wrapper.wait_for_game()
		monkey_wrapper.touch()
#drop_rate depends on what is done in the loop:
#	1 for no drops to only display screen and/or save screenshots
#	5 is good for looping all pixels of the screen(what is possibly more than we have to do if we do it right)
#if delay gets bigger while streaming, the drop_rate is too low!
#normal delay in same network should be <1s!
#but bigger drop_rate => lower fps.
#i think drop_rate 5 could be acceptable for production, i get 1-2 fps with drop_rate 5

#!!
#pixel loop runs the whole time. dont start before ingame until pixel loop checks for ingame start!
#!!
drop_rate = 2
#monkey_wrapper = MonkeyWrapper()# not used by now
save_screen = True #save screenshots to 'screen_capture'
show_screen = True#show screen in a window
screen_wrapper = ScreenWrapper('http://192.168.178.163:8080/stream.mjpeg',drop_rate,save_screen,show_screen)
#wait_game = True
#sprint("waiting for the game")
#time.sleep(15)
#while wait_game:
#	wait_game = screen_wrapper.wait_for_game()
#collect_rewards()
#while not wait_game:
#	wait_game = screen_wrapper.wait_for_game()
#	monkey_wrapper.action('play')
#	time.sleep(1)
#time.sleep(5)
#wait for game controlls here
succ = True
while succ:
	info = screen_wrapper.get_information_prod()
	succ = info[0]
	if info[0] and info[1]:
		print('full health:%s, enemys: %s, ulti: %s'%(info[2],len(info[3]),info[4]))