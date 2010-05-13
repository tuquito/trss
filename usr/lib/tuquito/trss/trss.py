#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Tuquito RSS 1.2
 Copyright (C) 2010
 Author: Mario Colque <mario@tuquito.org.ar>
 Tuquito Team! - www.tuquito.org.ar

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; version 3 of the License.
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
"""

import ConfigParser, feedparser
import gtk, pygame, pynotify
import os, time, webbrowser, gettext
import socket
socket.setdefaulttimeout(10)
from urllib2 import urlopen

# i18n
gettext.install('trss', '/usr/share/tuquito/locale')

# Inicia Notificaciones
if not pynotify.init ('TRSS-Notify'):
	exit(1)

#-Variables
home = os.environ['HOME']
icon = ['/usr/lib/tuquito/trss/trss-off.png', '/usr/lib/tuquito/trss/trss.png']
default_sound = '/usr/share/sounds/trss-pop.ogg'
home_dir = home + '/.trss/'
configfile = home_dir + 'config'
flag = False
flagC = False
flagS = True #flag de sonido
flagB = True #flag de crear botonera

class Trss:
	def hideWindow(self, widget, data=None):
		global flag
		flag = False
		self.window.hide()
		return True

	def showWeb(self, widget, link=None):
		global browser
		b = webbrowser.get(browser)
		b.open(link)

	def showList(self, data=None):
		global flagC
		if flagC == True:
			self.window.show_all()

	def insertLink(self, web, title, link):
		global flagB
		text = web + ' | ' + title
		if len(text) > 65:
			text = text[:65] + '... '
		if flagB:
			self.botonera1 = gtk.VBox(False, 0)
			self.botonera.pack_end(self.botonera1)
			flagB = False
		self.button = gtk.Button(text)
		self.button.connect('clicked', self.showWeb, link)
		self.botonera1.pack_end(self.button)

	def clean(self, widget, data=None):
		global flagB
		flagB = True
		self.botonera1.destroy()
		self.hideWindow(self)

	# Menu
	def setTooltip(self, text):
		self.staticon.set_tooltip(text)

	def setBlinking(self, data):
		self.staticon.set_blinking(data)

	def setIcon(self, error):
		if error == False:
			self.staticon.set_from_file(icon[0])
		else:
			self.staticon.set_from_file(icon[1])

	def activate(self, widget, data=None):
		global flag, flagC
		self.setBlinking(False)
		self.setTooltip(_('Conectado'))
		if flag == False:
			self.showList()
			flag = True
		else:
			self.window.hide()
			flag = False
		if flagC == False:
			notify('Tuquito RSS', _('No hay eventos nuevos'))

	def submenu(self, widget, button, time, data=None):
		if button == 3:
			if data:
				data.show_all()
				data.popup(None, None, None, 3, time)
		pass

	def openURL(self, widget, data=None):
		global browser
		b = webbrowser.get(browser)
		b.open(data)

	def refresh(self, widget):
		global wait
		tm.tempor = int(100 * 60 * wait)

	def addFont(self,widget,data=None):
		os.system('/usr/lib/tuquito/trss/trss-fonts.py &')

	def showPref(self, widget, data=None):
		os.system('/usr/lib/tuquito/trss/trss-pref.py &')

	def about(self, widget, data=None):
		os.system('/usr/lib/tuquito/trss/trss-about.py &')

	def __init__(self):
		global traybar
		self.glade = gtk.Builder()
		self.glade.add_from_file('/usr/lib/tuquito/trss/trss.glade')
		self.window = self.glade.get_object('trss')
		self.staticon = self.glade.get_object('statusicon')
		self.menu = self.glade.get_object('menu')
		self.botonera = self.glade.get_object('botonera')
		self.glade.connect_signals(self)

		menuItem=gtk.ImageMenuItem(gtk.STOCK_REDO)
		menuItem.get_children()[0].set_label(_('Ir a Blog Tuquito'))
		menuItem.connect('activate', self.openURL, 'http://blog.tuquito.org.ar')
		self.menu.append(menuItem)

		menuItem=gtk.ImageMenuItem(gtk.STOCK_REDO)
		menuItem.get_children()[0].set_label(_('Ir a Foros Tuquito'))
		menuItem.connect('activate', self.openURL, 'http://foros.tuquito.org.ar')
		self.menu.append(menuItem)

		menuItem=gtk.ImageMenuItem(gtk.STOCK_REDO)
		menuItem.get_children()[0].set_label(_('Ir a Tuquito Videos'))
		menuItem.connect('activate', self.openURL, 'http://videos.tuquito.org.ar')
		self.menu.append(menuItem)

		menuItem=gtk.ImageMenuItem(gtk.STOCK_REDO)
		menuItem.get_children()[0].set_label(_('Ir a Tuquito Social'))
		menuItem.connect('activate', self.openURL, 'http://tuquito.ning.com')
		self.menu.append(menuItem)

		menuItem=gtk.ImageMenuItem(gtk.STOCK_REDO)
		menuItem.get_children()[0].set_label(_('Ir a Universo Tuquito'))
		menuItem.connect('activate', self.openURL, 'http://universo.tuquito.org.ar')
		self.menu.append(menuItem)

		menuItem=gtk.ImageMenuItem(gtk.STOCK_REDO)
		menuItem.get_children()[0].set_label(_('Ir a Twitter Tuquito'))
		menuItem.connect('activate', self.openURL, 'http://twitter.com/tuquitolinux')
		self.menu.append(menuItem)

		menuItem=gtk.ImageMenuItem(gtk.STOCK_REDO)
		menuItem.get_children()[0].set_label(_('Ir a Identi.ca Tuquito'))
		menuItem.connect('activate', self.openURL, 'http://identi.ca/tuquito')
		self.menu.append(menuItem)

		separator = gtk.SeparatorMenuItem()
		self.menu.append(separator)

		menuItem=gtk.ImageMenuItem(gtk.STOCK_REFRESH)
		menuItem.get_children()[0].set_label(_('Actualizar lista'))
		menuItem.connect('activate', self.refresh)
		self.menu.append(menuItem)

		menuItem=gtk.ImageMenuItem(gtk.STOCK_ADD)
		menuItem.get_children()[0].set_label(_('Editar fuentes RSS'))
		menuItem.connect('activate', self.addFont)
		self.menu.append(menuItem)

		menuItem=gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
		menuItem.get_children()[0].set_label(_('Preferencias'))
		menuItem.connect('activate', self.showPref)
		self.menu.append(menuItem)

		separator = gtk.SeparatorMenuItem()
		self.menu.append(separator)

		menuItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
		menuItem.connect('activate', self.about)
		self.menu.append(menuItem)


		menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		menuItem.connect('activate', self.quit, self.staticon)
		self.menu.append(menuItem)

		self.setTooltip(_('Conectando...'))
		self.setBlinking(False)
		self.staticon.connect('activate', self.activate)
		self.staticon.connect('popup_menu', self.submenu, self.menu)
		self.staticon.set_visible(traybar)

	def quit(self, widget, data=None):
		if data:
			data.set_visible = False
		exit(0)

class Tempo:
    def get_time(self):
	return self.tempor
    def __init__(self):
	global wait
	self.timer = int(wait * 60 * 100)
	self.tempor = self.timer - (30 * 100)
    def run(self):
	self.tempor += 1
	if self.tempor > self.timer:
		self.tempor = 0
	time.sleep(0.01)

def notify(title, text, icon=icon[1]):
	if flagS == True:
		pygame.mixer.music.play()
	n = pynotify.Notification(title, text, icon)
	n.show()

def initialConfig():
	if not os.path.exists(home_dir):
		os.mkdir(home_dir)
	config = ConfigParser.ConfigParser()
	config.add_section("User settings")
	config.set("User settings", "blog", 'YES')
	config.set("User settings", "foros", 'YES')
	config.set("User settings", "videos", 'NO')
	config.set("User settings", "social", 'YES')
	config.set("User settings", "twitter", 'NO')
	config.set("User settings", "identica", 'YES')
	config.set("User settings", "universo", 'NO')
	config.set("User settings", "startup", 'YES')
	config.set("User settings", "traybar", 'YES')
	config.set("User settings", "sound", 'YES')
	config.set("User settings", "browser", 'default')
	config.set("User settings", "wait", 5)
	config.write(open(configfile, 'w'))
	readConfig()

def readConfig():
	global traybar, flagS, wait, browser, urls
	if os.path.isfile(configfile):
		try:
			config = ConfigParser.ConfigParser()
			config.read(configfile)
		except:
			os.remove(configfile)
			initialConfig()
		else:
			blog = config.get("User settings", "blog")
			foros = config.get("User settings", "foros")
			videos = config.get("User settings", "videos")
			social = config.get("User settings", "social")
			twitter = config.get("User settings", "twitter")
			identica = config.get("User settings", "identica")
			universo = config.get("User settings", "universo")
			traybarVal = config.get("User settings", "traybar")
			soundVal = config.get("User settings", "sound")
			browser = config.get("User settings", "browser")
			wait = float(config.get("User settings", "wait"))
			urls = []

			if blog == 'YES':
				urls.append(['Blog Tuquito', 'http://blog.tuquito.org.ar/feed/'])
			if twitter == 'YES':
				urls.append(['Twitter Tuquito', 'http://twitter.com/statuses/user_timeline/59312277.rss'])
			if foros == 'YES':
				urls.append(['Foros Tuquito', 'http://foros.tuquito.org.ar/rss.php'])
			if social == 'YES':
				urls.append(['Tuquito Social', 'http://tuquito.ning.com/activity/log/list?fmt=rss'])
			if videos == 'YES':
				urls.append(['Tuquito Videos', 'http://videos.tuquito.org.ar/index.php/feed/'])
			if identica == 'YES':
				urls.append(['Identi.ca Tuquito', 'http://identi.ca/api/statuses/user_timeline/tuquito.atom'])
			if universo == 'YES':
				urls.append(['Universo Tuquito', 'http://universo.tuquito.org.ar/index.php?media=atom'])

			if browser == 'default':
				browser = None
			if traybarVal == 'YES':
				traybar = True
			elif traybarVal == 'NO':
				traybar = False
			if soundVal == 'YES':
				flagS = True
			elif soundVal == 'NO':
				flagS = False
	else:
		initialConfig()

def readFonts():
	user_fonts = home_dir + 'userFonts'
	if os.path.isfile(user_fonts):
		f = open(user_fonts, 'r')
		g = f.readlines()
		f.close()
		for stri in g:
			dat = stri.split('|')
			fon = dat[0].strip()
			web = dat[1].strip()
			urls.append([fon, web])

def readMem(fon):
	global path, mem, home_dir
	path = home_dir + fon
	try:
		f = open(path, 'r')
		g = f.readlines()
		f.close()
		mem = str(g[0].strip())
	except:
		mem = 0

def conect(web):
	global conec, info
	tab.setTooltip(_('Conectando...'))
	try:
		urlopen(web)
		info = feedparser.parse(web)
		tab.setIcon(True)
		tab.setTooltip(_('Conectado'))
		conec = True
	except Exception, detail:
		#print detail
		tab.setIcon(False)
		tab.setTooltip(_('Sin conexion'))
		conec = False

pygame.init()
pygame.mixer.music.load(default_sound)
readConfig()
readFonts()
tab = Trss()
tm = Tempo()
while True:
	tm.run()
	while gtk.events_pending():
		gtk.main_iteration()
	if  tm.get_time() == int(wait * 60 * 100):
		for url in urls:
			web = url[1]
			fon = url[0]
			conect(web)
			if conec:
				cant = 0
				readMem(fon)
				numEntries = len(info.entries)

				try:
					last = str(info.entries[0].link)
				except IndexError:
					break

				if last != mem:
					f = open(path, 'w')
					f.write(last)
					f.close()

				if fon == 'Tuquito Social':
					linkHome = 'http://tuquito.ning.com'
				elif fon == 'Blog Tuquito':
					linkHome = 'http://blog.tuquito.org.ar'
				elif fon == 'Foros Tuquito':
					linkHome = 'http://foros.tuquito.org.ar'
				elif fon == 'Tuquito Videos':
					linkHome = 'http://videos.tuquito.org.ar'
				elif fon == 'Twitter Tuquito':
					linkHome = 'http://twitter.com/tuquitolinux'
				elif fon == 'Identi.ca Tuquito':
					linkHome = 'http://identi.ca/tuquito'
				elif fon == 'Universo Tuquito':
					linkHome = 'http://universo.tuquito.org.ar'
				else:
					linkHome = info.feed.link

				if mem == 0:
					tab.setBlinking(True)
					text = _('Hay ') + str(numEntries) + _(' entradas nuevas')
					tab.setTooltip(_('Hay Novedades'))
					tab.insertLink(fon, text, linkHome)
					notify(fon, text)
					flagC = True
				else:
					lasts = []
					for entrie in info.entries:
						data = []
						title = entrie.title.encode('utf-8')
						link = entrie.link
						if link != mem:
							data.append(title)
							data.append(link)
							lasts.append(data)
							cant += 1
						else:
							break

					if cant > 0:
						if flag:
							tab.window.hide()
							flag = False
						flagC = True
						tab.setBlinking(True)
						tab.setTooltip(_('Hay Novedades'))
						if cant > 3:
							text = _('Hay ') + str(cant) +  _(' entradas nuevas')
							tab.insertLink(fon, text, linkHome)
							notify(fon, text)
						else:
							lasts.reverse()
							for tit in lasts:
								text = tit[0].encode('utf-8')
								link = tit[1]
								notify(fon, text)
								tab.insertLink(fon, text, link)
