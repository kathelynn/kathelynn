## Embed module, to be used for making embeds with one line of code ##
import discord
async def action_embed(message, args=None, sendMessage=True, **kwargs):
    embed = discord.Embed(**kwargs)
    if 'authorName' in args:
        embed.set_author(name=args['authorName'])
    if 'authorIcon' in args:
        embed.set_author(name=args['authorName'], icon_url=args['authorIcon'])
    if 'imageURL' in args:
        embed.set_image(url=args['imageURL'])
    if sendMessage:
        return await message.send(embed=embed)
    return embed