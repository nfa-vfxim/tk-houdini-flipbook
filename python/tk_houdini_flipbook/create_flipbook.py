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
    def run_flipbook(self, settings):
        SceneViewer.flipbook(self.scene, settings=settings)

    # get a flipbook settings object and return with given inputs
    def get_flipbook_settings(self, inputSettings):
        self.__get_scene_viewer()

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

    def get_output_path(self):
        output_path = {}

        # create an temporary directory for the JPG files
        temp_dir = tempfile.mkdtemp()
        output_path["writeTempFile"] = os.path.join(temp_dir, "temporary.$F4.jpg")

        # format temporary path for importing in Nuke
        output_path["inputTempFile"] = re.sub(
            "\$F4", "####", output_path["writeTempFile"]
        )

        # get template object from info.yml
        review_template = self.app.get_template("review_file_template")
        work_template = self.app.get_template("work_file_template")
        fields = work_template.get_fields(hou.hipFile.path())
        self.app.logger.debug(fields)
        output_path["finFile"] = review_template.apply_fields(fields)

        return output_path

    def get_frame_range(self):
        frame_range = []

        frame_range.append(hou.hscriptExpression("$FSTART"))
        frame_range.append(hou.hscriptExpression("$FEND"))

        return frame_range

    def __get_scene_viewer(self):
        self.scene = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
        self.app.logger.debug("Using panetab %s" % (self.scene))
