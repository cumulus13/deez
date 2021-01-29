#!/virtualenv/py-deezer/bin/python
import os
import sys

debug = False

if "-d" in sys.argv[1:] or "--debug" in sys.argv[1:]:
	DIR_NAME = os.path.dirname(r"/mnt/sda3/PROJECTSX/deez/deez_debug.py")
	try:
		debug = True
		sys.argv.remove('-d')
	except:
		pass
	try:
		debug = True
		sys.argv.remove('--debug')
	except:
		pass
else:	
	DIR_NAME = os.path.dirname(r"/mnt/sda3/PROJECTSX/deez/deez_release.py")

DIR_ROOT = os.path.dirname(DIR_NAME)

# if sys.platform == 'win32':
sys.path.insert(0, DIR_ROOT)
try:
	sys.path.remove(DIR_NAME)
except:
	pass
sys.path = list(set(sys.path))
print(sys.path)
# print("DIR_NAME =", DIR_NAME)
if debug:
	os.environ.update({'DEBUG':'1'})
	from deez.deez_debug import Deez
else:
	from deez.deez_release import Deez

c = Deez()
c.usage()

