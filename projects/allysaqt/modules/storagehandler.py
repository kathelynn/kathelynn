# pylint: disable=used-before-assignment
import json
def store(guild_id=None, mode='', category=None, item=None, var=None):

    if isinstance(guild_id, int):
        guild_id = str(guild_id)
        
    if 'r' in mode: # loads json on memory
        try:
            with open("allysaqt.json") as f: storage = json.load(f)
        except FileNotFoundError:
            print("If you'd like to run this bot, please follow the instructions found in README.md")
    else:
        try: storage
        except UnboundLocalError:
            storage = store(mode='r*')

    if 'w' in mode: # saves json from memory
        with open("allysaqt.json", "w") as f:
            storage[guild_id][category][item] = var
            json.dump(storage, f)

    local = False
    if 'local' in mode: local = True 

    if '*' in mode: return storage
    elif '-' not in mode:
        # for flexible use case: in case of fallback where variable is 
        try: storage[guild_id][category][item]
        except KeyError:
            if not var:
                if storage["global"][category][item] and not local:
                    return storage["global"][category][item]
                else: raise KeyError('No default variable was set!')
            else: return var
        else: return storage[guild_id][category][item]