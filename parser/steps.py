from __future__ import unicode_literals
from __future__ import print_function

from pypeg2 import Namespace, List
from pypeg2 import endl, maybe_some, indent, some, name, parse, indent

from config import Time, Temperature
from process import Process

###################################################################################
#
#   Step
#
###################################################################################
def step_config():
    return [Temperature, Process]


class Step(Namespace):
    grammar = "Step:", name(), endl, indent(maybe_some(step_config()))


class Steps(List):
    grammar = maybe_some(Step)

