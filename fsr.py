# coding: utf-8
import huewe
import time
import sys
from datetime import datetime
import math



def fake_sunrise(mins, maxtemp, mintemp=800,steps=20):
	''' does a fake sunrise for some
		 mins up to a max temp '''
	dangle = math.pi / (2 * steps * mins)
	rng = maxtemp - mintemp
	if huewe.get_br():
		bedr = huewe.get_br().lights[0]
		bedr.on = True
		bedr.transitiontime = 600.0 / steps
		for i in range(mins * steps):
			sinx = math.sin(dangle * i)
			tmp = mintemp + sinx * rng
			bedr.xy = huewe.full_temp_to_xy(tmp)
			bedr.brightness = int(sinx * 255)
			print tmp, bedr.brightness/255.0, bedr.xy
			time.sleep(60.0 / steps)
	
def fake_sunset(mins, maxtemp, mintemp=800,steps=20,maxbri=1):
	''' does a fake sunset for some
		 mins up to a max temp '''
	dangle = math.pi / (2 * steps * mins)
	rng = maxtemp - mintemp
	if huewe.get_br():
		bedr = huewe.get_br().lights[0]
		bedr.on = True
		bedr.transitiontime = 600.0 / steps
		for i in range(mins * steps):
			cosx = math.cos(dangle * i)
			tmp = mintemp + cosx * rng
			bedr.xy = huewe.full_temp_to_xy(tmp)
			bedr.brightness = int(maxbri * cosx * 255)
			print tmp, bedr.brightness/255.0, bedr.xy
			time.sleep(60.0 / steps)
		bedr.on = False
			
			
def main():
	now = datetime.fromtimestamp(time.time())
	maxtemp = 4500
	mins = 30
	if len(sys.argv) > 1:
		mins = sys.argv[1]
	if len(sys.argv) > 2:
		maxtemp = sys.argv[2]
	if now.hour >= 20.0:
		fake_sunset(mins, maxtemp, 1200)
	else:
		fake_sunrise(mins, maxtemp, 1200)
	
	
if __name__ == "__main__": main()