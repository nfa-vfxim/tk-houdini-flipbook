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

class FlipbookDialog(QtWidgets.QDialog):
    def __init__(self, app, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        # create an instance of CreateFlipbook
        self.flipbook = CreateFlipbook(app)

        # other properties
        self.setWindowTitle("SGTK Flipbook")
        
        # define general layout
        layout = QtWidgets.QVBoxLayout()
        resolutionLayout = QtWidgets.QHBoxLayout()
        groupLayout = QtWidgets.QVBoxLayout()

        # widgets
        self.outputLabel = QtWidgets.QLabel("Flipbooking to: %s" % (self.flipbook.getOutputPath()))
        self.outputToMplay = QtWidgets.QCheckBox("MPlay Output", self)
        self.beautyPassOnly = QtWidgets.QCheckBox("Beauty Pass", self)
        self.useMotionblur = QtWidgets.QCheckBox("Motion Blur", self)
        
        # resolution widget
        # self.resolution = QtWidgets.QFrame()
        # self.resolution.setLayout(resolutionLayout)
        # self.resolutionX = QtWidgets.QLineEdit()
        # self.resolutionY = QtWidgets.QLineEdit()
        # self.resolution.addWidget(self.resolutionX)
        # self.resolution.addWidget(self.resolutionY)

        # options group
        self.optionsGroup = QtWidgets.QGroupBox("Flipbook options")
        groupLayout.addWidget(self.outputToMplay)
        groupLayout.addWidget(self.beautyPassOnly)
        groupLayout.addWidget(self.useMotionblur)
        self.optionsGroup.setLayout(groupLayout)

        # button box buttons
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.startButton = QtWidgets.QPushButton("Start Flipbook")

        # lower right button box
        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.addButton(self.startButton, QtWidgets.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.cancelButton, QtWidgets.QDialogButtonBox.ActionRole)

        # widgets additions
        layout.addWidget(self.outputLabel)
        # layout.addWidget(self.resolution)
        layout.addWidget(self.optionsGroup)
        layout.addWidget(buttonBox)

        self.cancelButton.clicked.connect(self.closeWindow)
        # self.startButton.clicked.connect()

        # finally, set layout
        self.setLayout(layout)

    def closeWindow(self):
        self.close()