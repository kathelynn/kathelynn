#from dotenv import load_dotenv
import asyncio
import discord
from discord.ext import commands
import os
from string import Template # gives module not found error if put on module list
from modules import *

##############
###COMMANDS###
##############

commands = discord.ext.commands
bot = commands.Bot(command_prefix=settingshandler.prefix)
Empty = discord.Embed.Empty

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
        content = ctx.message.content[len(pf):].split()
        content[0] = content[0].lower()
        try:
            aliases = memoryhandler.access(guild_id=ctx.guild.id, category='aliases', mode='*')
            for key, value in aliases.items():
                if content[0] in key:
                    content[0] = value
            ccmd = ccmdhandler.load(content[0], ctx=ctx)

            format_author = f'<@{ctx.author.id}>'
            format_author_avatarurl = ctx.author.avatar_url
            format_mentions = ctx.message.raw_mentions
            format_content = ' '.join(content[1:])
            format_clean_content = ctx.message.clean_content

            stringformatting = {
                "author": format_author, "author_avatarurl": format_author_avatarurl, "mentions": format_mentions,
                "content": format_content, "clean_content": format_clean_content
            }

            await ctx.send(**formatting.json_embed(ccmd, stringformatting))

   
        except KeyError:
            raise commands.CommandNotFound('Command does not exist!')
    
    if isinstance(error, discord.errors.Forbidden):
        ctx.author.send("Sorry! I currently don't have the permissions required to do that.")


#@bot.command()
#async def say(ctx, *args):
#    message = 'What should I say, qtpi?'
#    if args == (): await ctx.send(message)
#    else: await ctx.send(' '.join(args))

reactions = {}

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == bot.user: 
        react = reaction.emoji
        channel_id = str(reaction.message.channel.id)
        user_id = str(user.id)
        dictionary = {str(channel_id): {str(user_id): react}}
        merge(dictionary, reactions)
    
@bot.command(aliases=['ccommands', 'cc'])
async def customcommands(ctx, arg=None, path=None, botmsg=None):
    choices = None
    buttons = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    guild = ctx.guild
    pf = settingshandler.prefix(guild_id=guild.id)

    author = {'name': guild.name, 'icon_url': str(guild.icon_url)}
    fields = [{'name': f'`{pf}create', 'value':'Initialize embed creation tool'}]
    title = 'Custom Commands'
    footer = Empty
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
        fields=Empty

    embed = formatting.make_dict(embed={"title": title, "description":description, "color": color, "footer": footer, "author": author, "fields":fields})

    if botmsg:
        await botmsg.edit(**formatting.json_embed(embed))
        await botmsg.clear_reactions()
    else:
        await ctx.send(**formatting.json_embed(embed))

    if choices:
        for x in range(0, len(choices)):
            await botmsg.add_reaction(buttons[x])
        await botmsg.add_reaction('❎')

        for x in range(0,120):
            if str(ctx.author.id) in reactions[str(ctx.channel.id)]:
                for button in buttons:
                    if reactions[str(ctx.channel.id)][str(ctx.author.id)] == button:
                        button_picked = buttons.index(button)
                        button_picked = choices[button_picked]
                        del reactions[str(ctx.channel.id)][str(ctx.author.id)]
                        await customcommands(ctx, arg=arg, path=button_picked, botmsg=botmsg)
                        return
                    if reactions[str(ctx.channel.id)][str(ctx.author.id)] == '❎':
                        await customcommands(ctx, arg='cancel', botmsg=botmsg)
                        del reactions[str(ctx.channel.id)][str(ctx.author.id)]
                        return
            await asyncio.sleep(.125)
        await customcommands(ctx, arg, 'timeout')

@bot.command(aliases=['setting', 'set'])
async def settings(ctx, arg=None, arg2=None):
    permission_error = lambda arg, perm: f"Sorry, you need `{perm}` permission to access `{arg}` setting."
    author_permissions = ctx.author.guild_permissions
    guild = ctx.guild
    pf = settingshandler.prefix(guild_id=guild.id)

    author = {'name': guild.name, 'icon_url': str(guild.icon_url)}
    title = 'Settings'
    description = f"`prefix`: `{pf}`"
    color = 2896440

    if arg == 'prefix':
        title = 'Settings > Prefix'
        description = f"Prefix for `{guild.id}`: `{pf}`"
        if arg2:
            if not author_permissions.manage_guild:
                description = permission_error('prefix', 'Manage Server') # 'Guild' is 'Server' in Discord UX context
                color = 16711680
            elif len(arg2) > 3:
                description += f"\nSorry! `{arg2}` is {formatting.plurality(len(arg2) - 3, 'character')} too long."
                color = 16711680
            else:
                prefix = settingshandler.prefix(guild_id=guild.id, mode='rw', prefix=arg2)
                description += f"> `{prefix}`\nBot prefix has been changed!"
                color = 65280

    embed = formatting.make_dict(embed={"title": title, "description": description, "color": color, "author": author})
    await ctx.send(**formatting.json_embed(embed))

## To run the bot, you need to change the arguments inside bot.run with a string of your bot token, or try to ##
## create a 'discord_token.json' file with the name and token inside the dictionary.                          ##
token = memoryhandler.grabtoken()
bot.run(token["allysaqt"])