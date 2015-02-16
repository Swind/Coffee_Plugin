import StringIO

import sys

from pypeg2 import parse
from steps import Steps

from octoprint import server 
import octoprint.util.gcodeInterpreter as gcodeInterpreter

class Cookbook(object):

    default_content = """G21
G28
G90
M83

G1 Z80 F400
G1 X0 Y0
G1 F150
"""

    def __init__(self, name, content=default_content):
        self.name = name
        self.content = content

    def gcode(self):
        steps = parse(self.content, Steps)

        output = StringIO.StringIO()
        output.write(self.default_content)

        for step in steps:
            process = step["process"]

            for process_step in process:
                output.write("\n".join(process_step.gcode()))
                output.write("\n")

        gcode = output.getvalue()
        output.close()

        return CookbookGcode(gcode)

    # Save the cookbook script to file and generate a gcode file
    # This function is used by Octoprint file manager
    def save(self, path):
        with open(path, "w") as file:
            file.write(self.content)

class CookbookGcode(object):
    def __init__(self, gcode):
        self.gcode = gcode

    # Save the cookbook script to file and generate a gcode file
    # This function is used by Octoprint file manager
    def save(self, path):
        with open(path, "w") as file:
            file.write(self.gcode)
