#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Tuquito RSS 1.3
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
import gtk, pynotify
import os, time, sys
import webbrowser, gettext
import socket, threading
socket.setdefaulttimeout(10)
from urllib2 import urlopen

# i18n
gettext.install('trss', '/usr/share/tuquito/locale')

# Inicia Notificaciones
if not pynotify.init ('TRSS-Notify'):
	sys.exit(1)

# Variables
home = os.environ['HOME']
icon = ['/usr/lib/tuquito/trss/trss-off.png', '/usr/lib/tuquito/trss/trss.png']
default_sound = '/usr/lib/tuquito/trss/pop.ogg'
home_dir = os.path.join(home, '.tuquito/trss')
configfile = os.path.join(home_dir, 'config')
showWindow = False
force_reload = False
flagC = False
flagB = True #flag de crear botonera
proxy = None

gtk.gdk.threads_init()

class Trss(threading.Thread):
	def __init__(self, glade):
		threading.Thread.__init__(self)
		self.glade = glade
		self.window = self.glade.get_object('trss')
		self.staticon = self.glade.get_object('statusicon')

	def readMem(self, fon):
		self.path = os.path.join(home_dir, fon)
		try:
			f = open(self.path, 'r')
			g = f.readlines()
			f.close()
			self.mem = str(g[0].strip())
		except:
			self.mem = 0
	def checkConnection(self):
		gtk.gdk.threads_enter()
		self.staticon.set_tooltip(_('Checking the connection to the Internet...'))
		gtk.gdk.threads_leave()
		try:
			url = urlopen('http://google.com', None, proxy)
			url.read()
			url.close()
		except Exception, detail:
			if os.system('ping http://google.com -c1 -q'):
				setIcon(False)
				gtk.gdk.threads_enter()
				self.staticon.set_tooltip(_('Could not connect to the Internet'))
				gtk.gdk.threads_leave()
				autoRefresh = AutomaticRefreshThread(self.glade, False)
				autoRefresh.start()
				return False
		else:
			gtk.gdk.threads_enter()
			setIcon(True)
			self.staticon.set_tooltip(_('Connected'))
			gtk.gdk.threads_leave()
			return True

	def conect(self, web, font):
		try:
			gtk.gdk.threads_enter()
			self.staticon.set_tooltip(_('Searching news in %s...') % font)
			gtk.gdk.threads_leave()
			urlopen(web, None, proxy)
			self.info = feedparser.parse(web)
			self.conec = True
		except:
			self.conec = False

	def run(self):
		global showWindow, flagC, force_reload
		if self.checkConnection():
			for url in urls:
				fon, web = url
				print fon
				self.conect(web, fon)
				if self.conec:
					cant = 0
					self.readMem(fon)
					numEntries = len(self.info.entries)

					try:
						last = str(self.info.entries[0].link)
					except IndexError:
						break

					if last != self.mem:
						f = open(self.path, 'w')
						f.write(last)
						f.close()

					if fon == _('Social Tuquito'):
						linkHome = 'http://social.tuquito.org.ar'
					elif fon == _('Tuquito Blog'):
						linkHome = 'http://blog.tuquito.org.ar'
					elif fon == _('Tuquito Forums'):
						linkHome = 'http://foros.tuquito.org.ar'
					elif fon == _('Tuquito Videos'):
						linkHome = 'http://videos.tuquito.org.ar'
					elif fon == _('Tuquito Twitter'):
						linkHome = 'http://twitter.com/tuquitolinux'
					elif fon == _('Tuquito Identi.ca'):
						linkHome = 'http://identi.ca/tuquito'
					elif fon == _('Tuquito Universe'):
						linkHome = 'http://universo.tuquito.org.ar'
					else:
						linkHome = self.info.feed.link

					if self.mem == 0:
						gtk.gdk.threads_enter()
						self.staticon.set_blinking(True)
						self.staticon.set_tooltip(_('There news!'))
						gtk.gdk.threads_leave()
						text = _('There are %s new entries') % str(numEntries)
						insertLink(fon, text, linkHome)
						notify(fon, text)
						flagC = True
					else:
						lasts = []
						for entrie in self.info.entries:
							data = []
							title = entrie.title.encode('utf-8')
							link = entrie.link
							if link != self.mem:
								data.append(title)
								data.append(link)
								lasts.append(data)
								cant += 1
							else:
								break
						if cant > 0:
							if showWindow:
								self.window.hide()
								showWindow = False
							flagC = True
							gtk.gdk.threads_enter()
							self.staticon.set_blinking(True)
							self.staticon.set_tooltip(_('There news!'))
							gtk.gdk.threads_leave()
							if cant > 3:
								text = _('There are %s new entries') % str(cant)
								insertLink(fon, text, linkHome)
								notify(fon, text)
							else:
								lasts.reverse()
								for tit in lasts:
									text = tit[0].encode('utf-8')
									link = tit[1]
									notify(fon, text)
									insertLink(fon, text, link)
						else:
							gtk.gdk.threads_enter()
							self.staticon.set_tooltip(_('Connected'))
							gtk.gdk.threads_leave()
			force_reload = False
			autoRefresh = AutomaticRefreshThread(self.glade)
			autoRefresh.start()
		if flagC:
			showWindow = False

