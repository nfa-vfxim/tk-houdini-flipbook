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

import nuke
import sys
import datetime
import time
import os

input_path = sys.argv[1]
output_path = sys.argv[2]
project_name = sys.argv[3]
file_name = sys.argv[4]
first_frame = int(float(sys.argv[5]))
last_frame = int(float(sys.argv[6]))
appPath = sys.argv[7]
version = int(sys.argv[8])
resolution = sys.argv[9]
user_name = sys.argv[10]
task_name = sys.argv[11]
fps = float(sys.argv[12])

output_node = None

frame_padding = 3
_burnin_nk = os.path.join(appPath, "resources", "nfaSlate.nk")

# create group
group = nuke.nodes.Group()

# general metadata
company_name = "NFA"
today = datetime.date.today()
date_formatted = time.strftime("%d/%m/%Y %H:%M")
color_space = "Output - sRGB"

# operate in group
group.begin()


def __create_output_node(path):

    # get the Write node settings we'll use for generating the Quicktime
    wn_settings = __get_quicktime_settings()

    node = nuke.nodes.Write(file_type=wn_settings.get("file_type"))

    # apply any additional knob settings provided by the hook. Now that the knob has been
    # created, we can be sure specific file_type settings will be valid.
    for knob_name in wn_settings.keys():
        knob_value = wn_settings.get(knob_name)
        if knob_name != "file_type":
            node.knob(knob_name).setValue(knob_value)

    root_node = nuke.root()
    is_proxy = root_node["proxy"].value()
    if is_proxy:
        node["proxy"].setValue(path.replace(os.sep, "/"))
    else:
        node["file"].setValue(path.replace(os.sep, "/"))

    return node


def __get_quicktime_settings():
    settings = {}
    settings["file_type"] = "mov"
    if nuke.NUKE_VERSION_MAJOR >= 9:
        # Nuke 9.0v1 changed the codec knob name to meta_codec and added an encoder knob
        # (which defaults to the new mov64 encoder/decoder).
        settings["mov64_codec"] = 14
        settings["mov64_quality_max"] = "3"
        settings["mov64_fps"] = fps

        # setting output colorspace
        colorspace = nuke.root().knob("colorManagement").getValue()

        # If OCIO is set, Output - sRGB
        if colorspace:
            settings["colorspace"] = "Output - sRGB"

        # If no OCIO is set, detect if ACES is used or nuke_default
        else:
            ocio_config = nuke.root().knob("OCIO_config").getValue()

            if ocio_config == 2.0:
                settings["colorspace"] = "sRGB"

            else:
                settings["colorspace"] = "Output - sRGB"

    else:
        settings["codec"] = "jpeg"

    return settings


try:
    # create read node
    read = nuke.nodes.Read(
        name="source", file_type="jpg", file=input_path.replace(os.sep, "/")
    )
    read["on_error"].setValue("checkerboard")
    read["first"].setValue(first_frame)
    read["last"].setValue(last_frame)
    if color_space:
        read["colorspace"].setValue(color_space)

    # now create the slate/burnin node
    burn = nuke.nodePaste(_burnin_nk)
    burn.setInput(0, read)

    # format the burnins
    version_padding_format = "%%0%dd" % frame_padding
    version_str = version_padding_format % version

    if task_name:
        version_label = "%s, v%s" % (task_name, version_str)
    else:
        version_label = "v%s" % version_str

    burn.knob("project").setValue(project_name)
    burn.knob("company").setValue(date_formatted)
    burn.knob("file").setValue(file_name)
    burn.knob("date").setValue(date_formatted)

    framelist = "%i - %i (%i)" % (first_frame, last_frame, last_frame - first_frame)
    burn.knob("framelist").setValue(framelist)
    burn.knob("artist").setValue(user_name)
    burn.knob("task").setValue(task_name)
    burn.knob("version").setValue(version)
    burn.knob("fps").setValue(fps)
    burn.knob("colorspaceIDT").setValue("Output - sRGB")
    burn.knob("colorspaceODT").setValue("Output - sRGB")
    
    # Create the output node
    output_node = __create_output_node(output_path)
    output_node.setInput(0, burn)

finally:
    group.end()

if output_node:
    # Render the outputs, first view only
    nuke.executeMultiple(
        [output_node], ([first_frame - 1, last_frame, 1],), [nuke.views()[0]]
    )

# Cleanup after ourselves
nuke.delete(group)
