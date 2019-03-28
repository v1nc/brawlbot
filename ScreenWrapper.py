#wrapper for screen analysing
#reads http stream and returns ingame information
import numpy as np
import cv2, time, os, math
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

class ScreenWrapper:
	def __init__(self,stream_url,drop_rate,save,show):#create screen connection with given url
		self.save = save
		self.screen_capture = cv2.VideoCapture(stream_url)
		self.drop_rate = drop_rate
		self.drop_count = self.get_last_drop_count()
		self.show = show 
		self.colors = {"play": (8,195,235),"health" :(48,223,71) ,"enemy" : (58,37,187), 'health_grey' : (97,46,47) }
		self.coords = {"play" : (195,365), "att": (160,260)}
		self.raw_colors = {"att" : (254,201,156), 'att2' : (255,254,245), 'ulti': (41,40,96)}
		self.frames_needed = 5
		self.frame_counter = 0
		self.full_health = False
		self._init_colors()
	def _init_colors(self):
		for c in self.colors:
			self.colors[c] = convert_color(sRGBColor(self.colors[c][0],self.colors[c][1],self.colors[c][2]), LabColor)
	def get_information(self):#todo: make production method without ifs to speed up
		self.drop_count += 1
		ret = self.screen_capture.grab()
		if self.drop_count % self.drop_rate == 0: #drop frames to avoid delay
			ret, img = self.screen_capture.retrieve()
			if not ret:
				return (False,'stream failed')
			health_found, enemys = self._pixel_loop(img)
			#health_found = True
			if self.save:
				cv2.imwrite('screen_capture/%s.png'%self.drop_count,img)
			if self.show and health_found:
				cv2.imshow('VIDEO', img)
				if cv2.waitKey(1) == 27:
					return (False,'stream ended')
		return (True,False,'stream working')
	def get_information_prod(self):
		self.drop_count += 1
		ret = self.screen_capture.grab()
		if self.drop_count % self.drop_rate == 0: #drop frames to avoid delay
			self.frame_counter+=1
			ret, img = self.screen_capture.retrieve()
			if not ret:
				return (False,False)
			attack_color = img[self.coords["att"][0],self.coords["att"][1]]
			ulti = False
			if not ( self._compare_innacc(attack_color,self.raw_colors["att"],15) or self._compare_innacc(attack_color,self.raw_colors["att2"],15)):
				if not self._compare_innacc(attack_color,self.raw_colors["ulti"],15):
					print(attack_color)
					return (False,False)
				else:
					print(ulti)
					ulti = True
			health, enemys = self._pixel_loop(img)
			if not self.full_health and health:
				self.full_health = True
			if self.frame_counter == 5:
				self.frame_counter = 0
				return_full = self.full_health
				self.full_health = False
				return (True,True,return_full,enemys,ulti)
			return (True,False)
		return (True,False)		
	def wait_for_game(self):
		self.drop_count += 1
		ret = self.screen_capture.grab()
		if self.drop_count % self.drop_rate == 0 : #drop frames to avoid delay
			ret, img = self.screen_capture.retrieve()
			rows,cols,waste = img.shape
			if not cols == 384:
				return True
			if not ret:
				return False			
			if delta_e_cie2000(self._convert_color(img[self.coords["play"][0],self.coords["play"][1]]),self.colors["play"]) < 15:
				return False 
		return True
	def get_last_drop_count(self):
		count = 0
		for filename in os.listdir('screen_capture/'):
			tsplit =filename.split("_")
			tcount = int(tsplit[len(tsplit)-1].split(".png")[0])
			if tcount > count:
				count = tcount
		return count
	def _pixel_loop(self,img):#todo: kill display on left and right corner gets detected as enemy, thats bad uhh
		rows,cols,waste = img.shape
		health = False
		enemys = []
		ung = 20
		for i in range(rows):
		  for j in range(cols):
			if i > 30 and i< 145 and j > 20:
				if img[i,j][2] > 250 and img[i,j][0] > 250 and img[i,j][1] > 250: #bad check if text color above health bars
		  			try:#bad check if color under healthbar is like green
		  				#i+4 check -> wrong detection of the white circle!
		  				color_one = self._convert_color(img[i+1,j])
		  				color_two = self._convert_color(img[i+2,j])
		  				if not health and (delta_e_cie2000(color_one,self.colors['health']) < ung or delta_e_cie2000(color_two,self.colors['health']) < ung):
							#cv2.rectangle(clone, (j-25,i-25), (j + 25, i + 25), (0,255,0), 2)#draw bad rectangle around chars healthbar
							health = True
		  				elif not enemy and (delta_e_cie2000(color_one,self.colors['enemy']) < ung or delta_e_cie2000(color_two,self.colors['enemy']) < ung):
							#cv2.rectangle(clone, (j-25,i-25), (j + 25, i + 25), (0,0,255), 2)#draw bad rectangle around chars healthbar
							enemys.append((i,j))
					except:
						pass
		return (health, enemys)
	def _two_equals(tu,a):
		return (tu[0] == a and tu[1] == a) or (tu[0] == a and tu[2] == a) or (tu[1] == a and tu[2] == a)
	def _compare_innacc(self,a,b,acc):
		return abs(a[0]-b[0])<=acc and abs(a[1]-b[1])<=acc and abs(a[2]-b[2])<=acc
	def _compare23(self,a,b):
		return a[1] == b[1] and a[2] == b[2]
	def _convert_color(self,rgb):
		rgb_color = sRGBColor(rgb[0],rgb[1],rgb[2])
		lab_color = convert_color(rgb_color, LabColor);   
		return lab_color
	def close(self):
		self.screen_capturerelease()
		cv2.destroyAllWindows()

