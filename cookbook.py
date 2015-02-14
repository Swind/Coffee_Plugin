import StringIO

import sys

from pypeg2 import parse
from parser.steps import Steps

from octoprint import server 
import octoprint.util.gcodeInterpreter as gcodeInterpreter

default_content = """G21
G28
G90
M83

G1 Z80 F400
G1 X0 Y0
G1 F150
"""
class Cookbook(object):

    def __init__(self, name, stepsPath, gcodePath, content=default_content):
        self.name = name
        self.stepsPath = stepsPath
        self.gcodePath = gcodePath
        self._steps = None
        self.content = content

        self.gcode_analysis = gcodeInterpreter.gcode()
        self.total_move_time_minute = 0
        self.total_extrusion_amount = 0 

    def save(self, steps=None):
        if steps:
            self._steps = steps

        with open(self.stepsPath, "w") as stepsFile:
            stepsFile.write(steps)

        # Generate GCode and save it to file
        with open(self.gcodePath, "w") as gcodeFile:
            gcodeFile.write(self.gcode())

    def load(self):
        with open(self.stepsPath, "r") as stepsFile:
            self._steps = stepsFile.read()

    def gcode(self):
        steps = parse(self._steps, Steps)

        output = StringIO.StringIO()
        output.write(self.content)

        for step in steps:
            process = step["process"]

            for process_step in process:
                output.write("\n".join(process_step.gcode()))
                output.write("\n")

        gcode = output.getvalue()
        output.close()

        return gcode

    def steps(self):
        if self._steps is None:
            with open(self.stepsPath, "r") as stepsFile:
                self._steps = stepsFile.read()

    def analysis(self):
        self.gcode_analysis.read(self.gcode().split("\n"), server.printerProfileManager.get_current_or_default())

        self.total_move_time_minute = self.gcode_analysis.totalMoveTimeMinute
        self.total_extrusion_amount = self.gcode_analysis.extrusionAmount

        return self.gcode_analysis.totalMoveTimeMinute, 
