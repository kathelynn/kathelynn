#from discord.ext import commands
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import json

def prefix(bot, message, mode='r', prefix='$'):
    guild_id = str(message.guild.id) # json only supports string for name
    if 'r' in mode:
        with open("prefixes.json") as f:
            prefixes = json.load(f)
        if guild_id not in prefixes:
            prefix(bot, message, 'w', prefix)
    if 'w' in mode:
        with open("prefixes.json", "w") as f:
            prefixes[guild_id] = prefix
            json.dump(prefixes, f)
    return prefixes[guild_id]

#def prefix(bot, message):
#    guild = message.guild
#    return prefixes.get(id, default_prefix)

bot = commands.Bot(command_prefix=prefix)

#async def commands(message, prefix):
#    if prefix in message.content[:len(prefix)]:
#        message.content = message.content[len(prefix):].lower()
#        if 'hello' in message.content[0:5]:
#            await message.channel.send('bracket works')
#        elif 'prefix ' in message.content[0:7]:
#            args = message.content[7:]
#            #symbol = "!@$&"
#            #if args not in symbol: message.channel.send('Symbols not in argument: !@#$%^&*\|;:,.<>/?') 
#            prefixupdate(message.guild, args)
#        elif 'say ' in message.content[0:4]:
#            await message.channel.send(message.content[4:])
#        elif 'help' in message.content[0:4]:
#            pf = prefix
#            embedmessage = discord.Embed(title=f"UwU you're a cute, {message.author}", description=f"{pf}help - list of commands"
#            "\n{pf}prefix - change bot prefix for this server\n{pf}hello - surprises\n{pf}say - say something")
#            await message.channel.send(content=None, embed=embedmessage)
#        else:
#            await message.channel.send(f"That's not a command, try {prefix}help")

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
        #try: prefix = prefixes[str(message.guild.id)] ## prefix check
        #except: prefixupdate(message.guild, "$")
        #if prefix in message.content[:len(prefix)]:
        #    print('triggered')
        #    await commands(message, prefix)
        await bot.process_commands(message)

@bot.command()
async def hello(message):
    await message.send(f'Hello qtpi!')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN) # put the code in here