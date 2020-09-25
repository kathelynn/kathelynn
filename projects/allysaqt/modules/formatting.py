## Embed module, to be used for making embeds with one line of code ##
import discord

def json_embed(json): # translates stuff made from embed visualizer!

    if not 'content' in json: json['content'] = None

    set_embed = None
    if 'embed' in json:
        Empty = discord.Embed.Empty
        embeddicts = {}
        embedkwargs = {
            "title": Empty, "description": Empty, "url": Empty, "color": Empty, "timestamp": Empty
        }
        for key, value in json['embed'].items():
            if isinstance(value, dict):
                embeddicts[key] = value
            else: embedkwargs[key] = value
        
        set_embed = discord.Embed(
            title=embedkwargs['title'], description=embedkwargs['description'], url=embedkwargs['url'],
            color=embedkwargs['color'], timestamp=embedkwargs['timestamp']
            )
        for key, value in embeddicts.items():
            print(key, value)
            if key == 'footer':
                if 'text' in value:
                    set_embed.set_footer(text=embeddicts['footer']['text'])
                    if 'icon_url' in value:
                        set_embed.set_footer(text=embeddicts['footer']['text'], icon_url=embeddicts['footer']['icon_url'])
            elif key == 'thumbnail':
                set_embed.set_thumbnail(url=embeddicts['thumnbnail']['url'])
            elif key == 'image':
                set_embed.set_image(url=embeddicts['image']['url'])
            elif key == 'author':
                if 'name' in value:
                    if not 'url' in value:
                        embeddicts['author']['url'] = Empty
                    if not 'icon_url' in value:
                        embeddicts['author']['icon_url'] = Empty
                    set_embed.set_author(
                        name=embeddicts['author']['name'], url=embeddicts['author']['url'], icon_url=embeddicts['author']['icon_url']
                        )
            elif key == 'fields':
                if isinstance(value, list) and isinstance(value[0], dict):
                    for dictionary in value:
                        if 'inline' not in dictionary:
                            dictionary['inline'] = False
                        set_embed.add_field(name=dictionary['name'], value=dictionary['value'], inline=dictionary['inline'])

    return (json['content'], set_embed)

#async def action_embed(message, args={}, fields=[], sendMessage=True, **kwargs):
#    embed = discord.Embed(**kwargs)
#    
#    if isinstance(args, dict) and args != {}:
#        if 'authorName' in args:
#            embed.set_author(name=args['authorName'])
#            if 'authorIcon' in args:
#                embed.set_author(name=args['authorName'], icon_url=args['authorIcon'])
#        if 'thumbnailURL' in args:
#            embed.set_thumbnail(url=args['thumbnailURL'])
#        if 'imageURL' in args:
#            embed.set_image(url=args['imageURL'])
#    if isinstance(fields, list) and isinstance(fields[0], dict) and fields != {}:
#        for dictionary in fields:
#            if 'inline' not in dictionary:
#                dictionary['inline'] = False
#            embed.add_field(name=dictionary['name'], value=dictionary['value'], inline=dictionary['inline'])
#
#    if sendMessage:
#        return await message.send(embed=embed)
#    return embed

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


def make_dict(**kwargs):
    return kwargs