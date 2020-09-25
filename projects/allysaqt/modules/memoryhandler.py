import json
from modules import formatting
filename = 'allysaqt.json'

def loadfile(file):
    try:
        with open(file) as file:
            print('Disk read!')
            return json.load(file)
    except FileNotFoundError:
        print("If you'd like to run this bot, please follow the instructions found in README.md")

memory = loadfile(filename)

def access(guild_id=None, category=None, item=None, value=None, mode=''):

    if isinstance(guild_id, int):
        guild_id = str(guild_id)

    if 'w' in mode:
        with open(filename, 'w') as file:
            newdict = {guild_id: {category: {item: value}}}
            formatting.merge_dict(newdict, memory)
            json.dump(memory, file, indent=4)
        
    local_only = False
    if 'local' in mode:
        local_only = True

    if '*' in mode: 
        try:
            memory[guild_id][category]
            return memory[guild_id][category]
        except KeyError:
            if not local_only:
                return memory["global"][category]
            raise KeyError(f'{category} does not exist')

    elif '-' not in mode:
        try:
            memory[guild_id][category][item]
            return memory[guild_id][category][item]
        except KeyError:
            if value:
                return value
            if not local_only:
                return memory["global"][category][item]
            raise KeyError("No default value was set!")

def grabtoken():
    with open('discord_token.json') as discord_token:
        return json.load(discord_token)