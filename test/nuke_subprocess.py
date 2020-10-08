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

import subprocess

nPath = r"C:\Program Files\Nuke12.1v4\Nuke12.1.exe"
sPath = r"C:\Users\Bo.Kamphues\Documents\coding\tk-houdini-flipbook\python\tk_houdini_flipbook\slate.py"
inputPath = r"C:\Users\Bo.Kamphues\Downloads\flipbook_test\test.%04d.jpg"
outputPath = r"C:\Users\Bo.Kamphues\Downloads\flipbook_test\test.mov"
project_name = "Verlangen"
file_name = "ver_asset_model_v001.hip"
first_frame = 1001
last_frame = 1004
appPath = r"C:\Users\Bo.Kamphues\Documents\coding\tk-houdini-flipbook"
version = 1
resolution = "1920 x 1080"
user_name = "Bo Kamphues"
task_name = "Modelling Shit"
fps = 24

process = subprocess.Popen(
    [
        nPath,
        "-t",
        sPath,
        inputPath,
        outputPath,
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
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)

info, err = process.communicate()

print(info)
print(err)
