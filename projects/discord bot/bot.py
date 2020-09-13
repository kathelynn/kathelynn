#from discord.ext import commands
import discord
import json
#default_prefix = "$"

#def prefix(bot, message):
#    id = message.guild.id
#    return prefixes.get(id, default_prefix)

def prefixupdate(guild, prefix):
    global prefixes
    with open("prefixes.json", "w+") as f:
        prefixes[str(guild.id)] = prefix
        f.seek(0)
        json.dump(prefixes, f)

with open("prefixes.json") as f: prefixes = json.load(f)

async def commands(message, prefix):
    if prefix in message.content[:len(prefix)]:
        message.content = message.content[len(prefix):].lower()
        if 'hello' in message.content[0:5]:
            await message.channel.send('bracket works')
        elif 'prefix' in message.content[0:6]:
            args = message.content[7:]
            #symbol = "!@$&"
            #if args not in symbol: message.channel.send('Symbols not in argument: !@#$%^&*\|;:,.<>/?') 
            prefixupdate(message.guild, args)
        elif 'help' in message.content[0:5]:
            pf = prefix
            embedmessage = discord.Embed(title="UwU you're a cute", description=f"{pf}help - list of commands\n{pf}prefix - change bot prefix for this server\n{pf}hello - surprises")
            await message.channel.send(content=None, embed=embedmessage)
        else:
            message.channel.send("That's not a command, try >help")
        

client = discord.Client()
#bot = commands.Bot(command_prefix=prefixes)

@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    #channel = client.get_channel(754172127019794513)
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

@client.event
async def on_message(message):
        print('Message from {0.author}: {0.content}'.format(message))
        try: prefix = prefixes[str(message.guild.id)] ## prefix check
        except: prefixupdate(message.guild, "$")
        if prefix in message.content[:len(prefix)]:
            print('triggered')
            await commands(message, prefix)

#@bot.command
#async def herro(message):
#    await message.channel.send(f'Hello qtpi!')

client.run('NzU0MTg5NjE2NTI5MTQ1OTA3.X1xH0A.BLv8xSEnMlX5gbuGHB6Y_KuVvFI') # put the code in here
