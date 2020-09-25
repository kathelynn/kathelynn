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

def group(*args):
    args = ', '.join(list(*args[:len(*args)]))
    args = f'{args}, and {str(*args[len(*args):])}'
    return args

def plurality(num, item):
    if num < 2:
        return f'{num} {item}'
    return f'{num} {item}s'

def merge_dict(source, destination): # note: in python 3.9, operator `|=` exists for dictionary.
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dict(value, node)
        else:
            destination[key] = value

    return destination