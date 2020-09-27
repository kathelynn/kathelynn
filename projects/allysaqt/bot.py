'''Aly is a qt'''
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
    print(f'Logged on as {BOT.user}!')
    channel = BOT.get_channel(598967091978174477)
    await channel.send('I am awake~')

@BOT.event
async def on_message(message):
    '''Runs when we get a message to log it'''
    print('{0.author} from {0.channel}: {0.content}'.format(message))
    await BOT.process_commands(message)

@BOT.event
async def on_reaction_add(reaction, user):
    '''Runs when a reaction gets added'''
    if reaction.message.author == BOT.user:
        react = reaction.emoji
        channel_id = str(reaction.message.channel.id)
        user_id = str(user.id)
        dictionary = {str(channel_id): {str(user_id): react}}
        modules.formatting.merge_dict(dictionary, REACTIONS)

@BOT.command(aliases=['ccommands', 'cc'])
async def customcommands(ctx, arg=None, path=None, botmsg=None):
    '''Custom commands command'''
    choices = None
    buttons = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    guild = ctx.guild
    prefix = modules.settingshandler.prefix(guild_id=guild.id)

    author = {'name': guild.name, 'icon_url': str(guild.icon_url)}
    fields = [{'name': f'`{prefix}create', 'value':'Initialize embed creation tool'}]
    title = 'Custom Commands'
    footer = discord.Embed.Empty
    color = 800868

    if arg == 'cancel':
        description = "Operation cancelled."
        color = 16711680
    elif arg == 'timeout':
        description = "Timeout exceeded. Please try again"
        color = 16711680

    elif arg == 'create':
        title = 'Custom Commands > Create'
        description = "Work in Progress\n`1.` Foo\n`2.` Bar"
        choices = ['a', 'b0']

        if path:
            if path[0] == 'a':
                description = 'End'

            elif path[0] == 'b':
                description = "Work in progress\n`1.` Foobar\n`2.` Barfoo"
                choices = ['ba', 'bb']
                if path[1] == 'a':
                    description = "Foobar picked!"
                if path[1] == 'b':
                    description = "Barfoo picked!"

    if description:
        fields=discord.Embed.Empty

    embed = modules.formatting.make_dict(embed={"title": title, "description":description,
                                                "color": color, "footer": footer,
                                                "author": author, "fields":fields})

    if botmsg:
        await botmsg.edit(**modules.formatting.json_embed(embed))
        await botmsg.clear_reactions()
    else:
        await ctx.send(**modules.formatting.json_embed(embed))

    if choices:
        for i in range(0, len(choices)):
            await botmsg.add_reaction(buttons[i])
        await botmsg.add_reaction('❎')

        for i in range(0,120):
            if str(ctx.author.id) in REACTIONS[str(ctx.channel.id)]:
                for button in buttons:
                    if REACTIONS[str(ctx.channel.id)][str(ctx.author.id)] == button:
                        button_picked = buttons.index(button)
                        button_picked = choices[button_picked]
                        del REACTIONS[str(ctx.channel.id)][str(ctx.author.id)]
                        await customcommands(ctx, arg=arg, path=button_picked, botmsg=botmsg)
                        return
                    if REACTIONS[str(ctx.channel.id)][str(ctx.author.id)] == '❎':
                        await customcommands(ctx, arg='cancel', botmsg=botmsg)
                        del REACTIONS[str(ctx.channel.id)][str(ctx.author.id)]
                        return
            await asyncio.sleep(.125)
        await customcommands(ctx, arg, 'timeout')

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
