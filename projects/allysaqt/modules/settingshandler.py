'''Settings handler'''
from . import memoryhandler

def prefix(bot=None, ctx=None, guild_id=None, mode='', prefix=None): # mode should be same as on storagehandler.store
    '''Prefix ??'''
    if not guild_id:
        guild_id = ctx.guild.id
    if isinstance(guild_id, int):
        guild_id = str(guild_id)
    return memoryhandler.access(guild_id=guild_id, mode=mode,
                                category="settings", item="prefix", value=prefix)
