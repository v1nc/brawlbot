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
    def get_information(self):
        self.drop_count += 1
        ret = self.screen_capture.grab()
        if self.drop_count % self.drop_rate == 0: #drop frames to avoid delay
            ret, frame = self.screen_capture.retrieve()
            if not ret:
                return (False,'stream failed')
            img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)#loop all pixels
            rows,cols,waste = frame.shape
            for i in range(rows):#simulate pixel loop to test drop_rate, delay and fps
              for j in range(cols):
                pass
                #print(self._convert_color( img[i,j]))#print lab color
                #delta_e_cie2000(color1_lab, color2_lab) color difference
            if self.save:
                cv2.imwrite('screen_capture/%s.png'%drop_count,img)
            if self.show:
                cv2.imshow('VIDEO', frame)
                if cv2.waitKey(1) == 27:
                    return (False,'stream ended')
        return (True,'stream working')
    def _convert_color(self,rgb):
        rgb_color = sRGBColor(rgb[0],rgb[1],rgb[2])
        lab_color = convert_color(rgb_color, LabColor);   
        return lab_color   
    def close(self):
        self.screen_capturerelease()
        cv2.destroyAllWindows()