class AutomaticRefreshThread(threading.Thread):
	def __init__(self, glade, connectStatus=True):
		threading.Thread.__init__(self)
		self.glade = glade
		self.connectStatus = connectStatus

	def run(self):
		if self.connectStatus and int(wait) > 0:
			timer = int(wait * 60)
		else:
			timer = 60
		time.sleep(timer)
		if not showWindow and not force_reload:
			refresh = Trss(self.glade)
			refresh.start()

def notify(title, text, icon=icon[1]):
	if sound:
		os.system('play ' + default_sound + ' &')
	n = pynotify.Notification(title, text, icon)
	n.show()

def initialConfig():
	if not os.path.exists(home_dir):
		os.system('mkdir -p ' + home_dir)
	config = ConfigParser.ConfigParser()
	config.add_section("User settings")
	config.set("User settings", "blog", True)
	config.set("User settings", "foros", True)
	config.set("User settings", "videos", False)
	config.set("User settings", "social", True)
	config.set("User settings", "twitter", True)
	config.set("User settings", "identica", False)
	config.set("User settings", "universo", False)
	config.set("User settings", "startup", True)
	config.set("User settings", "traybar", True)
	config.set("User settings", "sound", True)
	config.set("User settings", "browser", 'default')
	config.set("User settings", "wait", 5)
	config.write(open(configfile, 'w'))
	readConfig()

def readConfig():
	global traybar, sound, wait, browser, urls
	if os.path.exists(configfile):
		try:
			config = ConfigParser.ConfigParser()
			config.read(configfile)
		except:
			initialConfig()
		else:
			blog = config.getboolean("User settings", "blog")
			foros = config.getboolean("User settings", "foros")
			videos = config.getboolean("User settings", "videos")
			social = config.getboolean("User settings", "social")
			twitter = config.getboolean("User settings", "twitter")
			identica = config.getboolean("User settings", "identica")
			universo = config.getboolean("User settings", "universo")
			traybar = config.getboolean("User settings", "traybar")
			sound = config.getboolean("User settings", "sound")
			browser = config.get("User settings", "browser")
			wait = config.getfloat("User settings", "wait")
			urls = []

			if blog:
				urls.append([_('Tuquito Blog'), 'http://blog.tuquito.org.ar/feed/'])
			if twitter:
				urls.append([_('Tuquito Twitter'), 'http://twitter.com/statuses/user_timeline/59312277.rss'])
			if foros:
				urls.append([_('Tuquito Forums'), 'http://foros.tuquito.org.ar/rss.php'])
			if social:
				urls.append([_('Social Tuquito'), 'http://social.tuquito.org.ar/activity/log/list?fmt=rss'])
			if videos:
				urls.append([_('Tuquito Videos'), 'http://videos.tuquito.org.ar/index.php/feed/'])
			if identica:
				urls.append([_('Tuquito Identi.ca'), 'http://identi.ca/api/statuses/user_timeline/tuquito.atom'])
			if universo:
				urls.append([_('Tuquito Universe'), 'http://universo.tuquito.org.ar/index.php?media=atom'])

			if browser == 'default':
				browser = None
	else:
		initialConfig()

