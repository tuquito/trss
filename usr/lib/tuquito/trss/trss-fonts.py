#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Tuquito RSS 1.3-1
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

import gtk
import gettext, os

# i18n
gettext.install('trss', '/usr/share/tuquito/locale')

#-Variables
userFonts = os.path.join(os.environ['HOME'], '.tuquito/trss/userFonts')

class Fonts:
	def __init__(self):
		self.glade = gtk.Builder()
		self.glade.add_from_file('/usr/lib/tuquito/trss/trss-fonts.glade')
		self.window = self.glade.get_object('window')
		self.window.set_title(_('RSS Tuquito Sources'))
		self.treeview_domains = self.glade.get_object('treeview_domains')

		self.column1 = gtk.TreeViewColumn(_('New Sources'), gtk.CellRendererText(), text=0)
		self.column1.set_sort_column_id(0)
		self.column1.set_resizable(True)
		self.treeview_domains.append_column(self.column1)
		self.treeview_domains.set_headers_clickable(True)
		self.treeview_domains.set_reorderable(False)
		self.treeview_domains.show()

		self.model = gtk.TreeStore(str)
		self.model.set_sort_column_id( 0, gtk.SORT_ASCENDING )
		self.treeview_domains.set_model(self.model)

		if not os.path.isfile(userFonts):
			os.system('touch ' + userFonts)
		fontsFile = open(userFonts)
		for line in fontsFile:
			line = str.strip(line)
			iter = self.model.insert_before(None, None)
			self.model.set_value(iter, 0, line)
		del self.model
		self.glade.connect_signals(self)
		self.window.show()

	def addFont(self, widget):
		self.glade.get_object('name').set_text('')
		self.glade.get_object('url').set_text('')
		self.glade.get_object('addFont').set_title(_('Add source'))
		self.glade.get_object('lname').set_label(_('Name: (eg Tuquito Forums)'))
		self.glade.get_object('lurl').set_label(_('Source URL:'))
		self.glade.get_object('addFont').show()

	def closeFonts(self, widget, data=None):
		self.glade.get_object('addFont').hide()
		return True

	def saveFont(self, widget):
		name = self.glade.get_object('name').get_text().strip()
		url = self.glade.get_object('url').get_text().strip()
		if url != '':
			self.model = self.treeview_domains.get_model()
			iter = self.model.insert_before(None, None)
			font = name + '|' + url
			self.model.set_value(iter, 0, font)
			os.system('echo "' + font + '" >>' + userFonts)
		self.closeFonts(self)

	def removeFont(self, widget):
		self.selection = self.treeview_domains.get_selection()
		(self.model, iter) = self.selection.get_selected()
		if (iter != None):
			font = self.model.get_value(iter, 0)
			os.system("sed '/" + font + "/ d' " + userFonts + ' > ' + userFonts + '.back')
			os.system('mv ' + userFonts + '.back ' + userFonts)
			self.model.remove(iter)

	def quit(self, widget, data=None):
		gtk.main_quit()
		return True

if __name__ == '__main__':
	win = Fonts()
	gtk.main()

