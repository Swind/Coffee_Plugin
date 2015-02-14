from __future__ import unicode_literals

from pypeg2 import Keyword, Enum, K

##################################################################################
#
# Unit
#
##################################################################################
def Unit(class_name, keywords):
    return type(
           str(class_name),
           (Keyword, ),
           dict({
                "grammar": Enum(*[K(keyword) for keyword in keywords])
                })
            )

TimeUnit = Unit("TimeUnit", ["min", "sec"])
LengthUnit = Unit("LengthUnit", ["cm", "mm"])
TemperatureUnit = Unit("TemperatureUnit", ["C", "F"])
CapacityUnit = Unit("CapacityUnit", ["l", "ml"])
