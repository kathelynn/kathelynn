import sys
from os import getcwd
from os.path import dirname
sys.path.insert(1, dirname(getcwd()))
from allysaqt import framework
from discord.ext import commands
BOT = commands.Bot(command_prefix=framework.loadstufftomemory.prefix)