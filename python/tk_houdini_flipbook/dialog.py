# MIT License

# Copyright (c) 2020 Netherlands Film Academy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import hou
import sgtk
from .create_flipbook import CreateFlipbook

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtUiTools

class FlipbookDialog(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.setWindowTitle("SGTK Flipbook")

        self.outputLabel = QtWidgets.QLabel(CreateFlipbook.getOutputPath())

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.startButton = QtWidgets.QPushButton("Start Flipbook")

        layout = QtWidgets.QVBoxLayout()

        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.addButton(self.startButton, QtWidgets.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.cancelButton, QtWidgets.QDialogButtonBox.ActionRole)

        layout.addWidget(self.outputLabel)
        layout.addWidget(buttonBox)
        self.setLayout(layout)