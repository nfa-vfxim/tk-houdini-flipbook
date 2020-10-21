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
import subprocess
import hou
import sgtk


class CreateSlate(object):
    def __init__(self, app):
        # initialize and set paths
        self.app = app
        self.nukePath = "%s" % (app.get_setting("nuke_path"))

        # set slate script path
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        self.slatePath = os.path.join(__location__, "slate.py")

    def runSlate(self, inputFile, outputFile, settings):
        # setup environment
        custom_env = os.environ.copy()

        if custom_env["PYTHONPATH"] != None:
            del custom_env["PYTHONPATH"]

        if custom_env["PYTHONHOME"] != None:
            del custom_env["PYTHONHOME"]

        # setup arguments for call
        context = self.app.context
        project_name = context.project["name"]
        user_name = context.user["name"]
        file_name = hou.hipFile.basename().lower()
        first_frame = settings["frameRange"]
        first_frame = first_frame[0]
        last_frame = settings["frameRange"]
        last_frame = last_frame[1]
        task_name = context.step["name"]
        self.app.logger.debug(task_name)
        fps = hou.fps()
        appPath = self.app.disk_location

        # ensure output path exists
        self.app.ensure_folder_exists(os.path.dirname(os.path.abspath(outputFile)))

        # calculate version number
        template = self.app.get_template("work_file_template")
        fields = template.get_fields(hou.hipFile.path())
        version = fields["version"]
        resolution = "%d x %d" % (
            settings["resolution"][0],
            settings["resolution"][0],
        )

        # call subprocess of nuke and convert
        process = subprocess.Popen(
            [
                self.nukePath,
                "-t",
                self.slatePath,
                inputFile,
                outputFile,
                project_name,
                file_name,
                str(first_frame),
                str(last_frame),
                appPath,
                str(version),
                resolution,
                user_name,
                task_name,
                str(fps),
            ],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=custom_env,
        )

        stdout, stderr = process.communicate()
        self.app.logger.debug(stdout)
        
        if stderr:
            self.app.logger.error(stderr)

        if stderr:
            raise Exception("Could not correctly render file. Used Nuke version %s" % (self.nukePath))
