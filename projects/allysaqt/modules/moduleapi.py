import sys
from os import getcwd
from os.path import dirname
sys.path.insert(1, dirname(getcwd()))
from allysaqt.bot import BOT
from allysaqt import framework

BOT = BOT