def readFonts():
	user_fonts = os.path.join(home_dir, 'userFonts')
	if os.path.isfile(user_fonts):
		f = open(user_fonts, 'r')
		g = f.readlines()
		f.close()
		for stri in g:
			dat = stri.split('|')
			fon = dat[0].strip()
			web = dat[1].strip()
			urls.append([fon, web])

# Menu
def setIcon(error):
	if error == False:
		staticon.set_from_file(icon[0])
	else:
		staticon.set_from_file(icon[1])

def activate(widget, data=None):
	global showWindow, flagC
	staticon.set_blinking(False)
	staticon.set_tooltip(_('Connected'))
	if not flagC:
		notify('Tuquito RSS', _('There are no new events'))
	if not showWindow:
		showList()
		showWindow = True
	else:
		window.hide()
		showWindow = False
		return True

def submenu(widget, button, time, data=None):
	if button == 3:
		if data:
			data.show_all()
			data.popup(None, None, None, 3, time)

def openURL(widget, data=None):
	b = webbrowser.get(browser)
	b.open(data)

def refresh(widget):
	global force_reload
	force_reload = True
	refresh = Trss(glade)
	refresh.start()

def addFont(widget, data=None):
	os.system('/usr/lib/tuquito/trss/trss-fonts.py &')

def showPref(widget, data=None):
	os.system('/usr/lib/tuquito/trss/trss-pref.py &')

def about(widget, data=None):
	os.system('/usr/lib/tuquito/trss/trss-about.py &')

def showList(widget=None):
	if flagC:
		window.show_all()

def hideWindow(widget, data=None):
	global showWindow
	showWindow = False
	window.hide()
	return True

def showWeb(widget, link=None):
	global browser
	b = webbrowser.get(browser)
	b.open(link)

def insertLink(web, title, link):
	global flagB, botonera1
	text = web + ' | ' + title
	if len(text) > 75:
		text = text[:75] + '... '
	if flagB:
		botonera1 = gtk.VBox(False, 0)
		botonera.pack_end(botonera1)
		flagB = False
	button = gtk.Button(text)
	button.connect('clicked', showWeb, link)
	button.set_alignment(0.0, 0.0)
	botonera1.pack_end(button)
	botonera1.show()

def clean(widget, data=None):
	global flagB, flagC
	flagB = True
	flagC = False
	botonera1.destroy()
	hideWindow(None)

def quit(widget, data=None):
	os.system('kill -9 ' + str(os.getpid()))

readConfig()
readFonts()

try:
	arg = sys.argv[1].strip()
except:
	arg = False

if arg != False:
	if startup:
		if arg == 'time':
			time.sleep(wait)
	else:
		sys.exit(0)

try:
	glade = gtk.Builder()
	glade.add_from_file('/usr/lib/tuquito/trss/trss.glade')
	window = glade.get_object('trss')
	staticon = glade.get_object('statusicon')
	menu = glade.get_object('menu')
	botonera = glade.get_object('botonera')
	window.set_title(_('Tuquito RSS'))
	window.connect('delete_event', hideWindow)
	glade.get_object('clean').connect('clicked', clean)

	menuItem=gtk.ImageMenuItem(gtk.STOCK_REFRESH)
	menuItem.get_children()[0].set_label(_('Refresh list'))
	menuItem.connect('activate', refresh)
	menu.append(menuItem)

	menuItem=gtk.ImageMenuItem(gtk.STOCK_ADD)
	menuItem.get_children()[0].set_label(_('Edit RSS feeds'))
	menuItem.connect('activate', addFont)
	menu.append(menuItem)

	menuItem=gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
	menuItem.connect('activate', showPref)
	menu.append(menuItem)

	menuItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
	menuItem.connect('activate', about)
	menu.append(menuItem)

	separator = gtk.SeparatorMenuItem()
	menu.append(separator)

	menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
	menuItem.connect('activate', quit)
	menu.append(menuItem)

	staticon.connect('activate', activate)
	staticon.connect('popup_menu', submenu, menu)
	staticon.set_tooltip(_('Connecting...'))
	staticon.set_visible(traybar)
	trss = Trss(glade)
	trss.start()
	gtk.main()
except:
	sys.exit(1)
