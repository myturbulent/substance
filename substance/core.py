import os
import logging
import yaml
from substance.shell import Shell
from substance.engine import Engine
from substance.utils import readYAML
from substance.exceptions import (
  FileSystemError,
  EngineNotFoundError,
  EngineExistsError
)

class Core(object):

  config = None
  defaultConfig = {"default": True}

  def __init__(self, configFile=None, basePath=None):
    self.basePath = os.path.abspath(basePath) if basePath else os.path.expanduser('~/.substance')
    self.enginesPath = os.path.join(self.basePath, "engines")

    self.configFile = configFile if configFile else "substance.yml"
    self.configFile = os.path.join(self.basePath, self.configFile)

  def assertPaths(self):
    Shell.makeDirectory(self.basePath)
    Shell.makeDirectory(self.enginesPath)

  def getBasePath(self):
    return self.basePath

  def getEnginesPath(self):
    return self.enginesPath

  def getConfigFile(self):
    return self.configFile

  def setConfigKey(self, key, value):
    if not self.config:
      self.readConfigFile()
    self.config[key] = value

  def getConfigKey(self, key):
    if not self.config:
      self.readConfigFile()
    return self.config.get(key, None)

  def getConfig(self):
    if not self.config:
      self.readConfigFile()
    return self.config

  def saveConfig(self, config=None):
    config = config or self.config
    try:
      with open(self.configFile, "w") as fileh:
        fileh.write(yaml.dump(config, default_flow_style=False))
    except Exception as err:
      raise FileSystemError("Failed to write configuration to %s : %s" % (self.configFile, err))

  def readConfigFile(self):
    if os.path.isfile(self.configFile):
      self.config = readYAML(self.configFile)
    else:
      logging.info("Generating default substance configuration in %s", self.configFile)
      self.saveConfig(self.defaultConfig)
    return self.config

  def getEngines(self):
    self.assertPaths()
    dirs = [d for d in os.listdir(self.enginesPath) if os.path.isdir(os.path.join(self.enginesPath, d))]
    return dirs

  def getEngine(self, name):
    self.assertPaths()
    enginePath = os.path.join(self.enginesPath, name)
    if not os.path.isdir(enginePath):
      raise EngineNotFoundError("Engine \"%s\" does not exist." % name)

    return Engine(name, enginePath)

  def createEngine(self, name, config=None, profile=None):
    self.assertPaths()
    enginePath = os.path.join(self.enginesPath, name)
    if os.path.isdir(enginePath):
      raise EngineExistsError("Engine \"%s\" already exists." % name)

    Shell.makeDirectory(enginePath)

    newEngine = Engine(name, enginePath)
    newEngine.generateDefaultConfig(config=config, profile=profile)

    return newEngine

  def removeEngine(self, name):
    self.assertPaths()
    enginePath = os.path.join(self.enginesPath, name)
    if not os.path.isdir(enginePath):
      raise EngineNotFoundError("Engine \"%s\" does not exist." % name)
    Shell.nukeDirectory(enginePath)

  def validDriver(self, driver):
    if driver is "VirtualBox":
      return True
