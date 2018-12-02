import asyncio
from . import Logger
from objdict import ObjDict
from .Store import store

class YPlugin(object):

    def __init__(self, **kwargs):
        self.store = store
        self.ystore = ObjDict()
        self.__dict__.update(kwargs)

        self.store.plugins.append(self)

    def on_init(self):

        def wrapper(func):
            self.store.add_oninit_handler(func)

            return func

        return wrapper

    def before_command(self):

        def wrapper(func):
            self.store.add_before_handler(func)

            return func

        return wrapper

    def after_command(self):

        def wrapper(func):
            self.store.add_after_handler(func)

            return func

        return wrapper

    def on_command(self, command):

        def wrapper(func):
            if type(command) in [list,tuple]:
                for comm in command:
                    self.store.add_handler(comm, func)
            else:
                self.store.add_handler(command, func)

            return func

        return wrapper


    '''
    Здесь начинаются дополнительные декораторы написанные не мной
    '''

    def check_file_attach(self, att_type: str = "photo"):
        '''
        Decorator by https://vk.com/id499950380
        '''
        def wrap(f):
            async def wrapped_func(update, store):
                # Проверяем есть-ли вложения
                if update.attachs:
                    # Начинаем проверять вложения на тип att_type
                    if update.attachs[0].type == att_type:
                        return await f(update, store)
                    else:
                        return await store.reply(f"Вложение должно быть тип {att_type}, а не {update.attachs[0].type}")
                else:
                    return await store.reply(f"Пожалуйста добавьте к сообщению вложение типа {att_type}")

            return wrapped_func

        return wrap

