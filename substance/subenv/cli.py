import sys
import logging
from importlib import import_module
from substance import (Program, Core)
from substance.subenv import SubenvAPI

class SubenvCLI(Program):
  """Subenv CLI command"""

  def __init__(self):
    super(SubenvCLI, self).__init__()

  def getShellOptions(self, optparser):
    optparser.add_option("-d", '--debug',  dest="debug", help="Activate debugging output", default=False, action="store_true")
    optparser.add_option('-y', "--yes", dest="assumeYes", help="Assume yes when prompted", default=False, action="store_true")
    optparser.add_option('-b', '--base', type="str", dest="base", help="Path to the base", default="/substance")
    return optparser

  def getUsage(self):
    return "subenv [options] COMMAND [command-options]"

  def getHelpTitle(self):
    return "Initialize a substance project environment"

  def setupCommands(self):
    self.addCommand('ls', 'substance.subenv.command.ls')
    self.addCommand('init', 'substance.subenv.command.init')
    self.addCommand('delete', 'substance.subenv.command.delete')
    self.addCommand('use', 'substance.subenv.command.use')

  def initCommand(self, command):
    core = Core()
    if self.getOption('assumeYes'):
      core.setAssumeYes(True)
    command.core = core

    api = SubenvAPI(self.getOption('base'))
    command.api = api

    return command


def cli():
  args = sys.argv
  args.pop(0)

  prog = SubenvCLI()
  prog.execute(args)