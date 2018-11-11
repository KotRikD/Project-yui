import traceback

import objdict
import common.Logger as Logger

class Stoaring:

    __slots__ = ("handlers", "plugins", "config", "wrappers", "temp_values", "before_handlers", "after_handlers", "cd_users", "on_init_handlers")

    def __init__(self):
        self.handlers = {}
        self.plugins = []
        self.on_init_handlers = []
        self.before_handlers = []
        self.after_handlers = []
        self.config = objdict.ObjDict()
        self.wrappers = objdict.ObjDict()
        self.temp_values = objdict.ObjDict()
        self.cd_users = {}

    def add_handler(self, cmd, func, check=True):
        if check:
            if cmd in store.handlers:
                aleardy = self.handlers[cmd]
                self.handlers[cmd] = []
                if type(aleardy) == list:
                    for x in aleardy:
                        self.handlers[cmd].append(x)
                else:
                    self.handlers[cmd].append(aleardy)

                self.handlers[cmd].append(func)
                return True

        self.handlers[cmd] = func
        return True

    def add_oninit_handler(self, handler):
        self.on_init_handlers.append(handler)
        return True

    def add_before_handler(self, handler):
        self.before_handlers.append(handler)
        return True

    def add_after_handler(self, handler):
        self.after_handlers.append(handler)
        return True

    async def call_async_safed(self, funcd, *args, **kwargs):
        result = None
        try:
            result = await funcd(*args, **kwargs)
            return result
        except Exception as e:
            Logger.Elog("Yui подняла тревогу, тут произошёл троллинг.")
            traceback.print_exc()
            return True

    async def call_on_init_handlers(self):
        for x in self.on_init_handlers:
            await self.call_async_safed(x, self)

        Logger.Nlog(f"Было загружено {len(self.plugins)} плагинов")

        return True

    async def call_command(self, update, currentStore):
        func = self.handlers.get(currentStore.cmd, None)
        if type(func) == list:
            for x in func:
                await self.call_async_safed(x, update, currentStore)
        else:
            await self.call_async_safed(func, update, currentStore)

        return True

    async def call_before_events(self, update, currentStore):
        result = False
        for x in self.before_handlers:
            a = await self.call_async_safed(x, update, currentStore)
            if a:
                result = True
                break

        return result

    async def call_after_events(self, update, currentStore):
        result = False
        for x in self.after_handlers:
            a = await self.call_async_safed(x, update, currentStore)
            if a:
                result = True
                break

        return result


store = Stoaring()

