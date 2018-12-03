from common.Plugin import YPlugin
from common.Store import store as gstore

plugin = YPlugin()

@plugin.on_command("test_debug")
async def test_debug(update, store):
    result = f"Yui-бот\nВерсия: {gstore.config.ver}\n"
    commands = []
    for (k,v) in gstore.handlers.items():
        commands.append(k)
    result += f"Команды: {str(commands)}\n"
    result += f"Количество команд: {len(gstore.handlers)}/{len(gstore.before_handlers)}/{len(gstore.after_handlers)}\n"
    result += f"Использование дб: {str(gstore.config.DBSettings['DBDriver'])}: {str(gstore.config.UseDB)}/redis: {str(gstore.config.UseRedis)}\n"
    result += f"КД: {gstore.config.CoolDownDelay}сек\n"
    result += f"ChatMeta: {gstore.config.UseChatMeta}\n"
    result += f"Префиксы: {str(gstore.config.Prefixes)}"

    return await store.reply(result)