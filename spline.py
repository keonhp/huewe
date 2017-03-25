import numpy as np


class linear:
	'''a 2d parametric linear interp'''
	def __init__(self, t, x, y):
		self._t = np.array(t)
		self._x = np.array(x)
		self._y = np.array(y)
		dx = []
		dy = []
		for i in range(self._t.size-1):
			dx.append((x[i+1]-x[i])/(t[i+1]-t[i]))
			dy.append((y[i+1]-y[i])/(t[i+1]-t[i]))
		self._dx = np.array(dx)
		self._dy = np.array(dy)
		
	def f(self, t):
		ind = np.searchsorted(self._t, t)
		if self._t[ind] == t:
			return (self._x[ind],self._y[ind])
		elif t < self._t[0]:
			return (self._x[0],self._y[0])
		elif ind == self._t.size:
			return (self._x[ind-1],self._y[ind-1])
		else:
			dt = t - self._t[ind-1]
			x = self._x[ind-1] + dt*self._dx[ind-1]
			y = self._y[ind-1] + dt*self._dy[ind-1]
			return [x,y]
		
		