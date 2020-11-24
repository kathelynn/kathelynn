VERSION = 0.1
import discord
from discord.ext import commands
import sys
from os import getcwd
from os.path import dirname
sys.path.insert(1, dirname(getcwd()))
from allysaqt import framework

def setup():
    pass
#BOT = commands.Bot(command_prefix=framework.loadstufftomemory.prefix)