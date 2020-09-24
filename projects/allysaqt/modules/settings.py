from modules import storagehandler
def prefix(bot=None, ctx=None, guild_id=None, mode='r', prefix=None): # mode should be same as on storagehandler.store
    if not guild_id: guild_id = ctx.guild.id
    if isinstance(guild_id, int):
        guild_id = str(guild_id)
    return storagehandler.store(guild_id, mode, category="settings", item="prefix", var=prefix)