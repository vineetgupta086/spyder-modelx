# -*- coding: utf-8 -*-

# Copyright (c) 2017-2018 Fumito Hamamura <fumito.ham@gmail.com>

# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation version 3.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.  If not, see <http://www.gnu.org/licenses/>.

# The source code contains parts copied and modified from Spyder project:
# https://github.com/spyder-ide/spyder
# See below for the original copyright notice.

#
# Copyright (c) Spyder Project Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from qtpy.QtWidgets import QStackedWidget


class MxStackedMixin:
    MX_WIDGET_CLASS = None  # To be defined in sub class

    def __init__(self, parent):

        self.main = parent  # Spyder3

        # Widgets
        self.stack = QStackedWidget(self)
        self.shellwidgets = {}

        # On active tab in IPython console change
        self.main.ipyconsole.tabwidget.currentChanged.connect(
            self.on_ipyconsole_current_changed)

    # ----- Stack accesors ----------------------------------------------------
    # Modified from https://github.com/spyder-ide/spyder/blob/v3.3.2/spyder/plugins/variableexplorer.py#L140

    def set_current_widget(self, analyzer):
        self.stack.setCurrentWidget(analyzer)

    def current_widget(self):
        return self.stack.currentWidget()

    def count(self):
        return self.stack.count()

    def remove_widget(self, analyzer):
        self.stack.removeWidget(analyzer)

    def add_widget(self, analyzer):
        self.stack.addWidget(analyzer)

    # ----- Public API --------------------------------------------------------
    # Modified from https://github.com/spyder-ide/spyder/blob/v3.3.2/spyder/plugins/variableexplorer.py#L156

    def add_shellwidget(self, shellwidget):
        """
        Register shell with variable explorer.

        This function opens a new NamespaceBrowser for browsing the variables
        in the shell.
        """
        shellwidget_id = id(shellwidget)
        if shellwidget_id not in self.shellwidgets:
            analyzer = self.MX_WIDGET_CLASS(self)
            analyzer.set_shellwidget(shellwidget)
            # analyzer.sig_option_changed.connect(self.change_option)
            # analyzer.sig_free_memory.connect(self.free_memory)
            self.add_widget(analyzer)
            self.shellwidgets[shellwidget_id] = analyzer
            self.set_shellwidget_from_id(shellwidget_id)
            return analyzer

    def remove_shellwidget(self, shellwidget_id):
        # If shellwidget_id is not in self.shellwidgets, it simply means
        # that shell was not a Python-based console (it was a terminal)
        if shellwidget_id in self.shellwidgets:
            analyzer = self.shellwidgets.pop(shellwidget_id)
            self.remove_widget(analyzer)
            analyzer.close()

    def set_shellwidget_from_id(self, shellwidget_id):
        if shellwidget_id in self.shellwidgets:
            analyzer = self.shellwidgets[shellwidget_id]
            self.set_current_widget(analyzer)

    def on_ipyconsole_current_changed(self):
        # Slot like IPythonConsole.reflesh_plugin
        client = self.main.ipyconsole.tabwidget.currentWidget()
        if client:
            sw = client.shellwidget
            self.set_shellwidget_from_id(id(sw))
