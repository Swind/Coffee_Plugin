from __future__ import unicode_literals
from __future__ import print_function

from pypeg2 import Namespace, List
from pypeg2 import endl, maybe_some, indent, some, name, parse, indent

from config import Time, Temperature

from spiral import Spiral
from circle import Circle
from origin import Origin

###################################################################################
#
#   Process
#
###################################################################################

class Waitting(Namespace):
    name = "waitting"
    grammar = "Waitting", ":", endl, indent(some(Time))

    def gcode(self):
        return ["\n", "G4 " + "S" + str(self["time"].get_seconds()), "\n"]


class Process(List):
    name = "process"
    grammar = "Process", ":", endl, indent(maybe_some([Origin, Spiral, Waitting, Circle]))

