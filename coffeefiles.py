# coding=utf-8
import re

__author__ = "Swind Ou<swind@code-life.info>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'

import os
import Queue
import threading
import yaml
import time
import logging
import octoprint.util as util

from octoprint.settings import settings
from octoprint.events import eventManager, Events
from octoprint.filemanager.destinations import FileDestinations

from werkzeug.utils import secure_filename

class CookbookManager(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._settings = settings()
        self._cookbookFolder = os.path.join(self._settings.getBaseFolder("plugins"), "coffee/cookbooks")

    def _getBasicFilename(self, filename):
            if filename.startswith(self._cookbookFolder):
                    return filename[len(self._cookbookFolder + os.path.sep):]
            else:
                    return filename

    def getAbsolutePath(self, filename, mustExist=True):
            filename = self._getBasicFilename(filename)
            
            # TODO: detect which type of file and add in the extra folder portion 
            secure = os.path.join(self._cookbookFolder, secure_filename(self._getBasicFilename(filename)))

            if mustExist and (not os.path.exists(secure) or not os.path.isfile(secure)):
                    return None

            return secure

    def getFileData(self, filename):
            if not filename:
                    return

            filename = self._getBasicFilename(filename)

            absolutePath = self.getAbsolutePath(filename)
            if absolutePath is None:
                    return None

            statResult = os.stat(absolutePath)
            fileData = {
                    "name": filename,
                    "size": statResult.st_size,
                    "origin": FileDestinations.LOCAL,
                    "date": int(statResult.st_ctime)
            }

            return fileData

    def getAllFiles(self):
        files = []

        for osFile in os.listdir(self._cookbookFolder):
            fileData = self.getFileData(osFile)

            if fileData is not None:
                files.append(fileData)

        return files

    def saveFile(self, filename, steps):
        filename = self._getBasicFilename(filename)
        absolutePath = self.getAbsolutePath(filename, mustExist=False)

        with open(absolutePath, "w") as cookbookFile:
            cookbookFile.write(steps)

        return self.getFileData(filename)

    def deleteFile(self, filename):
        filename = self._getBasicFilename(filename)
        absolutePath = self.getAbsolutePath(filename)

        if absolutePath is None:
            return None

        os.remove(absolutePath)
        return absolutePath
