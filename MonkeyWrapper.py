#wrapper for phone input via monkeyrunner
#todo: process stdout, what is completly ignored at this time!
from subprocess import Popen, PIPE, STDOUT
import time
class MonkeyWrapper:
	coords = {
		'shoot' : (1690,660),
		'ulti' : (1310,800),
		'reward' : (960,540),
		'play' : (1630,970),
		'leave' : (950,1000),#
		'box1': (190,360),
		'box2': (460,360),
		'reward_back': (65,85),
		'end_next': (1720,990),
		'end_leave': (1720,990),
	} 
	cmds_init = [
			'from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice',
			'device = MonkeyRunner.waitForConnection()',
			'package = "com.supercell.brawlstars"',
			'runComponent = package + "/" + package+".GameApp"',
			'device.shell("am force-stop com.supercell.brawlstars")',
			'device.startActivity(component=runComponent)',
	]
	def __init__(self):#create monkeyrunner connection and (re-)start game
		self.process = Popen(['monkeyrunner', '-u'], stdin=PIPE, stdout=PIPE, stderr=STDOUT,bufsize=1)
		self._cmd(self.cmds_init)	
	def close(self):
		self.process.stdin.close()
		self.process.stdout.close()
		self.process.wait()
	def action(self,action):
		if action in self.coords:
			self._touch(self.coords[action][0],self.coords[action][1])
	def collect_reward(self):#collect trophy rewards
		self.action('reward_back')
		self._wait()
		self.action('reward')
		self._wait()
		self.action('reward_back')
		self._wait()

	def leave_game(self):#end game round
		self.action('leave')
		self._wait()
		self.action('end_next')
		self._wait()
		self.action('end_leave')
		self._wait()
	def _wait(self):
		time.sleep(1)
	def _cmd(self,cmds):
		for c in cmds:
			print >>self.process.stdin, c
		self.process.stdin.flush()
	def touch(self):
		self.action('leave')
		self._wait()
	def _touch(self,x,y):
		self._cmd(['device.touch(%s,%s,MonkeyDevice.DOWN_AND_UP)'%(x,y)])