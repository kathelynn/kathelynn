## To be used for error checking
def p():
    global n
    try: n += 1
    except NameError: n = 1
    print(n)
    
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import json

def setPrefix(bot=None, message=None, mode='r', prefix=None):
    global prefixes
    guild_id = str(message.guild.id) # json only supports string for name

    if 'r' in mode:
        try:
            with open("prefixes.json") as f:
                prefixes = json.load(f)
        except FileNotFoundError:
            with open("prefixes.json", "x") as f:
                prefixes = {"692647317425094686": "$"}
                json.dump(prefixes, f)

    if 'w' in mode:
        with open("prefixes.json", "w") as f:
            if guild_id not in prefixes:
                setPrefix(message=message, mode='w', prefix=prefix)
            else: prefixes[guild_id] = prefix
            json.dump(prefixes, f)

    if guild_id not in prefixes:
        return "$"
    else: return prefixes[guild_id]

async def actionEmbed(message, args=None, **kwargs):
    embed = discord.Embed(**kwargs)
    if 'authorName' in args: embed.set_author(name=args['authorName'])
    if 'authorIcon' in args: embed.set_author(name=args['authorName'], icon_url=args['authorIcon'])
    if 'imageURL' in args: embed.set_image(url=args['imageURL'])
    await message.send(embed=embed)

def group(*args):
    args = ', '.join(list(*args[:len(*args)]))
    args = f'{args}, and {str(*args[len(*args):])}'
    return args

bot = commands.Bot(command_prefix=setPrefix)

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

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello qtpi!')

@bot.command()
async def say(ctx,arg='What should I say?'):
    await ctx.send(arg)

@bot.command()
@commands.has_permissions(administrator=True)
async def settings(ctx, arg=None, arg2=None):
    guild = ctx.guild
    header = {'authorName':guild.name, 'authorIcon':guild.icon_url}
    pf = setPrefix(message=ctx, mode='') # setting mode to blank as the variable from memory is only needed
    if arg == None:
        await actionEmbed(ctx, header,
        description=f"`prefix` : `{pf}`"
        )
    elif arg == 'prefix':
        title = 'Settings > Prefix'
        description = f'Prefix for `{guild.id}`: `{pf}`'
        if arg2 == None: await actionEmbed(ctx, header, title=title, description=description)
        else:
            prefix = setPrefix(message=ctx, mode='rw', prefix=arg2)
            await actionEmbed(ctx, header, title=title, description=f'{description} > `{prefix}`')

load_dotenv()
TOKEN = os.getenv('DISCORD')
bot.run(TOKEN) # put the code in here