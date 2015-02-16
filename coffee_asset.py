# coding=utf-8
from __future__ import absolute_import

__author__ = "Swind Ou <swind@code-life.info>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License"

import os
import octoprint.plugin

class CoffeeAssestPlugin(octoprint.plugin.AssetPlugin): 

    def get_asset_folder(self):
        return os.path.join(self._basefolder, "static")
