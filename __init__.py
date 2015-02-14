# coding=utf-8
from __future__ import absolute_import

__author__ = "Swind Ou <swind@code-life.info>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License"

#########################################################################################################
#
#   Plugin Settings 
#
#########################################################################################################
import octoprint.plugin

default_settings = {
        "coffee_folder": "coffee"
}
s = octoprint.plugin.plugin_settings("coffee", defaults = default_settings)
print s

#########################################################################################################
#
#   Flask Blueprint
#
#########################################################################################################
import os

import flask
from flask import jsonify, Response, render_template

import octoprint.util as util
from octoprint.settings import settings

from .coffeefiles import CoffeeManager

template_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
coffee_blueprinter = flask.Blueprint("plugin.coffee", __name__, template_folder=template_folder)
coffeeManager = CoffeeManager()
COFFEE_FOLDER = "coffee"

@coffee_blueprinter.route("/", methods=["GET"])
def index():
    return render_template("coffee_index.jinja2") 

@coffee_blueprinter.route("/cookbooks", methods=["GET"])
def ListCoffeeCookBooks():
    files = coffeeManager.getAllFiles()
    return jsonify(files=files, free=util.getFreeBytes(settings().getBaseFolder("plugins")))

@coffee_blueprinter.route("/cookbooks/<string:cookbook_name>", methods=["GET"])
def GetCoffeeCookBook(cookbook_name):
    cookbook_data = coffeeManager.getFileData(cookbook_name)

    if cookbook_data is None:
        abort(404)

    return jsonify(files=[cookbook_data], free=util.getFreeBytes(settings().getBaseFolder(COFFEE_FOLDER)))

@coffee_blueprinter.route("/cookbooks/<string:cookbook_name>", methods=["PUT"])
def ReplaceCoffeeCookBook(cookbook_name):
    if not request.json or not 'steps' in request.json:
        abort(400)

    cookbook_data = coffeeManager.saveFile(cookbook_name, request.json["steps"])

    return jsonify(files=[cookbook_data], free=util.getFreeBytes(settings().getBaseFolder(COFFEE_FOLDER)))

@coffee_blueprinter.route("/cookbooks/<string:cookbook_name>", methods=["DELETE"])
def DeleteCoffeeCookBook(cookbook_name):
    file_path = coffeeManager.deleteFile(cookbook_name)

    if file_path is None:
        abort(404)
    
    return Response(None, 204)

#########################################################################################################
#
#   Coffee Plugin 
#
#########################################################################################################
class CoffeePlugin(octoprint.plugin.BlueprintPlugin,
                   octoprint.plugin.AssetPlugin,
                   octoprint.plugin.SettingsPlugin):
    def __init__(self):
        pass

    ##~~ BlueprintPlugin API
    def get_blueprint(self):
            global coffee_blueprinter
            return coffee_blueprinter

    def is_blueprint_protected(self):
        return False

    ##~~ SettingsPlugin API
    def on_settings_load(self):
            return dict(
                    coffee_folder=s.get(["coffee_folder"])
            )

    def on_settings_save(self, data):
        if "coffee_folder" in data and data["coffee_folder"]:
            s.set(["coffee_folder"], data["coffee_folder"])

    ##~~ AssetPlugin API

    def get_asset_folder(self):
            import os
            return os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")

    def get_assets(self):
            return {
                    "js": ["js/mithril.js", "js/semantic.js"],
                    #"less": ["less/cura.less"],
                    "css": ["css/semantic.css"]
            }

__plugin_name__ = "Coffee Plugin"
__plugin_version__ = "0.1"
__plugin_description__ = "Coffee Printer"
__plugin_implementations__ = [CoffeePlugin()]

