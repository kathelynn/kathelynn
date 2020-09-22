import json
def store(guild_id=None, mode='r', category=None, item=None, var=None):
    if 'r' in mode: # loads json on memory
        try:
            with open("allysaqt.json") as f: storage = json.load(f)
        except FileNotFoundError:
            print("If you'd like to run this bot, please follow the instructions found in README.md")

    if 'w' in mode: # saves json from memory
        with open("allysaqt.json", "w") as f:
            storage[guild_id][category][item] = var
            json.dump(storage, f)

    # for flexible use case: this would return value set in the function if nothing is found on json
    if item not in storage[guild_id][category]:
        if not var:  raise Exception('No default variable was set!')
        else: return var

    else: return storage[guild_id][category][item]