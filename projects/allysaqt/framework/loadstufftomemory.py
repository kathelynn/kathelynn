from . import formatting
import json
import asyncio

''' Loads config'''
def config(item):
    with open('config.json') as cfg:
        cfg = json.load(cfg)
        return cfg[item]

FILENAME = config('filename')

def loadfile(file):
    '''Loads the file'''
    try:
        with open(file) as handle:
            print('Disk read!')
            return json.load(handle)
    except FileNotFoundError:
        print("If you'd like to run this bot, please follow the instructions found in README.md")

MEMORY = loadfile(FILENAME)

def savefile(memory, file):
    '''Saves the file'''
    with open(file, 'w') as handle:
        print('Disk read!')
        json.dump(memory, handle, indent=4)
        print('Memory saved!')

def access(guild_id=None, category=None, item=None, value=None, mode=''):
    global MEMORY
    if isinstance(guild_id, int):
        guild_id = str(guild_id)

    if 'r' in mode:
        MEMORY = loadfile(FILENAME)

    if 'w' in mode:
        newdict = {guild_id: {category: {item: value}}}
        print(newdict)
        print(MEMORY)
        MEMORY = formatting.merge_dict(newdict, MEMORY)
        print(MEMORY)

    if 's' in mode:
        savefile(MEMORY, FILENAME)

    local_only = False
    if 'local' in mode:
        local_only = True

    if '*' in mode:
        try:
            MEMORY[guild_id][category]
            return MEMORY[guild_id][category]
        except KeyError:    
            if not local_only:
                return MEMORY["global"][category]
            raise KeyError(f'{category} does not exist')

    elif '-' not in mode:
        # TODO: rewrite to if statements
        try:
            MEMORY[guild_id][category][item]
            return MEMORY[guild_id][category][item]
        except KeyError:
            if value:
                return value
            if not local_only:
                return MEMORY["global"][category][item]
            raise KeyError("No default value was set!")

def prefix(bot=None, ctx=None, guild_id=None, mode='', prefix=None): # mode should be same as on storagehandler.store
    '''Prefix ??'''
    if not guild_id:
        guild_id = ctx.guild.id
    prefix = access(guild_id=guild_id, mode=mode,
                  category="settings", item="prefix", value=prefix)
    print(prefix)
    return prefix

async def autosave():
    '''Autosaves storage in case of power failure, etc.'''
    INTERVAL = config('autosaveinterval')*60
    while True:
        await asyncio.sleep(INTERVAL)
        access(mode='s-')