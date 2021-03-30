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
import tempfile
import re
import os
from hou import SceneViewer


class CreateFlipbook(object):

    # constructing the app
    def __init__(self, app):
        self.app = app

    # run a flipbook render with given settings
    def runFlipbook(self, settings):
        SceneViewer.flipbook(self.scene, settings=settings)

    # get a flipbook settings object and return with given inputs
    def getFlipbookSettings(self, inputSettings):
        self.__getSceneViewer()

        settings = self.scene.flipbookSettings().stash()
        self.app.logger.debug("Using %s object" % (settings))

        # standard settings
        settings.outputToMPlay(inputSettings["mplay"])
        settings.output(inputSettings["output"])
        settings.useResolution(True)
        settings.resolution(inputSettings["resolution"])
        settings.cropOutMaskOverlay(True)
        settings.frameRange(inputSettings["frameRange"])
        settings.beautyPassOnly(inputSettings["beautyPass"])
        settings.antialias(hou.flipbookAntialias.HighQuality)
        settings.sessionLabel(inputSettings["sessionLabel"])
        settings.useMotionBlur(inputSettings["motionBlur"])

        return settings

    def getOutputPath(self):
        outputPath = {}

        # create an temporary directory for the JPG files
        tempDir = tempfile.mkdtemp()
        outputPath["writeTempFile"] = os.path.join(
            tempDir, "temporary.$F4.jpg")

        # format temporary path for importing in Nuke
        outputPath["inputTempFile"] = re.sub(
            "\$F4", "####", outputPath["writeTempFile"]
        )

        # get template object from info.yml
        reviewTemplate = self.app.get_template("review_file_template")
        workTemplate = self.app.get_template("work_file_template")
        fields = workTemplate.get_fields(hou.hipFile.path())
        self.app.logger.debug(fields)
        outputPath["finFile"] = reviewTemplate.apply_fields(fields)

        return outputPath

    def getFrameRange(self):
        frameRange = []

        frameRange.append(hou.hscriptExpression("$FSTART"))
        frameRange.append(hou.hscriptExpression("$FEND"))

        return frameRange

    def __getSceneViewer(self):
        self.scene = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
        self.app.logger.debug("Using panetab %s" % (self.scene))
