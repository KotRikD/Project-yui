import asyncio
import os
import shlex
import sys
import time
import traceback

from objdict import ObjDict

import common.Logger as Logger
import common.VK.Convert as Converter
from common.Store import store
from common.VK.VKWrappers import make_upload_docs, make_upload_photo, make_reply
from utils import load_config

import common.VK.Chatmeta as ChatMeta


class Yui:

    def __init__(self):
        self.store = store
        self.ver = "0.1.8 beta"

        Logger.Ylog(f"> Привет, я Yui! Бот для социальной сети ВК.\n> На данный момент моя версия: {self.ver}")
        load_config()
        self.call_init()

    def call_init(self):
        plugin_folder_files = os.listdir("plugins")
        if not plugin_folder_files:
            Logger.Elog("Не было найдено плагинов! Создайте хоть один плагин")
            exit()

        sys.path.insert(0, "plugins")
        for file in plugin_folder_files:
            if file.startswith("__"):
                continue
            try:
                plugin_subfolder = os.listdir(f"plugins/{file}")
                sys.path.insert(0, f"plugins/{file}")
                for subfiles in plugin_subfolder:
                    if subfiles.endswith(".py"):
                        try:
                            a = __import__(os.path.splitext(subfiles)[0], None, None, [''])
                            Logger.Slog(f"Юи загрузила плагин {subfiles}")
                        except Exception as err:
                            traceback.print_exc()
            except Exception:
                pass

            if file.endswith(".py"):
                try:
                    a = __import__(os.path.splitext(file)[0], None, None, [''])
                    Logger.Slog(f"Юи загрузила плагин {file}")
                except Exception as err:
                    traceback.print_exc()
        return True

    def say_goodbye(self):
        Logger.Ylog("Пока семпай, надеюсь ещё встретимся!")

    async def process_update(self, update):
        updated_message = await Converter.convert_to_message(update)

        await asyncio.sleep(0.1)

        prefix = None
        for lprefix in self.store.config.Prefixes:
            if updated_message.text.startswith(lprefix):
                updated_message.text = updated_message.text[len(lprefix):]
                prefix = lprefix
                break
        if not prefix:
            return True

        command = None
        for (k, v) in store.handlers.items():
            if updated_message.text.startswith(k):
                command = k
                break

        args = None
        if command:
            args = shlex.split(updated_message.text[len(command):].strip())

            if self.store.config.NeedLogMessage:
                Logger.Slog(
                    f"Пришла команда {command} с аргументами {args} из { f'ЛС {updated_message.peer_id}' if not updated_message.is_multichat else f'Беседы #{updated_message.chat_id}' }")

        ts = int(time.time())

        if updated_message.from_id in self.store.cd_users:
            if ts - self.store.cd_users[updated_message.from_id]['message_date'] <= self.store.config.CoolDownDelay:
                self.store.cd_users[updated_message.from_id]['message_date'] = ts
                return True

            self.store.cd_users[updated_message.from_id]['message_date'] = ts
        else:
            self.store.cd_users[updated_message.from_id] = {}
            self.store.cd_users[updated_message.from_id]['message_date'] = ts

        currentStore = ObjDict()
        currentStore.reply = make_reply(self.store, updated_message.peer_id, currentStore)
        currentStore.upload_photo = make_upload_photo(self.store, updated_message.peer_id)
        currentStore.upload_doc = make_upload_docs(self.store, updated_message.peer_id)
        currentStore.request = self.store.wrappers.request
        if command:
            currentStore.cmd = command
            currentStore.args = args
            currentStore.prefix = prefix

        if self.store.config.UseChatMeta:
            await ChatMeta.call_chat_meta(currentStore, updated_message)

        if await self.store.call_before_events(updated_message, currentStore):
            return True

        if command:
            await self.store.call_command(updated_message, currentStore)

        if await self.store.call_after_events(updated_message, currentStore):
            return True
