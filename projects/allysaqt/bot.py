'''Ally is a qt'''
testing = False
import asyncio
import discord
from discord.ext import commands
import framework # pylint:disable=import-error

BOT = commands.Bot(command_prefix=framework.loadstufftomemory.prefix)

@BOT.event
async def on_ready():
    '''Runs when the bot connects to discord'''
    print(f'Logged on as {BOT.user}!')
    await framework.loadstufftomemory.autosave()

@BOT.event
async def on_message(message):
    '''Runs when we get a message to log it'''
    print('{0.author} from {0.channel}: {0.content}'.format(message))
    await BOT.process_commands(message)

REACTIONS = {}

@BOT.event
async def on_reaction_add(reaction, user):
    '''Runs when a reaction gets added'''
    if reaction.message.author == BOT.user:
        dictionary = {str(reaction.message.channel.id): {str(user.id): reaction.emoji}}
        framework.formatting.merge_dict(dictionary, REACTIONS)
        await asyncio.sleep(30)
        del REACTIONS[str(reaction.message.channel.id)][str(user.id)]

@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        content = ctx.message.content[len(ctx.prefix):].split()
        if isinstance(content, list):
            content[0].lower()
        else:
            content.lower()
        
        ### temporary for now
        embed = discord.Embed.from_dict({"title":"Error", "description":str(error), "color":16711680})
        await ctx.send(embed=embed)

        try:
            pass
        except:
            pass
    elif isinstance(error, discord.errors.Forbidden):
        pass
    else:
        embed = discord.Embed.from_dict({"title":"⚠️ Error", "description":str(error), "color":16711680})
        await ctx.send(embed=embed)

import math, datetime
@BOT.command()
async def ping(self, ctx):
    embed = discord.Embed.from_dict({"title": '🏓 Pong!', "color": 2896440, "fields": [{"name": "Latency",
                                    "value": f"{math.floor((int(datetime.datetime.utcnow().strftime('%f')) - int(ctx.message.created_at.strftime('%f')))/1000)}ms"}]})
    await ctx.send(embed=embed)

'''For modules'''
from os import listdir, getcwd
from os.path import isfile, join
modules = [f for f in listdir(f"{getcwd()}/modules") if isfile(join(f"{getcwd()}/modules", f))]
modules.remove('__init__.py')
for x in range(0, len(modules)):
    modules[x] = modules[x][:len(modules[x])-3]
    print(modules[x])
print(modules)
loadedmodule = []
for module in modules:
    try:
        exec(f"from modules import {module}")
        globals()[module].setup(BOT)
        loadedmodule.append(module)
    except Exception as e:
        print(e)
print(f"Modules loaded: {[module for module in loadedmodule]}")

# To run the bot, you need to change the arguments inside bot.run
# with a string of your bot token, or try to ##
# create a 'discord_token.json' file with the name and token inside the dictionary.
TOKEN = framework.loadstufftomemory.config('token')
import atexit
atexit.register(framework.loadstufftomemory.access, **{'mode':'s-'})
BOT.run(TOKEN)