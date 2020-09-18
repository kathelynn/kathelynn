## To be used for error checking
def p(a):
    print(a)

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import json
#from customcommands import *

## Prefix storage module, will be used later for storing different kinds of things outside just prefixes
def store(guild_id=None, mode='r', category=None, item=None, var=None):
    if 'r' in mode:
        try:
            with open("allysaqt.json") as f:
                storage = json.load(f)
        except FileNotFoundError:
            print("If you'd like to run this bot, please follow the instructions found in README.md")

    if 'w' in mode:
        with open("allysaqt.json", "w") as f:
            storage[guild_id][category][item] = var
            json.dump(storage, f)

    if guild_id not in storage:
        if not var: 
            raise Exception('No default variable was set!')
        else: return var
    else: 
        return storage[guild_id][category][item]

## Embed module, to be used for making embeds with one line of code
async def action_embed(message, args=None, **kwargs):
    embed = discord.Embed(**kwargs)
    if 'authorName' in args:
        embed.set_author(name=args['authorName'])
    if 'authorIcon' in args:
        embed.set_author(name=args['authorName'], icon_url=args['authorIcon'])
    if 'imageURL' in args:
        embed.set_image(url=args['imageURL'])
    await message.send(embed=embed)

## For action embeds when multiple people are in
def group(*args):
    args = ', '.join(list(*args[:len(*args)]))
    args = f'{args}, and {str(*args[len(*args):])}'
    return args

def set_prefix(bot=None, message=None, guild_id=None, mode='r', prefix='a$'):
    if not guild_id: guild_id = message.guild.id
    if isinstance(guild_id, int):
        guild_id = str(guild_id)
    return store(guild_id, mode, category="settings", item="prefix", var=prefix)

def check():
    pass

def create():
    pass

##############
###COMMANDS###
##############
bot = commands.Bot(command_prefix=set_prefix)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    channel = bot.get_channel(754172127019794513)
    await channel.send('I am awake~')
    #while True:
    #    text = input('> ')
    #    if not text[0] == '#':
    #        await channel.send(text)
    #    else:
    #        for guild in client.guilds:
    #            channel = discord.utils.get(guild.text_channels, name=text[1:])
    #            if channel == None:
    #                print('Channel does not exist')
    #            else: print(f"Moved to #{channel.name} in '{channel.guild}'")

@bot.event
async def on_message(message):
        print('{0.author} from {0.channel}: {0.content}'.format(message))
        await bot.process_commands(message)

@bot.command(aliases=['hi'])
async def hello(ctx):

    await ctx.send(f'Hello, <@{ctx.author.id}> qtpi!')

@bot.command()
async def say(ctx, *args):
    if args == ():
        await ctx.send('What should I say, qtpi?')
    else: await ctx.send(' '.join(args))

@bot.command(aliases=['ccommands', 'cc'])
async def customcommands(ctx):
    guild = ctx.guild
    header = {'authorName': guild.name, 'authorIcon': guild.icon_url}
    title = 'Custom Commands'
    description = "Work in Progress\n`1.` Foo\n`2.`Bar"
    footer = None
    color = 800868

    await action_embed(ctx, header, title=title, description=description, color=color, footer=footer)

@bot.command(aliases=['set'])
async def settings(ctx, arg=None, arg2=None):
    guild = ctx.guild
    pf = set_prefix(guild_id=guild.id)

    header = {'authorName': guild.name, 'authorIcon': guild.icon_url}
    title = 'Settings'
    description = f"`prefix`: `{pf}`"
    color = 2896440

    if arg == 'prefix':
        title = 'Settings > Prefix'
        description = f"Prefix for `{guild.id}`: `{pf}`"
        if arg2:
            if len(arg2) > 2:
                description=f"Prefix for `{guild.id}`: `{pf}`\nSorry! `{arg2}` is `{len(arg2) - 2}` character(s) too long."
                color = 16711680
            else:
                prefix = set_prefix(guild_id=guild.id, mode='rw', prefix=arg2)
                description = f"{description} > `{prefix}`"

    await action_embed(ctx, header, title=title, description=description, color=color)

@settings.error
async def settings_error(error, ctx):
    if isinstance(error, MissingPermissions):
        description = f"Sorry, {ctx.author}! You do not have permission to access settings"
        color = 16711680
        await action_embed(ctx, description=description, color=color)

## To run the bot, you need to change the arguments inside bot.run with a string of your bot token, or try to
## create a 'discord_token.json' file with the name and token inside the dictionary.
with open('discord_token.json') as discord_token:
    token = json.load(discord_token)
bot.run(token["allysaqt"])