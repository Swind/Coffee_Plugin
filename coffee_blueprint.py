# coding=utf-8
from __future__ import absolute_import

__author__ = "Swind Ou <swind@code-life.info>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License"

import os

import flask
from flask import jsonify, Response, render_template, abort

import octoprint.plugin
from octoprint.filemanager.destinations import FileDestinations

from coffee.parser.cookbook import Cookbook

class CookbookPlugin(octoprint.plugin.BlueprintPlugin,
                     octoprint.plugin.StartupPlugin):
    COOKBOOK_FOLDER = "cookbooks"

    # ========================================================
    #
    # Startup Plugin Interface
    #
    # ========================================================
    def on_after_startup(self):
        from octoprint.filemanager import extensions
        # Append cookbook file type to local storage manager
        extensions["coffee"] = {
                "cookbook": ["cookbook"]
        }

        from octoprint.filemanager import all_extensions
        all_extensions.append("cookbook")


        self._file_manager.add_folder(FileDestinations.LOCAL, self.COOKBOOK_FOLDER)

    # ========================================================
    #
    # Blueprint Plugin Interface
    #
    # ========================================================
    """
    Cookbook Resource:

    {
        "name": "spiral.coffee", 
        "size": 1468987,
        "date": 1378847754,
        "refs": {
            "resource": "http://example.com/api/files/local/whistle_v2.gcode",
            "download": "http://example.com/downloads/files/local/whistle_v2.gcode" 
        },
        "gcodeAnalysis": {
            "estimatedPrintTime": 1188,
            "filament": {
              "length": 810,
              "volume": 5.36
            }
        },
        "print": {
            "failure": 4,
            "success": 23,
            "last": {
             "date": 1387144346,
             "success": true
        },
        "content": "Step 1 ..."
    } 
    """
    def is_blueprint_protected(self):
        return False

    def __get_file_path(self, name):
        return self._file_manager.sanitize_path(FileDestinations.LOCAL, self.COOKBOOK_FOLDER + "/" + name)

    def __list_cookbooks(self):
        files = self._file_manager.list_files(FileDestinations.LOCAL, self.COOKBOOK_FOLDER, filter=None, recursive=True)["local"]

        for name, metadata in files.items():
            if metadata["type"] == "coffee":
                gcode_name = name + ".gcode"

                # Merge gcode metadata to cookbook 
                gcode_metadata = files.get(gcode_name)
                if gcode_metadata is not None:
                    metadata["analysis"] = gcode_metadata["analysis"]
                    del files[gcode_name]

                # Read cookbook content from file
                sanitize_path = self.__get_file_path(name)
                
                with open(sanitize_path, "r") as cookbook_file:
                    metadata["content"] = cookbook_file.read() 

                # Remove ".cookbook" from the key name in the dict
                files[name.replace(".cookbook", "")] = metadata
                del files[name]

        return files

    @octoprint.plugin.BlueprintPlugin.route("/", methods=["GET"])
    def index(self):
        return render_template("coffee_index.jinja2")

    @octoprint.plugin.BlueprintPlugin.route("/cookbooks", methods=["GET"])
    def list_cookbooks(self):
        return jsonify(self.__list_cookbooks())

    @octoprint.plugin.BlueprintPlugin.route("/cookbooks/<string:name>", methods=["GET"])
    def get_cookbook(self, name):
        files = self.__list_cookbooks()

        if name in files:
            return jsonify(files[name])
        else:
            abort(404)

    @octoprint.plugin.BlueprintPlugin.route("/cookbooks/<string:name>", methods=["PUT"])
    def update_cookbook(self, name):
        name = name + ".cookbook"

        from flask import request
        content = request.data
        
        sanitize_path = self.__get_file_path(name)

        # Generate gcode file
        cookbook = Cookbook(name, content)
        gcode = cookbook.gcode()

        self._file_manager.add_file(FileDestinations.LOCAL, os.path.join(self.COOKBOOK_FOLDER, name), cookbook, allow_overwrite=True)
        self._file_manager.add_file(FileDestinations.LOCAL, os.path.join(self.COOKBOOK_FOLDER, name + ".gcode"), gcode, allow_overwrite=True)

        return Response(None, status=201)

    @octoprint.plugin.BlueprintPlugin.route("/cookbooks/<string:name>", methods=["DELETE"])
    def delete_cookbook(self, name):
        name = name + ".cookbook"

        self._file_manager.remove_file(FileDestinations.LOCAL, os.path.join(self.COOKBOOK_FOLDER, name))
        self._file_manager.remove_file(FileDestinations.LOCAL, os.path.join(self.COOKBOOK_FOLDER, name + ".gcode"))

        return Response(None, status=202)
