# coding=utf-8
__author__ = "Swind Ou <swind@code-life.info>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'

from flask import request, jsonify, make_response, abort, Response
import re

import octoprint.util as util
from octoprint.filemanager.destinations import FileDestinations
from octoprint.settings import settings, valid_boolean_trues
from octoprint.server import printer, CookbookManager, eventManager, restricted_access, NO_CONTENT
from octoprint.server.api import api

import octoprint.util as util

COFFEE_FOLDER = "coffee"

@api.route("/coffee", methods=["GET"])
def ListCoffeeCookBooks():
    """
    Example:
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
            }
      } 
        }
    """
    files = coffeeManager.getAllFiles()
    return jsonify(files=files, free=util.getFreeBytes(settings().getBaseFolder(COFFEE_FOLDER)))

@api.route("/coffee/<string:cookbook_name>", methods=["GET"])
def GetCoffeeCookBook(cookbook_name):
    cookbook_data = coffeeManager.getFileData(cookbook_name)

    if cookbook_data is None:
        abort(404)

    return jsonify(files=[cookbook_data], free=util.getFreeBytes(settings().getBaseFolder(COFFEE_FOLDER)))

@api.route("/coffee/<string:cookbook_name>", methods=["PUT"])
def ReplaceCoffeeCookBook(cookbook_name):
    if not request.json or not 'steps' in request.json:
        abort(400)

    cookbook_data = coffeeManager.saveFile(cookbook_name, request.json["steps"])

    return jsonify(files=[cookbook_data], free=util.getFreeBytes(settings().getBaseFolder(COFFEE_FOLDER)))

@api.route("/coffee/<string:cookbook_name>", methods=["DELETE"])
def DeleteCoffeeCookBook(cookbook_name):
    file_path = coffeeManager.deleteFile(cookbook_name)

    if file_path is None:
        abort(404)
    
    return Response(None, 204)

