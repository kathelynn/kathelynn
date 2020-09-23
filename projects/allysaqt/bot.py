#pylint: disable=undefined-variable

#from dotenv import load_dotenv
import importlib
module_list = ['discord', 'discord.ext.commands', 'os', 'asyncio', 'json']
for lib in module_list:
    globals()[lib] = importlib.import_module(lib)
from modules import *

## Embed module, to be used for making embeds with one line of code ##
async def action_embed(message, args=None, sendMessage=True, **kwargs):
    embed = discord.Embed(**kwargs)
    if 'authorName' in args:
        embed.set_author(name=args['authorName'])
    if 'authorIcon' in args:
        embed.set_author(name=args['authorName'], icon_url=args['authorIcon'])
    if 'imageURL' in args:
        embed.set_image(url=args['imageURL'])
    if sendMessage:
        return await message.send(embed=embed)
    return embed

def merge(source, destination): # note: in python 3.9, operator `|=` exists for dictionary.
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination

## For action embeds when multiple people are in ##
def group(*args):
    args = ', '.join(list(*args[:len(*args)]))
    args = f'{args}, and {str(*args[len(*args):])}'
    return args

def plurality(num, item):
    if num < 2:
        return f'{num} {item}'
    return f'{num} {item}s'

##############
###COMMANDS###
##############

commands = discord.ext.commands
bot = commands.Bot(command_prefix=settings.prefix)

@bot.event
async def on_ready():
    global reactions
    reactions = {}

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pf = await bot.get_prefix(ctx)
        message_content = ctx.message.content[len(pf):]
        try:
            ccommand = ccommands.load(message_content, ctx=ctx)
            if 'content' not in ccommand:
                ccommand['content'] = None
            if 'embed' not in ccommand:
                ccommand['embed'] = None
            await ctx.send(content=ccommand['content'], embed=ccommand['embed'])
        except KeyError:
            raise commands.CommandNotFound('Command does not exist!')
        


@bot.command(aliases=['hi'])
async def hello(ctx): 
    message = f'Hello, <@{ctx.author.id}> qtpi!'
    await ctx.send(message)

@bot.command()
async def say(ctx, *args):
    message = 'What should I say, qtpi?'
    if args == (): await ctx.send(message)
    else: await ctx.send(' '.join(args))

reactions = {}

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == bot.user: 
        react = reaction.emoji
        channel_id = str(reaction.message.channel.id)
        user_id = str(user.id)
        print(react)
        dictionary = {str(channel_id): {str(user_id): react}}
        merge(dictionary, reactions)
        print(reactions)
        #print(reactions[message.guild.id][message.channel.id].pop(message.id))
    
@bot.command(aliases=['ccommands', 'cc'])
async def customcommands(ctx, botmsg=None, path=None, end=False):
    guild = ctx.guild
    header = {'authorName': guild.name, 'authorIcon': guild.icon_url}
    title = 'Custom Commands'
    footer = None
    color = 800868
    buttons = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    if path == 'cancel':
        description = "Operation cancelled."
        color = 16711680
        end = True
    if path == 'timeout':
        description = "Timeout exceeded. Please try again"
        color = 16711680
        end = True

    if not path:
        choices = ['a0', 'b0']
        description = "Work in Progress\n`1.` Foo\n`2.` Bar"
        botmsg = await action_embed(ctx, header, title=title, description=description, color=color, footer=footer)

    if path:
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

        await botmsg.edit(embed=await action_embed(ctx, header, sendMessage=False, title=title, description=description, color=color, footer=footer))

    await botmsg.clear_reactions()

    if not end:
        for x in range(0, len(choices)):
            await botmsg.add_reaction(buttons[x])
        await botmsg.add_reaction('❎')

        for x in range(0,120):
            if str(ctx.author.id) in reactions[str(ctx.channel.id)]:
                for item in buttons:
                    if reactions[str(ctx.channel.id)][str(ctx.author.id)] == item:
                        item_picked = buttons.index(item)
                        item_picked = choices[item_picked]
                        del reactions[str(ctx.channel.id)][str(ctx.author.id)]
                        await customcommands(ctx, botmsg=botmsg, path=item_picked)
                        return
                    if reactions[str(ctx.channel.id)][str(ctx.author.id)] == '❎':
                        await customcommands(ctx, botmsg=botmsg, path='cancel')
                        del reactions[str(ctx.channel.id)][str(ctx.author.id)]
                        return
            await asyncio.sleep(.125)
        await customcommands(ctx, 'timeout')

@bot.command(aliases=['set'])
async def settings(ctx, arg=None, arg2=None):
    permission_error = lambda arg, perm: f"Sorry, you need `{perm}` permission to access `{arg}` setting."
    author_permissions = ctx.author.guild_permissions
    guild = ctx.guild
    prefix = settings.prefix(guild_id=guild.id)

    header = {'authorName': guild.name, 'authorIcon': guild.icon_url}
    title = 'Settings'
    description = f"`prefix`: `{prefix}`"
    color = 2896440

    if arg == 'prefix':
        title = 'Settings > Prefix'
        description = f"Prefix for `{guild.id}`: `{prefix}`"
        if arg2:
            if not author_permissions.manage_guild:
                description = permission_error('prefix', 'Manage Server') # 'Guild' is 'Server' in Discord UX context
                color = 16711680
            elif len(arg2) > 3:
                description += f"\nSorry! `{arg2}` is {plurality(len(arg2) - 3, 'character')} too long."
                color = 16711680
            else:
                prefix = settings.prefix(guild_id=guild.id, mode='rw', prefix=arg2)
                description += f"> `{prefix}`\nBot prefix has been changed!"
                color = 65280

    await action_embed(ctx, header, title=title, description=description, color=color)

## To run the bot, you need to change the arguments inside bot.run with a string of your bot token, or try to ##
## create a 'discord_token.json' file with the name and token inside the dictionary.                          ##
token = grabtoken()
bot.run(token["allysaqt"])