from __future__ import unicode_literals
from __future__ import print_function

from pypeg2 import *
import re

import itertools

import matplotlib.pyplot as plt
import numpy as np

from config import *
from unit import *


class Circle(Namespace):
    """
    Circle: 1 cm
        Water: 40 ml
        AvgWater: 0.01 ml
        Space: 0.1 mm
    """
    name = "circle"
    grammar = "Circle", ":", attr("radius", LengthItem), endl, indent(maybe_some([Space, Water, AvgWater]))

    prev_angle = 0

    def points(self, avg_water):
        circumference = 2 * np.pi * self.get_radius()
        space = self.get_space()
        water = self["water"].get_ml()
        steps = water / avg_water

        cylinder = round((space * steps) / circumference)

        av = 2 * np.pi * cylinder / steps

        step_range = np.arange(0.0, steps)

        x = self.get_radius() * np.cos(av * step_range)
        y = self.get_radius() * np.sin(av * step_range)
        z = avg_water

        return zip(x, y, itertools.repeat(z, len(x)))

    def __convert_to_mm(self, value, unit):
        if unit == "cm":
            return value * 10
        else:
            return value

    def get_radius(self):
        return self.__convert_to_mm(float(self.radius.value), self.radius.unit)

    def get_space(self):
        return self.__convert_to_mm(float(self["space"].value), self["space"].unit)

    def gcode(self):
        points = self.points(self["avgwater"].get_ml())

        lines = []
        for point in points:
            if self.get_radius() <= 5:
                template = "G1 X%.4f Y%.4f E%.4f F80"
            else:
                template = "G1 X%.4f Y%.4f E%.4f"

            tmp = template % point

            lines.append(tmp)

        return lines
