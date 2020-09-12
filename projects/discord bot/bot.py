from discord.ext import commands
import discord
import json
with open("prefixes.json") as f:
    f.seek(0)
    prefixes = json.load(f)
    print(prefixes)
default_prefix = "$"

def prefix(bot, message):
    id = message.guild.id
    print('prefix grabbed')
    return prefixes.get(id, default_prefix)

client = discord.Client()
bot = commands.Bot(command_prefix="$")

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
        if '!' in message.content[:1]:
            if 'hello' in message.content[1:]:
                await message.channel.send(f'Hello qtpi! why are you using brackets')
    
@bot.command
async def pleasework(message):
    await message.channel.send(f'Hello qtpi!')

client.run('') # put the code in here
bot.run()