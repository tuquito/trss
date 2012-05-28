#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Tuquito RSS
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

import ConfigParser
import gtk
import os, pynotify, gettext, gobject

# i18n
gettext.install('trss', '/usr/share/tuquito/locale')

# Lista de navegadores soportados
browsers = [None,'mozilla','firefox','netscape','galeon','epiphany','konqueror','opera','grail','links','lynx','w3m']
home = os.environ['HOME']

# Inicia Notificaciones
if not pynotify.init ('TRSS-PREF-Notify'):
	exit(1)

class Preferencias:
	def verificaStart(self):
		dr = home + '/.config/autostart/'
		if not os.path.exists(dr):
			os.system('mkdir -p ' + dr)
		configFile = dr + 'trss.desktop'
		line = []
		f = open(configFile, 'w')
		line.append('[Desktop Entry]\n')
		line.append('Name=Tuquito RSS\n')
		line.append('Comment=Notifier official Tuquito sites\n')
		line.append('Comment[en]=Notificador de los sitios oficiales de Tuquito\n')
		line.append('Comment[pt]=Notificador de eventos en los sitios oficiales de Tuquito GNU/Linux\n')
		line.append('Type=Application\n')
		line.append('Exec=trss\n')
		line.append('Icon=/usr/lib/tuquito/trss/trss.png\n')
		line.append('Terminal=false\n')
		line.append('Categories=Utility;\n')
		if self.startup == True:
			line.append('X-GNOME-Autostart-enabled=true')
		else:
			line.append('X-GNOME-Autostart-enabled=false')
		f.writelines(line)
		f.close

	def saveExit(self, widget, data=None):
		self.verificaStart()
		if self.universo:
			self.blog = False
			self.foros = False
			self.videos = False
			self.social = False
			self.identica = False
			self.twitter = False
			self.universo = True
		else:
			self.universo = False

		self.waitVal = self.spinner.get_value_as_int()
		self.saveConfig(self)
		self.notify(_('Your settings are saved correctly.\nYou must restart your session to ensure that changes are made'))
		gtk.main_quit()

	def initialConfig(self):
		if not os.path.exists(self.path):
			os.system('mkdir -p ' + self.path)
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
		config.write(open(self.configfile, 'w'))

	def saveConfig(self, widget):
		model = self.combobox.get_model()
		active = self.combobox.get_active()
		if active < 0:
			return None
		browser = model[active][0]
		self.browser = browser.lower()
		config = ConfigParser.ConfigParser()
		config.add_section("User settings")
		config.set("User settings", "blog", self.blog)
		config.set("User settings", "foros", self.foros)
		config.set("User settings", "videos", self.videos)
		config.set("User settings", "social", self.social)
		config.set("User settings", "identica", self.identica)
		config.set("User settings", "twitter", self.twitter)
		config.set("User settings", "universo", self.universo)
		config.set("User settings", "startup", self.startup)
		config.set("User settings", "traybar", self.traybar)
		config.set("User settings", "sound", self.sound)
		config.set("User settings", "browser", self.browser)
		config.set("User settings", "wait", self.waitVal)
		config.write(open(self.configfile, 'w'))

	def readConfig(self):
		try:
			config = ConfigParser.ConfigParser()
			config.read(self.configfile)
			self.blog = config.getboolean("User settings", "blog")
			self.foros = config.getboolean("User settings", "foros")
			self.videos = config.getboolean("User settings", "videos")
			self.social = config.getboolean("User settings", "social")
			self.identica = config.getboolean("User settings", "identica")
			self.twitter = config.getboolean("User settings", "twitter")
			self.universo = config.getboolean("User settings", "universo")
			self.startup = config.getboolean("User settings", "startup")
			self.traybar = config.getboolean("User settings", "traybar")
			self.sound = config.getboolean("User settings", "sound")
			browser = config.get("User settings", "browser")
			self.wait = config.get("User settings", "wait")
			self.browser = browser.strip()
			self.searchBrowser(self, browser)
		except:
			self.initialConfig()

	def searchBrowser(self, widget, data=None):
		import webbrowser
		i = 0
		model = gtk.ListStore(gobject.TYPE_STRING)
		for browser in browsers:
			if browser == data or browser == None:
				j = i
			try:
				webbrowser.get(browser)
			except:
				pass
			else:
				if browser == None:
					self.browser_title = 'Default'
				elif browser == 'mozilla':
					self.browser_title = 'Mozilla'
				elif browser == 'firefox':
					self.browser_title = 'Firefox'
				elif browser == 'netscape':
					self.browser_title = 'Netscape'
				elif browser == 'galeon':
					self.browser_title = 'Galeon'
				elif browser == 'epiphany':
					self.browser_title = 'Epiphany'
				elif browser == 'konqueror':
					self.browser_title = 'Konqueror'
				elif browser == 'opera':
					self.browser_title = 'Opera'
				elif browser == 'grail':
					self.browser_title = 'Grail'
				elif browser == 'links':
					self.browser_title = 'Links'
				elif browser == 'lynx':
					self.browser_title = 'Lynx'
				else:
					self.browser_title = 'W3M'
				model.append([self.browser_title])
				i += 1
		self.combobox.set_model(model)
		cell = gtk.CellRendererText()
		self.combobox.pack_start(cell, True)
		self.combobox.add_attribute(cell, 'text', 0)
		self.combobox.set_active(j)

	def __init__(self):
		self.path = os.path.join(home, '.tuquito/trss')
		self.configfile = os.path.join(self.path, 'config')
		self.blog = False
		self.foros = False
		self.videos = False
		self.social = False
		self.twitter = False
		self.identica = False
		self.universo = False
		self.startup = False
		self.traybar = False
		self.sound = False
		self.wait = 5

		self.glade = gtk.Builder()
		self.glade.add_from_file('/usr/lib/tuquito/trss/trss-pref.glade')
		self.window = self.glade.get_object('main-win')
		self.combobox = self.glade.get_object('navegadores')

		self.readConfig()

		self.adj = self.glade.get_object('adjust')
		self.adj.configure(float(self.wait), 1.0, 60.0, 1.0, 10.0, 0.0)
		self.spinner = self.glade.get_object('minutos')

		self.window.set_title(_('Preferences'))
		self.glade.get_object('sitios').set_label('<b>' + _('Places to go') + '</b>')
		self.glade.get_object('comporta').set_label('<b>' + _('Behavior') + '</b>')
		self.glade.get_object('tiempo').set_label('<b>' + _('Refresh') + '</b>')
		self.glade.get_object('navegador').set_label('<b>' + _('Select browser') + '</b>')

		self.glade.get_object('blog').set_active(self.blog)
		self.glade.get_object('blog').set_label(_('Tuquito Blog'))
		self.glade.get_object('foros').set_active(self.foros)
		self.glade.get_object('foros').set_label(_('Tuquito Forums'))
		self.glade.get_object('videos').set_active(self.videos)
		self.glade.get_object('videos').set_label(_('Tuquito Videos'))
		self.glade.get_object('social').set_active(self.social)
		self.glade.get_object('social').set_label(_('Social Tuquito'))
		self.glade.get_object('identica').set_active(self.identica)
		self.glade.get_object('identica').set_label(_('Tuquito Identi.ca'))
		self.glade.get_object('twitter').set_active(self.twitter)
		self.glade.get_object('twitter').set_label(_('Tuquito Twitter'))
		self.glade.get_object('universo').set_active(self.universo)
		self.glade.get_object('universo').set_label(_('Only Tuquito Universe (disable other)'))
		self.glade.get_object('inicio').set_active(self.startup)
		self.glade.get_object('inicio').set_label(_('Automatic start'))
		self.glade.get_object('icono').set_active(self.traybar)
		self.glade.get_object('icono').set_label(_('Show icon on the panel'))
		self.glade.get_object('sonido').set_active(self.sound)
		self.glade.get_object('sonido').set_label(_('Play sound alert'))

		self.glade.get_object('min').set_label(_('(minutes)'))

		self.glade.connect_signals(self)
		self.window.show()

	def quit(self, widget, data=None):
		gtk.main_quit()
		return True

	def togBlog(self, widget, data=None ):
		self.blog = widget.get_active()

	def togForos(self, widget, data=None ):
		self.foros = widget.get_active()

	def togVideos(self, widget, data=None ):
		self.videos = widget.get_active()

	def togSocial(self, widget, data=None ):
		self.social = widget.get_active()

	def togIdentica(self, widget, data=None ):
		self.identica = widget.get_active()

	def togTwitter(self, widget, data=None ):
		self.twitter = widget.get_active()

	def togUniverso(self, widget, data=None ):
		self.universo = widget.get_active()

	def togStartup(self, widget, data=None ):
		self.startup = widget.get_active()

	def togTray(self, widget, data=None ):
		self.traybar = widget.get_active()

	def togSound(self, widget, data=None ):
		self.sound = widget.get_active()

	def notify(self, text):
		if self.sound == True:
			os.system('play /usr/lib/tuquito/trss/pop.ogg')
		n = pynotify.Notification('Tuquito RSS', text, '/usr/lib/tuquito/trss/trss.png')
		n.show()

if __name__ == '__main__':
	win = Preferencias()
	gtk.main()
