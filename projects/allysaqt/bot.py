'''Ally is a qt'''
testing = False
import asyncio
import discord
from discord.ext import commands
import framework # pylint:disable=import-error
from framework import loadstufftomemory # pylint:disable=import-error
MEMORY = loadstufftomemory.MEMORY

BOT = commands.Bot(command_prefix=loadstufftomemory.prefix)

@BOT.event
async def on_ready():
    '''Runs when the bot connects to discord'''
    print(f'Logged on as {BOT.user}!')
    await loadstufftomemory.autosave()

@BOT.event
async def on_message(message):
    '''Runs when the bot logs a message'''
    print('{0.author} from {0.channel}: {0.content}'.format(message))
    await BOT.process_commands(message)

REACTIONS = {}

@BOT.event
async def on_reaction_add(reaction, user):
    '''Runs when a reaction is added'''
    if reaction.message.author == BOT.user:
        dictionary = {str(reaction.message.channel.id): {str(user.id): reaction.emoji}}
        print(dictionary)
        framework.formatting.merge_dict(dictionary, REACTIONS)
        await asyncio.sleep(30)
        if REACTIONS[str(reaction.message.channel.id)][str(user.id)] == reaction:
            del REACTIONS[str(reaction.message.channel.id)][str(user.id)]

EMBED_TIMEOUT = loadstufftomemory.config('embedtimeout')
EMBED_TICKRATE = loadstufftomemory.config('embedtickrate')

print(EMBED_TIMEOUT)
print(EMBED_TICKRATE)

async def interactive_reaction(ctx, message, buttons):
    '''Makes reactions on messages interactive'''
    for i in range(0, len(buttons)):
        await message.add_reaction(buttons[i])
    await message.add_reaction('❎')

    channel_reactions = REACTIONS[str(ctx.channel.id)]
    secs = 1/EMBED_TICKRATE
    for i in range(0, EMBED_TIMEOUT * EMBED_TICKRATE):
        if str(ctx.author.id) in channel_reactions:
            if channel_reactions[str(ctx.author.id)] in buttons:
                reaction = buttons.index(channel_reactions[str(ctx.author.id)])
                del REACTIONS[str(ctx.channel.id)][str(ctx.author.id)]
                return reaction, None
            elif REACTIONS[str(ctx.channel.id)][str(ctx.author.id)] == '❎':
                del REACTIONS[str(ctx.channel.id)][str(ctx.author.id)]
                return -1, 'cancelled'
        await asyncio.sleep(secs)
    return -1, 'timeout'

@BOT.event
async def on_command_error(ctx, error):
    '''To check if the command is a runtime command'''
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
    else:
        embed = discord.Embed.from_dict({"title":"⚠️ Error", "description":str(error), "color":16711680})
        await ctx.send(embed=embed)
        raise error

import math, datetime
@BOT.command()
async def ping(ctx):
    '''Ping command'''
    embed = discord.Embed.from_dict({"title": '🏓 Pong!', "color": 2896440, "fields": [{"name": "Latency",
                                    "value": f"{math.floor((int(datetime.datetime.utcnow().strftime('%f')) - int(ctx.message.created_at.strftime('%f')))/1000)}ms"}]})
    await ctx.send(embed=embed)

