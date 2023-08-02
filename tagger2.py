#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import traceback
from make_colors import make_colors
from pydebugger.debug import debug
from configset import configset
from xnotify.notify import notify
import mutagen
from unidecode import unidecode
import requests
from bs4 import BeautifulSoup as bs
import re
from pprint import pprint

try:
	from pause import pause
except:
	def pause(*args, **kwargs):
		return None

class Tagger(object):
	CONFIG = configset()
	debug(configset_configname = CONFIG.configname)
	notify.set_config(CONFIG.configname)
	EVENT = ['error', 'change', 'update', 'clean']
	notify.register('Tagger', EVENT, None, 20)
	ICON_ERROR = os.path.join(os.path.dirname(__file__), 'error.png')
	TAGS = {}


	def __init__(self, musicfile = None, configfile = None):
		super(Tagger, self)
		if configfile:
			self.CONFIG = configset(configfile)
		if musicfile:
			self.TAGS = self.get_tag(musicfile)
		if self.TAGS:
			_easytags = {}
			htmltag, _ = self.get_tag_html()
			debug(htmltag = htmltag, debug = True)
			debug(htmltag_keys = sorted(htmltag.keys()), debug = True)
			debug(self_TAGS_keys = sorted(self.TAGS.keys()), debug = True)
			same_tags1 = []
			same_tags2 = []
			for i in htmltag.keys():
				for t in self.TAGS.keys():
					if i in t:
						same_tags1.append(i)
						same_tags2.append(t)
			debug(same_tags1 = sorted(same_tags1), debug = True)
			debug(same_tags2 = sorted(same_tags2), debug = True)
			pause()
			for i in htmltag.keys():
				if not i in same_tags1:
					try:
						# getattr(self, htmltag.get(i), setattr(self, htmltag.get(i), getattr(mutagen.id3, i)()))
						setattr(self, htmltag.get(i), getattr(mutagen.id3, i)())
					except AttributeError:
						pass
					try:
						self.TAGS.update({htmltag.get(i) : getattr(mutagen.id3, i)()})
					except:
						pass
					if htmltag.get(i) == 'userdefinedurl' and i in same_tags1:
						setattr(self, 'url', getattr(mutagen.id3, i)())
						self.TAGS.update({'url' : getattr(mutagen.id3, i)()})
					elif htmltag.get(i) == 'grouping' and i in same_tags1:
						setattr(self, 'group', getattr(mutagen.id3, i)())
						self.TAGS.update({'group' : getattr(mutagen.id3, i)()})
					elif htmltag.get(i) == 'originalartist' and i in same_tags1:
						setattr(self, 'orgartist', getattr(mutagen.id3, i)())
						self.TAGS.update({'orgartist' : getattr(mutagen.id3, i)()})
					elif htmltag.get(i) == 'partofset' and i in same_tags1:
						setattr(self, 'disc', getattr(mutagen.id3, i)())
						self.TAGS.update({'disc' : getattr(mutagen.id3, i)()})
						setattr(self, 'cd', getattr(mutagen.id3, i)())
						self.TAGS.update({'cd' : getattr(mutagen.id3, i)()})
					elif htmltag.get(i) == 'popularimeter' and i in same_tags1:
						setattr(self, 'rating', getattr(mutagen.id3, i)())
						self.TAGS.update({'rating' : getattr(mutagen.id3, i)()})
					self.TAGS.save()
				else:
					try:
						print("i =", i)
						# self.TAGS.update({htmltag.get(i) : getattr(self.TAGS, same_tags2[same_tags1.index(i)])})
						self.TAGS.update({htmltag.get(i) : self.TAGS.get(same_tags2[same_tags1.index(i)])})
						setattr(self, htmltag.get(i), self.TAGS.get(same_tags2[same_tags1.index(i)]))
						# setattr(self, htmltag.get(i), getattr(self.TAGS, same_tags2[same_tag1.index(i)]))
					except:
						print("Tag Pass:", same_tags2[same_tags1.index(i)])
						traceback.format_exc()
					
					
					if htmltag.get(i) == 'userdefinedurl' and i in same_tags1:
						setattr(self, 'url', self.TAGS.get(same_tags2[same_tags1.index(i)]))
						self.TAGS.update({'url' : self.TAGS.get(same_tags2[same_tags1.index(i)])})
					elif htmltag.get(i) == 'grouping' and i in same_tags1:
						setattr(self, 'group', self.TAGS.get(same_tags2[same_tags1.index(i)]))
						self.TAGS.update({'group' : self.TAGS.get(same_tags2[same_tags1.index(i)])})
					elif htmltag.get(i) == 'originalartist' and i in same_tags1:
						setattr(self, 'orgartist', self.TAGS.get(same_tags2[same_tags1.index(i)]))
						self.TAGS.update({'orgartist' : self.TAGS.get(same_tags2[same_tags1.index(i)])})
					elif htmltag.get(i) == 'partofset' and i in same_tags1:
						setattr(self, 'disc', self.TAGS.get(same_tags2[same_tags1.index(i)]))
						self.TAGS.update({'disc' : self.TAGS.get(same_tags2[same_tags1.index(i)])})
						setattr(self, 'cd', self.TAGS.get(same_tags2[same_tags1.index(i)]))
						self.TAGS.update({'cd' : self.TAGS.get(same_tags2[same_tags1.index(i)])})
					elif htmltag.get(i) == 'popularimeter' and i in same_tags1:
						setattr(self, 'rating', self.TAGS.get(same_tags2[same_tags1.index(i)]))
						self.TAGS.update({'rating' : self.TAGS.get(same_tags2[same_tags1.index(i)])})
					
					_easytags.update({htmltag.get(i) : self.TAGS.get(same_tags2[same_tags1.index(i)])})
				
			APIC_FOUND = []
			for t in self.TAGS:
				if 'APIC:' in t:
					if not self.TAGS.get(t).data or len(self.TAGS.get(t).data) == 0 or len(self.TAGS.get(t).data) < 50:
						self.TAGS.pop(t)
						self.TAGS.save()
					else:
						APIC_FOUND.append([t, self.TAGS.get(t)])
			debug(len_APIC_FOUND = len(APIC_FOUND), debug = True)
			if len(APIC_FOUND) == 1:
				self.TAGS.update({'picture' : APIC_FOUND[0][1]})
				setattr(self, 'picture', APIC_FOUND[0][1])
				self.TAGS.update({'cover' : APIC_FOUND[0][1]})
				setattr(self, 'cover', APIC_FOUND[0][1])
			else:
				if len(APIC_FOUND) > 2:
					cover_name = ['cover', 'front', 'folder']
					for i in APIC_FOUND:
						for c in cover_name:
							if c in i[0]:
								self.TAGS.update({'picture' : i[1]})
								setattr(self, 'picture', i[1])
								self.TAGS.update({'cover' : i[1]})
								setattr(self, 'cover', i[1])
								self.TAGS.save()
								break
					try:
						if not self.picture.data:
							self.TAGS.update({'picture' : APIC_FOUND[0][1]})
							setattr(self, 'picture', APIC_FOUND[0][1])
							self.TAGS.update({'cover' : APIC_FOUND[0][1]})
							setattr(self, 'cover', APIC_FOUND[0][1])
					except:
						pass
			pause()			
						
			debug(self_TAGS_keys = self.TAGS.keys())
			setattr(self, "tags", self.TAGS)
			setattr(self, "easytags", _easytags)
			setattr(self, "as_dict", vars(self))

	@classmethod
	def as_dict(self):
		return vars(self)

	@classmethod
	def save(self):
		return self.TAGS.save()

	@classmethod
	def update(self, data):
		self.TAGS.update(data)

	@classmethod
	def get_tag_html(self):
		content = ''
		content = open(os.path.join(os.path.dirname(__file__), 'idv4.html'), 'r').read()
		if isinstance(content, bytes):
			content = content.decode('utf-8', errors="ignore")
		
		if not content:
			return {}
		b = bs(content, 'lxml')
		all_tr = b.find_all('tr')
		debug(all_tr = all_tr)
		data1 = {}
		data2 = {}
		for i in all_tr:
			debug(i = i, debug = True)
			all_td = i.find_all('td')
			debug(all_td = all_td)
			debug(key = all_td[0].text, debug = True)
			data1.update({
				re.sub("'", "", all_td[0].text) : all_td[1].text.lower()
			})
			data2.update({
				all_td[1].text.lower() : re.sub("'", "", all_td[0].text)
			})
		pause()
		debug(data1 = data1)
		debug(data2 = data2)
		data2.update({'cover':data2.get('picture')})
		data2.update({'url':data2.get('userdefinedurl')})
		data2.update({'album':data2.get('band')})
		data2.update({'group':data2.get('grouping')})
		data2.update({'orgartist':data2.get('originalartist')})
		data2.update({'disc':data2.get('partofset')})
		data2.update({'cd':data2.get('partofset')})
		data2.update({'rating':data2.get('popularimeter')})
		
		return data1, data2

	@classmethod
	def get_tag(self, musicfile):
		if not os.path.isfile(musicfile):
			print(make_colors("Music file not Found !", 'lw', 'lr'))
			notify.send('Tagger Error', "Music file not Found !", "error", iconpath = self.ICON_ERROR)
			sys.exit(1)

		tags = {}
		try:
			tags = mutagen.File(musicfile)
		except:
			print(make_colors("Invalid music file !", 'lw', 'r'))
			# sys.exit()
		self.TAGS = tags
		return tags

	@classmethod
	def get_artist(self, musicfile = None):
		tag = {}
		if musicfile:
			tags = self.get_tag(musicfile)
		else:
			if self.TAGS:
				tags = self.TAGS
			
		return tags.get()

	@classmethod
	def usage(self):
		parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
		parser.add_argument('-sa', '--licface', action = 'store_true')
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			pass

