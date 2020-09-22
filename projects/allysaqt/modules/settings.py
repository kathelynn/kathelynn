from modules import storagehandler
def set_prefix(bot=None, message=None, guild_id=None, mode='r', prefix='a$'):
    if not guild_id: guild_id = message.guild.id
    if isinstance(guild_id, int):
        guild_id = str(guild_id)
    return storagehandler.store(guild_id, mode, category="settings", item="prefix", var=prefix)