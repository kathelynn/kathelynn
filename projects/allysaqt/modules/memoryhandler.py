'''Memoryhandler'''
import json
from . import formatting
FILENAME = 'allysaqt.json'

def loadfile(file):
    '''Loads the file'''
    try:
        with open(file) as handle:
            print('Disk read!')
            return json.load(handle)
    except FileNotFoundError:
        print("If you'd like to run this bot, please follow the instructions found in README.md")

MEMORY = loadfile(FILENAME)

def access(guild_id=None, category=None, item=None, value=None, mode=''):
    '''???'''
    if isinstance(guild_id, int):
        guild_id = str(guild_id)

    if 'w' in mode:
        with open(FILENAME, 'w') as file:
            newdict = {guild_id: {category: {item: value}}}
            formatting.merge_dict(newdict, MEMORY)
            json.dump(MEMORY, file, indent=4)

    local_only = False
    if 'local' in mode:
        local_only = True

    if '*' in mode:
        try:
            # TODO: rewrite to if statements
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

def grabtoken():
    '''Gets the token'''
    with open('discord_token.json') as discord_token:
        return json.load(discord_token)
