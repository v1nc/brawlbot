#wrapper for screen analysing
#reads http stream and returns ingame information
import numpy as np
import cv2, time
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
class ScreenWrapper:
	def __init__(self,stream_url,drop_rate,save,show):#create screen connection with given url
		self.save = save
		self.screen_capture = cv2.VideoCapture(stream_url)
		self.drop_rate = drop_rate
		self.drop_count = 0
		self.show = show
		self.colors = {"health" : convert_color(sRGBColor(48,223,71), LabColor)}
	def get_information(self):#todo: make production method without ifs to speed up
		self.drop_count += 1
		ret = self.screen_capture.grab()
		if self.drop_count % self.drop_rate == 0: #drop frames to avoid delay
			ret, img = self.screen_capture.retrieve()
			if not ret:
				return (False,'stream failed')			
			img = self._pixel_loop(img)
			if self.save:
				cv2.imwrite('screen_capture/%s.png'%self.drop_count,img)
			if self.show:
				cv2.imshow('VIDEO', img)
				if cv2.waitKey(1) == 27:
					return (False,'stream ended')
		return (True,'stream working')
	def _pixel_loop(self,img):
		rows,cols,waste = img.shape
		for i in range(rows):
		  for j in range(cols):
			if i > 30 and j > 30:
				if img[i,j][2] == 255 and img[i,j][0] == 255: #bad check if text color above health bars
		  			try:#bad check if color under healthbar is like green
		  				if delta_e_cie2000(self._convert_color(img[i+1,j]),self.colors['health']) < 15 or delta_e_cie2000(self._convert_color(img[i+2,j]),self.colors['health']) < 15:
							cv2.rectangle(img, (j-25,i-25), (j + 25, i + 25), (0,0,255), 2)#draw bad rectangle around chars healthbar
							return img
					except:
						pass
		return img
	def _two_equals(tu,a):
		return (tu[0] == a and tu[1] == a) or (tu[0] == a and tu[2] == a) or (tu[1] == a and tu[2] == a)
	def _convert_color(self,rgb):
		rgb_color = sRGBColor(rgb[0],rgb[1],rgb[2])
		lab_color = convert_color(rgb_color, LabColor);   
		return lab_color
	def close(self):
		self.screen_capturerelease()
		cv2.destroyAllWindows()

