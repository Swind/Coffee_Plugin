# coding=utf-8
from __future__ import absolute_import

__author__ = "Swind Ou <swind@code-life.info>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License"

from coffee.coffee_blueprint import CookbookPlugin 
from coffee.coffee_startup import CoffeeStartUpPlugin 

__plugin_name__ = "Coffee Plugin"
__plugin_version__ = "0.1"
__plugin_description__ = "Coffee Printer"
__plugin_implementations__ = [CookbookPlugin()]
