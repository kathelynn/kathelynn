import discord
import math
import datetime
from .moduleapi import BOT
from .moduleapi import framework

@BOT.command()
async def ping(ctx):
    embed = discord.Embed.from_dict({"title": '🏓 Pong!', "color": 2896440, "fields": [{"name": "Latency",
                                     "value": f"{math.floor((int(datetime.datetime.utcnow().strftime('%f')) - int(ctx.message.created_at.strftime('%f')))/1000)}ms"}]})
    await ctx.send(embed=embed)

@BOT.command(aliases=['setting', 'set'])
async def settings(ctx, arg=None, arg2=None):
    '''Settings command'''
    permission_error = lambda arg, perm: f"Sorry, you need `{perm}` permission to access `{arg}` setting."
    author_permissions = ctx.author.guild_permissions
    guild = ctx.guild
    prefix = framework.loadstufftomemory.prefix(guild_id=guild.id)

    author = {'name': guild.name, 'icon_url': str(guild.icon_url)}
    title = '⚙️ Settings'
    description = f"`prefix`: `{prefix}`"
    color = 2896440

    if arg == 'prefix':
        title = f'{title} > Prefix'
        description = f"Prefix for `{guild.id}`: `{prefix}`"
        if arg2:
            if not author_permissions.manage_guild:
                # 'Guild' is 'Server' in Discord UX context
                description = permission_error('prefix', 'Manage Server')
                color = 16711680
            elif len(arg2) > 3:
                description += f"\nSorry! `{arg2}` is {framework.formatting.plurality(len(arg2) - 3, 'character')} too long."
                color = 16711680
            else:
                prefix = framework.loadstufftomemory.prefix(guild_id=guild.id, mode='w', prefix=arg2)
                description += f"> `{prefix}`\nBot prefix has been changed!"
                color = 65280

    embed = framework.formatting.make_dict(embed={"title": title, "description": description,
                                                "color": color, "author": author})
    await ctx.send(**framework.formatting.json_embed(embed))

from . import embedinterface

@BOT.command(aliases=['ccommands', 'cc'])
async def customcommands(ctx, arg=None, path='00', botmsg=None):
    '''Custom commands command'''
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
        fields = [{'name': f'{prefix}customommands create`', 'value':'Initialize embed creation tool'}]
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
            if path[1] == 'b':
                description = "Barfoo picked!"

    embed_JSON = {}    
    for embed in ['title', 'description', 'color', 'footer', 'author', 'fields']:
        value = locals()[embed]
        if value:
            embed_JSON[embed] = value
        
    embed = discord.Embed.from_dict({"title": title, "description":description, "color": color,
                                     "footer": footer, "author": author, "fields":fields})

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
        path_result = await embedinterface.interactive_reaction(ctx, botmsg, buttons[:len(choices)])
        if isinstance(path_result, int):
            path_result, embed_error = choices[path_result]
            if embed_error:
                path_result = embed_error
        await customcommands(ctx, arg=arg, path=path_result, botmsg=botmsg)