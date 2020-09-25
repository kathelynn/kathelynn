#pylint: disable=undefined-variable
#from dotenv import load_dotenv
import importlib
module_list = ['asyncio', 'discord', 'discord.ext.commands', 'os']
for lib in module_list:
    globals()[lib] = importlib.import_module(lib)
from string import Template # gives module not found error if put on module list
from modules import *

##############
###COMMANDS###
##############

commands = discord.ext.commands
bot = commands.Bot(command_prefix=setting.prefix)

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
        #try:
        aliases = memoryhandler.access(guild_id=ctx.guild.id, category='aliases', mode='*')
        for key, value in aliases.items():
            if content[0] in key:
                content[0] = value
        ccmd = cc.load(content[0], ctx=ctx)

        format_author = f'<@{ctx.author.id}>'
        format_author_avatarurl = ctx.author.avatar_url
        format_mentions = ctx.message.raw_mentions
        format_content = ' '.join(content[1:])
        format_clean_content = ctx.message.clean_content

        stringformatting = {
            "author": format_author, "author_avatarurl": format_author_avatarurl, "mentions": format_mentions
        }

        def str_format(str_input):
            str_input = Template(str_input)
            return str_input.substitute (
                author=format_author, author_avatarurl=format_author_avatarurl, mentions=format_mentions,
                content=format_content, clean_content=format_clean_content
            )

        def dict_format(dictionary):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    dictionary[key] = dict_format(value)
                else:
                    dictionary[key] = str_format(value)
                    return dictionary

        #embed = formatting.make_dict(title=title, description=description, color=color, author=author)
        #embed = formatting.make_dict(embed=embed)
        content, embed = formatting.json_embed(ccmd, )
        if content: content = str_format(content)

        await ctx.send(content=content, embed=embed)

        #except KeyError:
        #    raise commands.CommandNotFound('Command does not exist!')

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
    author = {'name': guild.name, 'icon_url': str(guild.icon_url)}
    description = "Test."
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

    embed = formatting.make_dict(title=title, description=description, color=color, footer=footer, author=author)
    embed = formatting.make_dict(embed=embed)
    content, embed = formatting.json_embed(embed)

    if botmsg:
        await botmsg.edit(content=content, embed=embed)
        await botmsg.clear_reactions()
    else:
        await ctx.send(content=content, embed=embed)

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
    pf = setting.prefix(guild_id=guild.id)

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
                prefix = setting.prefix(guild_id=guild.id, mode='rw', prefix=arg2)
                description += f"> `{prefix}`\nBot prefix has been changed!"
                color = 65280

    embed = formatting.make_dict(title=title, description=description, color=color, author=author)
    embed = formatting.make_dict(embed=embed)
    content, embed = formatting.json_embed(embed)
    await ctx.send(content=content, embed=embed)

## To run the bot, you need to change the arguments inside bot.run with a string of your bot token, or try to ##
## create a 'discord_token.json' file with the name and token inside the dictionary.                          ##
token = memoryhandler.grabtoken()
bot.run(token["allysaqt"])