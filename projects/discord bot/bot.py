import discord
import time

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    channel = client.get_channel(754172127019794513)
    while True:
        text = input('> ')
        if not text[0] == '#':
            await channel.send(text)
        else:
            for guild in client.guilds:
                channel = discord.utils.get(guild.text_channels, name=text[1:])
                if channel == None:
                    print('Channel does not exist')
                else: print(f"Moved to #{channel.name} in '{channel.guild}'")

@client.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))


client.run('token')