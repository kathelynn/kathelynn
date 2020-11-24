import asyncio
from .moduleapi import framework
from .moduleapi import BOT

REACTIONS = {}
EMBED_TIMEOUT = 15
EMBED_TICKRATE = 8

@BOT.event
async def on_reaction_add(reaction, user):
    '''Runs when a reaction gets added'''
    if reaction.message.author == BOT.user:
        dictionary = {str(reaction.message.channel.id): {str(user.id): reaction.emoji}}
        framework.formatting.merge_dict(dictionary, REACTIONS)
        await asyncio.sleep(30)
        del REACTIONS[str(reaction.message.channel.id)][str(user.id)]

async def interactive_reaction(ctx, message, buttons):
    '''Makes reactions on messages interactive'''
    for i in range(0, len(buttons)):
        await message.add_reaction(buttons[i])
    await message.add_reaction('❎')

    channel_reactions = REACTIONS[str(ctx.channel.id)]
    secs = 1/EMBED_TICKRATE
    for i in range(0, EMBED_TIMEOUT*EMBED_TICKRATE):
        if str(ctx.author.id) in channel_reactions:
            if channel_reactions[str(ctx.author.id)] in buttons:
                reaction = buttons.index(channel_reactions[str(ctx.author.id)])
                del REACTIONS[str(ctx.channel.id)][str(ctx.author.id)]
                return reaction, None
            if REACTIONS[str(ctx.channel.id)][str(ctx.author.id)] == '❎':
                del REACTIONS[str(ctx.channel.id)][str(ctx.author.id)]
                return -1, 'cancelled'
            await asyncio.sleep(1/secs)
    return -1, 'timeout'