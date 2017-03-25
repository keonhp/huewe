import pywapi
import phue
import time
import math
import pickle
import spline
from datetime import datetime

_brbr = False
_ciexy = False
_waketime = (4, 40) # hour, minute
ev = u'USCA0350'
oak = u'USCA0791'

def get_br():
	'''singleton for bridge'''
	global _brbr
	
	if not _brbr:
		_brbr = phue.Bridge('192.168.56.150')
		try:
			_brbr.get_light(0)
		except Exception as e:
			print e.message
			_brbr = False
	return _brbr
	

def get_weather(where):
	'''let's query for oakland weather'''
	yahoo = pywapi.get_weather_from_yahoo(where)
	return yahoo
	
	
def get_angle(report):
	'''takes a full report gets sun angle'''
	astr = report['astronomy']
	rise = datetime.strptime(astr['sunrise'], '%I:%M %p')
	fall = datetime.strptime(astr['sunset'], '%I:%M %p')
	nrise = 60.0 * rise.hour + rise.minute
	nfall = 60.0 * fall.hour + fall.minute
	factor = math.pi / (nfall - nrise)
	now = datetime.fromtimestamp(time.time())
	nnow = 60.0 * now.hour + now.minute
	angle = factor * (nnow - nrise)
	nwake = 60.0 * _waketime[0] + _waketime[1]
	wangle = factor * (nwake - nrise)
	return (angle, wangle)


def kelvin_curve(theta):
	'''get a temp for an angle'''
	theta = min(max(theta, 0), math.pi)
	sintheta = math.sin(theta)
	kelvin = 1200 + 4500 * sintheta
	return kelvin


def brightness_curve(theta, phi):
	'''get a bri for an angle theta
			returns 0 if less than phi'''
	bri = 1
	if (theta < phi):
		bri = 0
	elif (theta < 0):
		beta = math.pi / phi
		bri = 0.5 + 0.5 * math.cos(beta * theta)
	elif ((theta > 0.875 * math.pi) and
	      (theta < 1.125 * math.pi)):
	  bri = 0.5 - 0.5 * math.cos(8.0 * theta)
	return int(bri*255)


def full_temp_to_xy(temp):
	'''temp to ciexy''' 
	global _ciexy
	if not _ciexy:
		t = []
		x = []
		y = []
		f = open('ciexy.txt')
		for l in f.readlines():
			ll = l.split(',')
			t.append(int(ll[0]))
			x.append(float(ll[1]))
			y.append(float(ll[2]))
		_ciexy = spline.linear(t,x,y)
	return _ciexy.f(temp)
		
		

def main():
	'''main method'''
	ya = get_weather(ev)
	if ya is None:
		return 'fail'
	today = ya['condition']
	tmrw = ya['forecasts']
	(yangle, wangle) = get_angle(ya)
	kel = kelvin_curve(yangle)
	print today['temp']+'c', today['text']
	print 'sun at %spi' % (yangle/math.pi)
	print 'wake at %spi' % (wangle/math.pi)
	print 'temp at %sK' % kel
	print full_temp_to_xy(kel)
	if get_br():
		bedr = get_br().get_light_objects('name')['bedroom']
		bedr.on = True
		bedr.brightness = brightness_curve(yangle, wangle)
		#bedr.colortemp_k = int(kel)
		xy = full_temp_to_xy(kel)
		bedr.xy = xy
		

if __name__ == "__main__": main()
