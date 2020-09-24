# pylint: disable=used-before-assignment
import json
def store(guild_id=None, mode='r', category=None, item=None, var=None): # mode should be blank '', but 'r' is used for debugging purposes
    if isinstance(guild_id, int):
        guild_id = str(guild_id)
        
    if 'r' in mode: # loads json on memory
        try:
            with open("allysaqt.json") as f: storage = json.load(f)
        except FileNotFoundError:
            print("If you'd like to run this bot, please follow the instructions found in README.md")
            exit()
    #else:
    #    try: storage
    #    except NameError:
    #        storage = store(mode='r*')

    if 'w' in mode: # saves json from memory
        with open("allysaqt.json", "w") as f:
            storage[guild_id][category][item] = var
            json.dump(storage, f)

    local = False
    if 'local' in mode: local = True 

    if '*' in mode: return storage
    elif '-' not in mode:
        # for flexible use case: in case of fallback where variable is 
        try:
            storage[guild_id][category][item]
            return storage[guild_id][category][item]
        except KeyError:
            if var:
                return var
            else:
                if not local:
                    return storage["global"][category][item]
                else:
                    raise KeyError('No default variable was set!')