import discord
from modules import memoryhandler

class CommandExists(Exception):
    pass

def if_global(command):
    try:
        memoryhandler.access(guild_id="global", mode='', category='commands', item=command, value=None)
        return True
    except KeyError:
        return False
    
def if_local(command, guild_id=None):
    try:
        memoryhandler.access(guild_id=guild_id, mode='rlocal', category='commands', item=command, value=None)
        return True
    except KeyError:
        return False

def if_unused(command, guild_id=None):
    if if_global(command) or if_local(command, guild_id):
        return False
    else: return True

def create(command, ctx=None, guild_id=None, **kwargs):
    if not if_unused(command, guild_id):
        raise CommandExists(f'{command} exists in dictionary!')
    if not 'json' in kwargs:
        json = {}
        items = ['content', 'embed']
        for item in items:
            try:
                json[item] = kwargs[item]
            except: pass
    if not json == {}:
        memoryhandler.access(guild_id=guild_id, mode='w*', category='commands', item=command, value=json)
    else: raise TypeError('JSON cannot be empty')

def load(command, ctx=None, guild_id=None, mode='r'):
    if not guild_id: guild_id = ctx.guild.id
    return memoryhandler.access(guild_id=guild_id, mode=mode, category='commands', item=command)