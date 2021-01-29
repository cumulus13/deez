#!/usr/bin/env python
from configset import configset
import time
from make_colors import make_colors
from pydebugger.debug import debug
import os

configname = None
conf = configset(configname)
def sleep(option='sleep', section='time', SL=None):
	SM = 0
	n = 0
	if SL:
		ST = SL
		conf.write_config(option, section, str(SL))
	else:
		ST = conf.get_config(option, section, '10')
	while 1:
		if not SM == conf.get_config(option	, section, '10'):
			ST = conf.get_config(option	, section, '10')
			SM = ST
			n  = 0
		debug(ST = ST)
		if os.getenv('DEBUG'):
			print(make_colors("SLEEP:", 'lw', 'lr') + " " + make_colors("1 from {}".format(str(ST - n)), 'lw', 'bl'))
		time.sleep(1)
		if ST == n or n > ST:
			break
		debug(n = n)
		n += 1
		debug(n = n)

if __name__ == '__main__':
	sleep()