if __name__ == '__main__':
	# data1, data2 = Tagger.get_tag_html()
	# t = Tagger(r"/tmp/01. Never Back Down.mp3")
	t = Tagger(r"/projects/01. Bonds  - Unbroken (feat. Ty Tabor, Brian Tichy).mp3")
	d = vars(t)
	# pprint(d)
	pprint(t.as_dict.keys())
	# t.compilation.text = "https://www.google.com"
	# t.save()
	# print(t.artist)
	# print("artist =", t.artist)
	# print(dir(t.artist))
	# print(type(t.artist))
	# print(t.media)
	# print(t.get('artist'))
	# t.album.text = "TEST"
	# t.save()

	# print("time =", t.time)
	# t.time.text = "2020"
	# t.save()
	# print("lyrics =", t.lyrics)
	# t.lyrics.text = "2030"
	# t.lyrics.lang = "XXX"
	# t.save()
	# print("lyrics =", t.lyrics)
	# print("time =", t.time)
	# print("compilation =", t.compilation)
	# print("album =", t.album)
	# print("album =", t.band)
	# print("comment =", t.comment)
	# print("CD =", t.partofset)
	# print(dir(t.others.get('comment')))
	# print("URL =", t.userdefinedurl)
	# print(t.picture)
	# print(t.as_dict.keys())
	# print(t.easytags.keys())
	pause()
	np = 1
	for i in sorted(t.tags.keys()):
		if i == 'picture' or 'APIC' in i or 'cover' in i:
			print(str(np) + ". ", i, "=", len(t.tags.get(i).data))
			np+=1
		else:
			print(i, "=", t.tags.get(i))
	

