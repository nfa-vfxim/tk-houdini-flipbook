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

import os
import hou
from .create_flipbook import CreateFlipbook
from .create_slate import CreateSlate
from .submit_version import SubmitVersion

from PySide2 import QtGui
from PySide2 import QtWidgets


class FlipbookDialog(QtWidgets.QDialog):
    def __init__(self, app, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.app = app

        # create an instance of CreateFlipbook
        # create an instance of CreateSlate
        self.flipbook = CreateFlipbook(app)
        self.slate = CreateSlate(app)

        # other properties
        self.setWindowTitle("SGTK Flipbook")

        # define general layout
        layout = QtWidgets.QVBoxLayout()
        groupLayout = QtWidgets.QVBoxLayout()

        # widgets
        self.outputLabel = QtWidgets.QLabel(
            "Flipbooking to: %s"
            % (os.path.basename(self.flipbook.getOutputPath()["finFile"]))
        )
        self.outputToMplay = QtWidgets.QCheckBox("MPlay Output", self)
        self.outputToMplay.setChecked(True)
        self.beautyPassOnly = QtWidgets.QCheckBox("Beauty Pass", self)
        self.useMotionblur = QtWidgets.QCheckBox("Motion Blur", self)

        # save new version widget
        self.saveNewVersionCheckbox = QtWidgets.QCheckBox(
            "Save New Version", self)
        self.saveNewVersionCheckbox.setChecked(True)

        # description widget
        self.descriptionLabel = QtWidgets.QLabel("Description")
        self.description = QtWidgets.QLineEdit()

        # resolution sub-widgets x
        self.resolutionX = QtWidgets.QWidget()
        resolutionXLayout = QtWidgets.QVBoxLayout()
        self.resolutionXLabel = QtWidgets.QLabel("Width")
        self.resolutionXLine = QtWidgets.QLineEdit()
        self.resolutionX.default = "1920"
        self.resolutionXLine.setPlaceholderText(self.resolutionX.default)
        self.resolutionXLine.setInputMask("9990")
        resolutionXLayout.addWidget(self.resolutionXLabel)
        resolutionXLayout.addWidget(self.resolutionXLine)
        self.resolutionX.setLayout(resolutionXLayout)

        # resolution sub-widgets y
        self.resolutionY = QtWidgets.QWidget()
        resolutionYLayout = QtWidgets.QVBoxLayout()
        self.resolutionYLabel = QtWidgets.QLabel("Height")
        self.resolutionYLine = QtWidgets.QLineEdit()
        self.resolutionY.default = "1080"
        self.resolutionYLine.setPlaceholderText(self.resolutionY.default)
        self.resolutionYLine.setInputMask("9990")
        resolutionYLayout.addWidget(self.resolutionYLabel)
        resolutionYLayout.addWidget(self.resolutionYLine)
        self.resolutionY.setLayout(resolutionYLayout)

        # resolution group
        self.resolutionGroup = QtWidgets.QGroupBox("Resolution")
        resolutionGroupLayout = QtWidgets.QHBoxLayout()
        resolutionGroupLayout.addWidget(self.resolutionX)
        resolutionGroupLayout.addWidget(self.resolutionY)
        self.resolutionGroup.setLayout(resolutionGroupLayout)

        # frame range widget
        self.frameRange = QtWidgets.QGroupBox("Frame range")
        frameRangeGroupLayout = QtWidgets.QHBoxLayout()

        # frame range start sub-widget
        self.frameRangeStart = QtWidgets.QWidget()
        frameRangeStartLayout = QtWidgets.QVBoxLayout()
        self.frameRangeStartLabel = QtWidgets.QLabel("Start")
        self.frameRangeStartLine = QtWidgets.QLineEdit()
        self.frameRangeStartLine.setPlaceholderText(
            "%i" % (self.flipbook.getFrameRange()[0])
        )
        self.frameRangeStartLine.setInputMask("9000")
        frameRangeStartLayout.addWidget(self.frameRangeStartLabel)
        frameRangeStartLayout.addWidget(self.frameRangeStartLine)
        self.frameRangeStart.setLayout(frameRangeStartLayout)
        frameRangeGroupLayout.addWidget(self.frameRangeStart)

        # frame range end sub-widget
        self.frameRangeEnd = QtWidgets.QWidget()
        frameRangeEndLayout = QtWidgets.QVBoxLayout()
        self.frameRangeEndLabel = QtWidgets.QLabel("End")
        self.frameRangeEndLine = QtWidgets.QLineEdit()
        self.frameRangeEndLine.setPlaceholderText(
            "%i" % (self.flipbook.getFrameRange()[1])
        )
        self.frameRangeEndLine.setInputMask("9000")
        frameRangeEndLayout.addWidget(self.frameRangeEndLabel)
        frameRangeEndLayout.addWidget(self.frameRangeEndLine)
        self.frameRangeEnd.setLayout(frameRangeEndLayout)
        frameRangeGroupLayout.addWidget(self.frameRangeEnd)

        # frame range widget finalizing
        self.frameRange.setLayout(frameRangeGroupLayout)

        # copy to path widget
        self.copyPathButton = QtWidgets.QPushButton("Copy Path to Clipboard")

        # options group
        self.optionsGroup = QtWidgets.QGroupBox("Flipbook options")
        groupLayout.addWidget(self.outputToMplay)
        groupLayout.addWidget(self.beautyPassOnly)
        groupLayout.addWidget(self.useMotionblur)
        groupLayout.addWidget(self.saveNewVersionCheckbox)
        groupLayout.addWidget(self.copyPathButton)
        self.optionsGroup.setLayout(groupLayout)

        # button box buttons
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.startButton = QtWidgets.QPushButton("Start Flipbook")

        # lower right button box
        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.addButton(
            self.startButton, QtWidgets.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.cancelButton,
                            QtWidgets.QDialogButtonBox.ActionRole)

        # widgets additions
        layout.addWidget(self.outputLabel)
        layout.addWidget(self.descriptionLabel)
        layout.addWidget(self.description)
        layout.addWidget(self.frameRange)
        layout.addWidget(self.resolutionGroup)
        layout.addWidget(self.optionsGroup)
        layout.addWidget(buttonBox)

        # connect button functionality
        self.cancelButton.clicked.connect(self.closeWindow)
        self.startButton.clicked.connect(self.startFlipbook)
        self.copyPathButton.clicked.connect(self.copyPathToClipboard)

        # finally, set layout
        self.setLayout(layout)

    def closeWindow(self):
        self.close()

    def startFlipbook(self):

        inputSettings = {}

        outputPath = self.flipbook.getOutputPath()
        description = self.validateDescription()

        # create submitter class
        submit = SubmitVersion(
            self.app,
            outputPath["finFile"],
            int(self.validateFrameRange()[0]),
            int(self.validateFrameRange()[1]),
            description,
        )

        # validation of inputs
        inputSettings["frameRange"] = self.validateFrameRange()
        inputSettings["resolution"] = self.validateResolution()
        inputSettings["mplay"] = self.validateMplay()
        inputSettings["beautyPass"] = self.validateBeauty()
        inputSettings["motionBlur"] = self.validateMotionBlur()
        inputSettings["output"] = outputPath["writeTempFile"]
        inputSettings["sessionLabel"] = outputPath["finFile"]

        self.app.logger.debug(
            "Using the following settings, %s" % (inputSettings))

        # retrieve full settings object
        settings = self.flipbook.getFlipbookSettings(inputSettings)

        # run the actual flipbook
        try:
            with hou.InterruptableOperation(
                "Flipbooking",
                long_operation_name="Creating a flipbook",
                open_interrupt_dialog=True,
            ) as operation:
                operation.updateLongProgress(0, "Starting Flipbook")
                self.flipbook.runFlipbook(settings)
                operation.updateLongProgress(
                    0.25, "Rendering to Nuke, please sit tight."
                )
                self.slate.runSlate(
                    outputPath["inputTempFile"],
                    outputPath["finFile"],
                    inputSettings,
                )
                operation.updateLongProgress(0.5, "Uploading to Shotgun")
                submit.submit_version()
                operation.updateLongProgress(0.75, "Saving")
                self.saveNewVersion()
                operation.updateLongProgress(1, "Done, closing window.")
                self.closeWindow()
                self.app.logger.info("Flipbook successful")

        except Exception as e:
            self.app.logger.error("Oops, something went wrong!")
            self.app.logger.error(e)

        return

    # copyPathButton callback
    # copy the output path to the clipboard
    def copyPathToClipboard(self):
        path = self.flipbook.getOutputPath()['finFile']
        self.app.logger.debug("Copying path to clipboard: %s" % path)
        QtGui.QGuiApplication.clipboard().setText(path)
        return

    # saveNewVersion callback
    def saveNewVersion(self):

        # if validateSaveNewVersion returns true, save the current hipfile with an incremented version number
        if(self.validateSaveNewVersion()):
            self.app.logger.debug("Saving new version.")
            hou.hipFile.saveAndIncrementFileName()
        # if validateSaveNewVersion returns false, just save the current hipfile
        else:
            hou.hipFile.save()

    # saveNewVersion validation
    # check if the save new version option is ticked
    def validateSaveNewVersion(self):
        return self.saveNewVersionCheckbox.isChecked()

    def validateFrameRange(self):
        # validating the frame range input
        frameRange = []

        if self.frameRangeStartLine.hasAcceptableInput():
            self.app.logger.debug(
                "Setting start of frame range to %s" % (
                    self.frameRangeStartLine.text())
            )
            frameRange.append(int(self.frameRangeStartLine.text()))
        else:
            self.app.logger.debug(
                "Setting start of frame range to %i"
                % (self.flipbook.getFrameRange()[0])
            )
            frameRange.append(self.flipbook.getFrameRange()[0])

        if self.frameRangeEndLine.hasAcceptableInput():
            self.app.logger.debug(
                "Setting end of frame range to %s" % (
                    self.frameRangeEndLine.text())
            )
            frameRange.append(int(self.frameRangeEndLine.text()))
        else:
            self.app.logger.debug(
                "Setting end of frame range to %i" % (
                    self.flipbook.getFrameRange()[1])
            )
            frameRange.append(self.flipbook.getFrameRange()[1])

        return tuple(frameRange)

    def validateResolution(self):
        # validating the resolution input
        resolution = []

        if self.resolutionXLine.hasAcceptableInput():
            self.app.logger.debug(
                "Setting width resolution to %s" % (
                    self.resolutionXLine.text())
            )
            resolution.append(int(self.resolutionXLine.text()))
        else:
            self.app.logger.debug(
                "Setting width resolution to %s" % (self.resolutionX.default)
            )
            resolution.append(int(self.resolutionX.default))

        if self.resolutionYLine.hasAcceptableInput():
            self.app.logger.debug(
                "Setting height resolution to %s" % (
                    self.resolutionYLine.text())
            )
            resolution.append(int(self.resolutionYLine.text()))
        else:
            self.app.logger.debug(
                "Setting height resolution to %s" % (self.resolutionY.default)
            )
            resolution.append(int(self.resolutionY.default))

        return tuple(resolution)

    def validateMplay(self):
        # validating the mplay checkbox

        return self.outputToMplay.isChecked()

    def validateBeauty(self):
        # validating the beauty pass checkbox

        return self.beautyPassOnly.isChecked()

    def validateMotionBlur(self):
        # validating the motion blur checkbox

        return self.useMotionblur.isChecked()

    def validateDescription(self):

        return str(self.description.text().encode('utf-8'))
