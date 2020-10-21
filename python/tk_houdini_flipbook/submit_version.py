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

import sgtk
import os
from PySide2 import QtCore


class SubmitVersion(object):

    # initialize class
    def __init__(self, app, filePath, firstFrame, lastFrame, description):

        # bind parented app class
        self.app = app
        # bind rendered file path
        self.file = filePath
        # bind frame range
        self.frameRange = [firstFrame, lastFrame]
        self.description = description

    # submit file to shotgun
    def submit_version(self):

        # bind user
        user = sgtk.util.get_current_user(self.app.sgtk)

        # calculate name for version
        # get file path and strip it of path and extension
        name = os.path.splitext(os.path.basename(self.file))[0]

        # get the current context
        ctx = self.app.context

        # update data object for submission
        data = {
            "code": name,
            "sg_status_list": "rev",
            "entity": ctx.entity,
            "sg_task": ctx.task,
            "sg_first_frame": self.frameRange[0],
            "sg_last_frame": self.frameRange[1],
            "sg_frames_have_slate": False,
            "created_by": user,
            "user": user,
            "description": self.description,
            "sg_movie_has_slate": True,
            "project": ctx.project,
        }

        # calculate frame count and range and update accordingly
        data["frame_count"] = self.frameRange[1] - self.frameRange[0] + 1
        data["frame_range"] = "%s-%s" % (self.frameRange[0], self.frameRange[1])

        # link movie file
        data["sg_path_to_movie"] = self.file

        # create the version in shotgun
        try:
            version = self.app.sgtk.shotgun.create("Version", data)
        except:
            self.app.logger.debug("This is the error.")
        
        self.app.logger.debug("Created version in shotgun: %s" % str(data))

        # upload the movie files to shotgun
        self.__upload_version(version)
        self.app.logger.debug("Uploaded version in shotgun")

    # function to upload files to shotgun
    def __upload_version(self, version):

        # create a new event loop to upload files
        eventLoop = QtCore.QEventLoop()

        # open new thread and wait for thread to finish
        thread = UploaderThread(self.app, version, self.file)
        thread.finished.connect(eventLoop.quit)
        thread.start()
        eventLoop.exec_()

        if thread.get_errors():
            for e in thread.get_errors():
                self.app.logger.error(e)


class UploaderThread(QtCore.QThread):

    # initialize class
    def __init__(self, app, version, filePath):

        # initialize super class
        QtCore.QThread.__init__(self)

        self.app = app
        self.version = version
        self.file = filePath
        self._errors = []

    # function to retreive errors
    def get_errors(self):

        return self._errors

    # run the actual thread
    def run(self):

        try:
            self.app.sgtk.shotgun.upload(
                "Version", self.version["id"], self.file, "sg_uploaded_movie"
            )
        except Exception as e:
            self._errors.append("Movie upload to Shotgun failed: %s" % e)