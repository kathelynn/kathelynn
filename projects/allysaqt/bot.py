'''Ally is a qt'''
import asyncio
import discord
from discord.ext import commands
import modules

# COMMANDS

BOT = commands.Bot(command_prefix=modules.settingshandler.prefix)
REACTIONS = {}

@BOT.event
async def on_ready():
    '''Runs when the bot connects to discord'''
#    print(f'Logged on as {BOT.user}!')
#    channel = BOT.get_channel(598967091978174477)
#    await channel.send('I am awake~')

@BOT.event
async def on_message(message):
    '''Runs when we get a message to log it'''
    print('{0.author} from {0.channel}: {0.content}'.format(message))
    await BOT.process_commands(message)

async def ccommand(message):
    print(message.content[len(message.prefix):])

@BOT.event
async def on_reaction_add(reaction, user):
    '''Runs when a reaction gets added'''
    if reaction.message.author == BOT.user:
        dictionary = {str(reaction.message.channel.id): {str(user.id): reaction.emoji}}
        modules.formatting.merge_dict(dictionary, REACTIONS)
        await asyncio.sleep(30)
        del REACTIONS[str(reaction.message.channel.id)][str(user.id)]

async def interactive_reaction(ctx, message, buttons):
    '''Makes reactions on messages interactive'''
    for i in range(0, len(buttons)):
        await message.add_reaction(buttons[i])
    await message.add_reaction('❎')

    channel_reactions = REACTIONS[str(ctx.channel.id)]
    for i in range(0,240):
        if str(ctx.author.id) in channel_reactions:
            if channel_reactions[str(ctx.author.id)] in buttons:
                reaction = buttons.index(channel_reactions[str(ctx.author.id)])
                del REACTIONS[str(ctx.channel.id)][str(ctx.author.id)]
                return reaction
            if REACTIONS[str(ctx.channel.id)][str(ctx.author.id)] == '❎':
                del REACTIONS[str(ctx.channel.id)][str(ctx.author.id)]
                return 'cancel'
        await asyncio.sleep(.125)
    return 'timeout'

@BOT.command(aliases=['ccommands', 'cc'])
async def customcommands(ctx, arg=None, path='00', botmsg=None):
    '''Custom commands command'''
    choices = None
    buttons = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    guild = ctx.guild
    prefix = modules.settingshandler.prefix(guild_id=guild.id)

    author = {'name': guild.name, 'icon_url': str(guild.icon_url)}
    title = 'Custom Commands'
    description = None
    fields = None
    footer = None
    color = 800868

    if not arg:
        fields = [{'name': f'{prefix}customommands create`', 'value':'Initialize embed creation tool'}]
    if arg == 'create':
        title = 'Custom Commands > Create'
        description = "Work in Progress\n`1.` Foo\n`2.` Bar"
        choices = ['a', 'b0']

        if path == 'cancel':
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
            if path[1] == 'b':
                description = "Barfoo picked!"

    embed_JSON = {}    
    for embed in ['title', 'description', 'color', 'footer', 'author', 'fields']:
        value = locals()[embed]
        if value:
            embed_JSON[embed] = value
        
    embed = discord.Embed.from_dict({"title": title, "description":description,
                                                "color": color, "footer": footer,
                                                "author": author, "fields":fields})

    if botmsg:
        #await botmsg.edit(**modules.formatting.json_embed(embed))
        await botmsg.clear_reactions()
        await botmsg.edit(embed=embed)
    else:
        botmsg = await ctx.send(embed=embed)
        #await ctx.send(**modules.formatting.json_embed(embed))

    try: 
        if path in choices:
            return
    except TypeError: return
    if choices or not end:
        path_result = await interactive_reaction(ctx, botmsg, buttons[:len(choices)])
        if isinstance(path_result, int):
            path_result = choices[path_result]
        await customcommands(ctx, arg=arg, path=path_result, botmsg=botmsg)

@BOT.command(aliases=['setting', 'set'])
async def settings(ctx, arg=None, arg2=None):
    '''Settings command'''
    permission_error = lambda arg, perm: f"Sorry, you need `{perm}` permission to access `{arg}` setting."
    author_permissions = ctx.author.guild_permissions
    guild = ctx.guild
    prefix = modules.settingshandler.prefix(guild_id=guild.id)

    author = {'name': guild.name, 'icon_url': str(guild.icon_url)}
    title = 'Settings'
    description = f"`prefix`: `{prefix}`"
    color = 2896440

    if arg == 'prefix':
        title = 'Settings > Prefix'
        description = f"Prefix for `{guild.id}`: `{prefix}`"
        if arg2:
            if not author_permissions.manage_guild:
                # 'Guild' is 'Server' in Discord UX context
                description = permission_error('prefix', 'Manage Server')
                color = 16711680
            elif len(arg2) > 3:
                description += f"\nSorry! `{arg2}` is {modules.formatting.plurality(len(arg2) - 3, 'character')} too long."
                color = 16711680
            else:
                prefix = modules.settingshandler.prefix(guild_id=guild.id, mode='rw', prefix=arg2)
                description += f"> `{prefix}`\nBot prefix has been changed!"
                color = 65280

    embed = modules.formatting.make_dict(embed={"title": title, "description": description,
                                                "color": color, "author": author})
    await ctx.send(**modules.formatting.json_embed(embed))

# To run the bot, you need to change the arguments inside bot.run
# with a string of your bot token, or try to ##
# create a 'discord_token.json' file with the name and token inside the dictionary.
TOKEN = modules.memoryhandler.grabtoken()
BOT.run(TOKEN["allysaqt"])
