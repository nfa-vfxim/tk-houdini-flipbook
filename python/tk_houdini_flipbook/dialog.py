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
        self.setWindowTitle("ShotGrid Flipbook")

        # define general layout
        layout = QtWidgets.QVBoxLayout()
        group_layout = QtWidgets.QVBoxLayout()

        # widgets
        self.output_label = QtWidgets.QLabel(
            "Flipbooking to: %s"
            % (os.path.basename(self.flipbook.get_output_path()["finFile"]))
        )
        self.output_to_mplay = QtWidgets.QCheckBox("MPlay Output", self)
        self.output_to_mplay.setChecked(True)
        self.beauty_pass_only = QtWidgets.QCheckBox("Beauty Pass", self)
        self.use_motionblur = QtWidgets.QCheckBox("Motion Blur", self)

        # save new version widget
        self.save_new_version_checkbox = QtWidgets.QCheckBox("Save New Version", self)
        self.save_new_version_checkbox.setChecked(True)

        # description widget
        self.description_label = QtWidgets.QLabel("Description")
        self.description = QtWidgets.QLineEdit()

        # resolution sub-widgets x
        self.resolution_x = QtWidgets.QWidget()
        resolution_x_layout = QtWidgets.QVBoxLayout()
        self.resolution_x_label = QtWidgets.QLabel("Width")
        self.resolution_x_line = QtWidgets.QLineEdit()
        self.resolution_x.default = "1920"
        self.resolution_x_line.setPlaceholderText(self.resolution_x.default)
        self.resolution_x_line.setInputMask("9990")
        resolution_x_layout.addWidget(self.resolution_x_label)
        resolution_x_layout.addWidget(self.resolution_x_line)
        self.resolution_x.setLayout(resolution_x_layout)

        # resolution sub-widgets y
        self.resolution_y = QtWidgets.QWidget()
        resolution_y_layout = QtWidgets.QVBoxLayout()
        self.resolution_y_label = QtWidgets.QLabel("Height")
        self.resolution_y_line = QtWidgets.QLineEdit()
        self.resolution_y.default = "1080"
        self.resolution_y_line.setPlaceholderText(self.resolution_y.default)
        self.resolution_y_line.setInputMask("9990")
        resolution_y_layout.addWidget(self.resolution_y_label)
        resolution_y_layout.addWidget(self.resolution_y_line)
        self.resolution_y.setLayout(resolution_y_layout)

        # resolution group
        self.resolution_group = QtWidgets.QGroupBox("Resolution")
        resolution_group_layout = QtWidgets.QHBoxLayout()
        resolution_group_layout.addWidget(self.resolution_x)
        resolution_group_layout.addWidget(self.resolution_y)
        self.resolution_group.setLayout(resolution_group_layout)

        # frame range widget
        self.frame_range = QtWidgets.QGroupBox("Frame range")
        frame_range_group_layout = QtWidgets.QHBoxLayout()

        # frame range start sub-widget
        self.frame_range_start = QtWidgets.QWidget()
        frame_range_start_layout = QtWidgets.QVBoxLayout()
        self.frame_range_start_label = QtWidgets.QLabel("Start")
        self.frame_range_start_line = QtWidgets.QLineEdit()
        self.frame_range_start_line.setPlaceholderText(
            "%i" % (self.flipbook.get_frame_range()[0])
        )
        self.frame_range_start_line.setInputMask("9000")
        frame_range_start_layout.addWidget(self.frame_range_start_label)
        frame_range_start_layout.addWidget(self.frame_range_start_line)
        self.frame_range_start.setLayout(frame_range_start_layout)
        frame_range_group_layout.addWidget(self.frame_range_start)

        # frame range end sub-widget
        self.frame_range_end = QtWidgets.QWidget()
        frame_range_end_layout = QtWidgets.QVBoxLayout()
        self.frame_range_end_label = QtWidgets.QLabel("End")
        self.frame_range_end_line = QtWidgets.QLineEdit()
        self.frame_range_end_line.setPlaceholderText(
            "%i" % (self.flipbook.get_frame_range()[1])
        )
        self.frame_range_end_line.setInputMask("9000")
        frame_range_end_layout.addWidget(self.frame_range_end_label)
        frame_range_end_layout.addWidget(self.frame_range_end_line)
        self.frame_range_end.setLayout(frame_range_end_layout)
        frame_range_group_layout.addWidget(self.frame_range_end)

        # frame range widget finalizing
        self.frame_range.setLayout(frame_range_group_layout)

        # copy to path widget
        self.copy_path_button = QtWidgets.QPushButton("Copy Path to Clipboard")

        # options group
        self.options_group = QtWidgets.QGroupBox("Flipbook options")
        group_layout.addWidget(self.output_to_mplay)
        group_layout.addWidget(self.beauty_pass_only)
        group_layout.addWidget(self.use_motionblur)
        group_layout.addWidget(self.save_new_version_checkbox)
        group_layout.addWidget(self.copy_path_button)
        self.options_group.setLayout(group_layout)

        # button box buttons
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.start_button = QtWidgets.QPushButton("Start Flipbook")

        # lower right button box
        button_box = QtWidgets.QDialogButtonBox()
        button_box.addButton(self.start_button, QtWidgets.QDialogButtonBox.ActionRole)
        button_box.addButton(self.cancel_button, QtWidgets.QDialogButtonBox.ActionRole)

        # widgets additions
        layout.addWidget(self.output_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description)
        layout.addWidget(self.frame_range)
        layout.addWidget(self.resolution_group)
        layout.addWidget(self.options_group)
        layout.addWidget(button_box)

        # connect button functionality
        self.cancel_button.clicked.connect(self.close_window)
        self.start_button.clicked.connect(self.start_flipbook)
        self.copy_path_button.clicked.connect(self.copy_path_to_clipboard)

        # finally, set layout
        self.setLayout(layout)

    def close_window(self):
        self.close()

    def start_flipbook(self):

        input_settings = {}

        output_path = self.flipbook.get_output_path()
        description = self.validate_description()

        # create submitter class
        submit = SubmitVersion(
            self.app,
            output_path["finFile"],
            int(self.validate_frame_range()[0]),
            int(self.validate_frame_range()[1]),
            description,
        )

        # validation of inputs
        input_settings["frameRange"] = self.validate_frame_range()
        input_settings["resolution"] = self.validate_resolution()
        input_settings["mplay"] = self.validate_mplay()
        input_settings["beautyPass"] = self.validate_beauty()
        input_settings["motionBlur"] = self.validate_motionblur()
        input_settings["output"] = output_path["writeTempFile"]
        input_settings["sessionLabel"] = output_path["finFile"]

        self.app.logger.debug("Using the following settings, %s" % (input_settings))

        # retrieve full settings object
        settings = self.flipbook.get_flipbook_settings(input_settings)

        # run the actual flipbook
        try:
            with hou.InterruptableOperation(
                "Flipbooking",
                long_operation_name="Creating a flipbook",
                open_interrupt_dialog=True,
            ) as operation:
                operation.updateLongProgress(0, "Starting Flipbook")
                self.flipbook.run_flipbook(settings)
                operation.updateLongProgress(
                    0.25, "Rendering to Nuke, please sit tight."
                )
                self.slate.run_slate(
                    output_path["inputTempFile"],
                    output_path["finFile"],
                    input_settings,
                )
                operation.updateLongProgress(0.5, "Uploading to Shotgun")
                submit.submit_version()
                operation.updateLongProgress(0.75, "Saving")
                self.save_new_version()
                operation.updateLongProgress(1, "Done, closing window.")
                self.close_window()
                self.app.logger.info("Flipbook successful")

        except Exception as e:
            self.app.logger.error("Oops, something went wrong!")
            self.app.logger.error(e)

        return

    # copyPathButton callback
    # copy the output path to the clipboard
    def copy_path_to_clipboard(self):
        path = self.flipbook.get_output_path()["finFile"]
        self.app.logger.debug("Copying path to clipboard: %s" % path)
        QtGui.QGuiApplication.clipboard().setText(path)
        return

    # save_new_version callback
    def save_new_version(self):

        # if validate_save_new_version returns true, save the current hipfile with an incremented version number
        if self.validate_save_new_version():
            self.app.logger.debug("Saving new version.")
            hou.hipFile.saveAndIncrementFileName()
        # if validate_save_new_version returns false, just save the current hipfile
        else:
            hou.hipFile.save()

    # save_new_version validation
    # check if the save new version option is ticked
    def validate_save_new_version(self):
        return self.save_new_version_checkbox.isChecked()

    def validate_frame_range(self):
        # validating the frame range input
        frame_range = []

        if self.frame_range_start_line.hasAcceptableInput():
            self.app.logger.debug(
                "Setting start of frame range to %s"
                % (self.frame_range_start_line.text())
            )
            frame_range.append(int(self.frame_range_start_line.text()))
        else:
            self.app.logger.debug(
                "Setting start of frame range to %i"
                % (self.flipbook.get_frame_range()[0])
            )
            frame_range.append(self.flipbook.get_frame_range()[0])

        if self.frame_range_end_line.hasAcceptableInput():
            self.app.logger.debug(
                "Setting end of frame range to %s" % (self.frame_range_end_line.text())
            )
            frame_range.append(int(self.frame_range_end_line.text()))
        else:
            self.app.logger.debug(
                "Setting end of frame range to %i"
                % (self.flipbook.get_frame_range()[1])
            )
            frame_range.append(self.flipbook.get_frame_range()[1])

        return tuple(frame_range)

    def validate_resolution(self):
        # validating the resolution input
        resolution = []

        if self.resolution_x_line.hasAcceptableInput():
            self.app.logger.debug(
                "Setting width resolution to %s" % (self.resolution_x_line.text())
            )
            resolution.append(int(self.resolution_x_line.text()))
        else:
            self.app.logger.debug(
                "Setting width resolution to %s" % (self.resolution_x.default)
            )
            resolution.append(int(self.resolution_x.default))

        if self.resolution_y_line.hasAcceptableInput():
            self.app.logger.debug(
                "Setting height resolution to %s" % (self.resolution_y_line.text())
            )
            resolution.append(int(self.resolution_y_line.text()))
        else:
            self.app.logger.debug(
                "Setting height resolution to %s" % (self.resolution_y.default)
            )
            resolution.append(int(self.resolution_y.default))

        return tuple(resolution)

    def validate_mplay(self):
        # validating the mplay checkbox

        return self.output_to_mplay.isChecked()

    def validate_beauty(self):
        # validating the beauty pass checkbox

        return self.beauty_pass_only.isChecked()

    def validate_motionblur(self):
        # validating the motion blur checkbox

        return self.use_motionblur.isChecked()

    def validate_description(self):

        return str(self.description.text().encode("utf-8"))