@BOT.command(aliases=['setting', 'set'])
async def settings(ctx, arg=None, arg2=None):
    '''Settings command'''
    permission_error = lambda arg, perm: f"Sorry, you need `{perm}` permission to access `{arg}` setting."
    author_permissions = ctx.author.guild_permissions
    guild = ctx.guild
    pfx = framework.loadstufftomemory.prefix(guild_id=guild.id)

    author = {'name': guild.name, 'icon_url': str(guild.icon_url)}
    title = '⚙️ Settings'
    description = f"`prefix`: `{framework.loadstufftomemory.prefix}`"
    color = 2896440

    if arg == 'prefix':
        title = f'{title} > Prefix'
        description = f"Prefix for `{guild.id}`: `{pfx}`"
        if arg2:
            if not author_permissions.manage_guild:
                # 'Guild' is 'Server' in Discord UX context
                description = permission_error('prefix', 'Manage Server')
                color = 16711680
            elif len(arg2) > 3:
                description += f"\nSorry! `{arg2}` is {framework.formatting.plurality(len(arg2) - 3, 'character')} too long."
                color = 16711680
            else:
                pfx = framework.loadstufftomemory.prefix(guild_id=guild.id, mode='w', prefix=arg2)
                description += f"> `{pfx}`\nBot prefix has been changed!"
                color = 65280

    embed = framework.formatting.make_dict(embed={"title": title, "description": description,
                                                "color": color, "author": author})
    await ctx.send(**framework.formatting.json_embed(embed))

@BOT.command(aliases=['ccommands', 'cc'])
async def customcommands(ctx, arg=None, path='00'):
    '''Custom commands command'''
    end = False
    while not end:
        choices = None
        buttons = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        guild = ctx.guild
        prefix = framework.loadstufftomemory.prefix(guild_id=guild.id)

        author = {'name': guild.name, 'icon_url': str(guild.icon_url)}
        title = 'Custom Commands'
        description = None
        fields = None
        footer = None
        color = 800868

        if not arg:
            fields = [{'name': f'`{prefix}{ctx.invoked_with} create`', 'value':'Initialize embed creation tool'}]
        if arg == 'create':
            title = f'{title} > Create'
            description = "Work in Progress\n`1.` Foo\n`2.` Bar"
            choices = ['a', 'b0']

            if path == 'cancelled':
                description = 'Operation cancelled.'
                color = 16711680
                end = True
            if path == 'timeout':
                description = 'Timeout exceeded. Please try again'
                color = 16711680
            if path[0] == 'a':
                description = 'End'
                end = True
            elif path[0] == 'b':
                description = "Work in progress\n`1.` Foobar\n`2.` Barfoo"
                choices = ['ba', 'bb']
                if path[1] == 'a':
                    description = "Foobar picked!"
                    end = True
                if path[1] == 'b':
                    description = "Barfoo picked!"
                    end = True

        embed_JSON = {}    
        for embed in ['title', 'description', 'color', 'footer', 'author', 'fields']:
            value = locals()[embed]
            if value:
                embed_JSON[embed] = value
            
        embed = discord.Embed.from_dict({"title": title, "description":description, "color": color,
                                        "footer": footer, "author": author, "fields":fields})

        try:
            botmsg
            #await botmsg.edit(**modules.formatting.json_embed(embed))
            await botmsg.clear_reactions()
            await botmsg.edit(embed=embed)
        except NameError:
            botmsg = await ctx.send(embed=embed)
            #await ctx.send(**modules.formatting.json_embed(embed))

        if choices and not end:
            path_result, embed_error = await interactive_reaction(ctx, botmsg, buttons[:len(choices)])
            if embed_error:
                path_result = embed_error
            else:
                path_result = choices[path_result]
            path = path_result

# '''For modules'''
# from os import listdir, getcwd
# from os.path import isfile, join
# modules = [f for f in listdir(f"{getcwd()}/modules") if isfile(join(f"{getcwd()}/modules", f))]
# modules.remove('__init__.py')
# for x in range(0, len(modules)):
#     modules[x] = modules[x][:len(modules[x])-3]
#     print(modules[x])
# print(modules)
# loadedmodule = []
# for module in modules:
#     try:
#         exec(f"from modules import {module}")
#         globals()[module].setup(BOT)
#         loadedmodule.append(module)
#     except Exception as e:
#         print(e)
# print(f"Modules loaded: {[module for module in loadedmodule]}")

TOKEN = loadstufftomemory.config('token')
import atexit
atexit.register(loadstufftomemory.access, **{'mode':'s-'})
BOT.run(TOKEN)