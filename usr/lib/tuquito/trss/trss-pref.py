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

import ConfigParser
import gtk, pygtk, pygame
pygtk.require('2.0')
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
			os.mkdir(dr)
		configFile = dr + 'trss.desktop'
		line = []
		f = open(configFile, 'w')
		line.append('[Desktop Entry]\n')
		line.append('Name=Tuquito RSS\n')
		line.append('Comment=Notificador de eventos en los sitios oficiales de Tuquito GNU/Linux\n')
		line.append('Comment[en]=Notificador de eventos en los sitios oficiales de Tuquito GNU/Linux\n')
		line.append('Comment[fr]=Notificador de eventos en los sitios oficiales de Tuquito GNU/Linux\n')
		line.append('Comment[it]=Notificador de eventos en los sitios oficiales de Tuquito GNU/Linux\n')
		line.append('Comment[pt]=Notificador de eventos en los sitios oficiales de Tuquito GNU/Linux\n')
		line.append('Comment[pt_BR]=Notificador de eventos en los sitios oficiales de Tuquito GNU/Linux\n')
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

		if self.blog:
			self.blog = 'YES'
		else:
			self.blog = 'NO'

		if self.foros:
			self.foros = 'YES'
		else:
			self.foros = 'NO'

		if self.videos:
			self.videos = 'YES'
		else:
			self.videos = 'NO'

		if self.social:
			self.social = 'YES'
		else:
			self.social = 'NO'

		if self.twitter:
			self.twitter = 'YES'
		else:
			self.twitter = 'NO'

		if self.identica:
			self.identica = 'YES'
		else:
			self.identica = 'NO'

		if self.startup:
			self.startupVal = 'YES'
		else:
			self.startupVal = 'NO'

		if self.traybar:
			self.traybarVal = 'YES'
		else:
			self.traybarVal = 'NO'

		if self.sound:
			self.soundVal = 'YES'
		else:
			self.soundVal = 'NO'

		if self.universo:
			self.blog = 'NO'
			self.foros = 'NO'
			self.videos = 'NO'
			self.social = 'NO'
			self.identica = 'NO'
			self.twitter = 'NO'
			self.universo = 'YES'
		else:
			self.universo = 'NO'
			
		self.waitVal = self.spinner.get_value_as_int()
		self.saveConfig(self)
		self.notify(_('Sus configuraciones se guardaron correctamente') + '\n' + _('Debe reiniciar su sesion para que se efectuen los cambios'))
		gtk.main_quit()

	def initialConfig(self):
		if not os.path.exists(self.path):
			os.mkdir(self.path)
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
		config.set("User settings", "startup", self.startupVal)
		config.set("User settings", "traybar", self.traybarVal)
		config.set("User settings", "sound", self.soundVal)
		config.set("User settings", "browser", self.browser)
		config.set("User settings", "wait", self.waitVal)
		config.write(open(self.configfile, 'w'))

	def readConfig(self):
		try:
			config = ConfigParser.ConfigParser()
			config.read(self.configfile)
			followBlog = config.get("User settings", "blog")
			followForos = config.get("User settings", "foros")
			followVideos = config.get("User settings", "videos")
			followSocial = config.get("User settings", "social")
			followIdentica = config.get("User settings", "identica")
			followTwitter = config.get("User settings", "twitter")
			followUniverso = config.get("User settings", "universo")
			startupVal = config.get("User settings", "startup")
			traybarVal = config.get("User settings", "traybar")
			soundVal = config.get("User settings", "sound")
			browser = config.get("User settings", "browser")
			self.wait = config.get("User settings", "wait")
			self.browser = browser.strip()

			if followBlog == 'YES':
				self.blog = True
			elif followBlog == 'NO':
				self.blog = False

			if followForos == 'YES':
				self.foros = True
			elif followForos == 'NO':
				self.foros = False

			if followVideos == 'YES':
				self.videos = True
			elif followVideos == 'NO':
				self.videos = False

			if followSocial == 'YES':
				self.social = True
			elif followSocial == 'NO':
				self.social = False

			if followIdentica == 'YES':
				self.identica = True
			elif followIdentica == 'NO':
				self.identica = False

			if followTwitter == 'YES':
				self.twitter = True
			elif followTwitter == 'NO':
				self.twitter = False

			if followUniverso == 'YES':
				self.universo = True
			elif followUniverso == 'NO':
				self.universo = False

			if startupVal == 'YES':
				self.startup = True
			elif startupVal == 'NO':
				self.startup = False

			if traybarVal == 'YES':
				self.traybar = True
			elif traybarVal == 'NO':
				self.traybar = False

			if soundVal == 'YES':
				self.sound = True
			elif soundVal == 'NO':
				self.sound = False

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
		self.path = home + '/.trss/'
		self.configfile = self.path + 'config'
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

		self.window.set_title(_('Preferencias'))
		self.glade.get_object('sitios').set_label('<b>' + _('Sitios a seguir') + '</b>')
		self.glade.get_object('comporta').set_label('<b>' + _('Comportamiento') + '</b>')
		self.glade.get_object('tiempo').set_label('<b>' + _('Tiempo de refresco') + '</b>')
		self.glade.get_object('navegador').set_label('<b>' + _('Seleccionar navegadores') + '</b>')

		self.glade.get_object('blog').set_active(self.blog)
		self.glade.get_object('blog').set_label(_('Blog Tuquito'))
		self.glade.get_object('foros').set_active(self.foros)
		self.glade.get_object('foros').set_label(_('Foros Tuquito'))
		self.glade.get_object('videos').set_active(self.videos)
		self.glade.get_object('videos').set_label(_('Videos Tuquito'))
		self.glade.get_object('social').set_active(self.social)
		self.glade.get_object('social').set_label(_('Tuquito Social'))
		self.glade.get_object('identica').set_active(self.identica)
		self.glade.get_object('identica').set_label(_('Identi.ca Tuquito'))
		self.glade.get_object('twitter').set_active(self.twitter)
		self.glade.get_object('twitter').set_label(_('Twitter Tuquito'))
		self.glade.get_object('universo').set_active(self.universo)
		self.glade.get_object('universo').set_label(_('Solo Universo Tuquito (deshabilita los demas)'))
		self.glade.get_object('inicio').set_active(self.startup)
		self.glade.get_object('inicio').set_label(_('Inicio automatico'))
		self.glade.get_object('icono').set_active(self.traybar)
		self.glade.get_object('icono').set_label(_('Mostrar icono en el panel'))
		self.glade.get_object('sonido').set_active(self.sound)
		self.glade.get_object('sonido').set_label(_('Reproducir sonido de aviso'))
		
		self.glade.get_object('min').set_label(_('(minutos)'))

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
			pygame.init()
			pygame.mixer.music.load('/usr/share/sounds/trss-pop.ogg')
			pygame.mixer.music.play()
		n = pynotify.Notification('Tuquito RSS', text, '/usr/lib/tuquito/trss/trss.png')
		n.show()

if __name__ == '__main__':
	win = Preferencias()
	gtk.main()
