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
import hou
from hou import SceneViewer

class CreateFlipbook(object):
    
    @staticmethod
    def runFlipbook(settings):
        SceneViewer.flipbook(settings)

    @staticmethod
    def getFlipbookSettings(inputSettings):
        settings = hou.SceneViewer.flipbookSettings().stash()

        # standard settings
        settings.outputToMPlay(True)
        settings.output(inputSettings.output)
        settings.useResolution(True)
        settings.resolution(inputSettings.resolution)
        settings.cropOutMaskOverlay(True)
        settings.frameRange(inputSettings.frameRange)
        settings.visibleObjects(inputSettings.visibleObjects)
        settings.beautyPassOnly(inputSettings.beautyPassOnly)
        settings.antialias(hou.flipbookAntialias.HighQuality)
        settings.sessionLabel(inputSettings.sessionLabel)
        settings.useMotionBlur(inputSettings.useMotionBlur)

        return settings

    @staticmethod
    def getOutputPath():
        outputPath = ""

        

        return outputPath