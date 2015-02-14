from __future__ import unicode_literals

import re

from pypeg2 import Namespace, List
from pypeg2 import attr, maybe_some, endl

from unit import TemperatureUnit, LengthUnit, CapacityUnit, TimeUnit

##################################################################################
#
#   Config Item in Step
#
##################################################################################
def value(): return attr("value", re.compile(r"[0-9\\.]+"))
def ConfigItem(class_name, unit_class, with_endl=True):

    grammar = (class_name, ":", value(), attr("unit", unit_class), endl)

    return type(
            str(class_name),
            (Namespace, ),
            dict({
                "grammar" : grammar,
                "name" : str(class_name).lower()
                })
            )

Temperature = ConfigItem("Temperature", TemperatureUnit)
Radius = ConfigItem("Radius", LengthUnit)
Length = ConfigItem("Length", LengthUnit)
Space = ConfigItem("Space", LengthUnit)
Distance = ConfigItem("Distance", LengthUnit)
Cylinder = ConfigItem("Cylinder", None)
Interval = ConfigItem("Interval", LengthUnit)
Water = ConfigItem("Water", CapacityUnit)
AvgWater = ConfigItem("AvgWater", CapacityUnit)

def get_ml(self):
    if self.unit == "l":
        return float(self.value) * 1000
    else:
        return float(self.value)

Water.get_ml = get_ml
AvgWater.get_ml = get_ml

class LengthItem(Namespace):
    grammar = value(), attr("unit", LengthUnit)

class TimeItem(Namespace):
    grammar = value(), attr("unit", TimeUnit)

class Time(List):
    name = "time"
    grammar = "Time", ":", maybe_some(TimeItem), endl

    def get_seconds(self):
        seconds = 0

        for item in self:
            if item.unit == "min":
                seconds = seconds + float(item.value) * 60
            else:
                seconds = seconds + float(item.value)

        return int(seconds)

