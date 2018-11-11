import asyncio

import aiohttp
from objdict import ObjDict

from common.Store import store
import common.Logger as logger
import json

class VKLongPoll:

    def __init__(self, yuiworker):
        self.token = store.config.VKToken
        self.longpoll = None
        longpoll_settings = None

        if not longpoll_settings:
            longpoll_settings = {}

        self.group_id = None
        self.longpoll = None
        self.yuiworker = yuiworker

        self.version = "5.80"
        self.longpoll_settings = longpoll_settings

        self.api_url = "https://api.vk.com/method/{{}}?access_token={}&v={}" \
            .format(self.token, self.version)
        self.longpoll_url = "{}?act=a_check&key={}&wait=25&ts={}"


    async def request(self, method, **kwargs):
        url = self.api_url.format(method)
        data = {}
        for k, v in kwargs.items():
            if v is not None:
                data[k] = v

        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, data=data) as response:
                raw_respose_text = await response.text()

        raw_response = json.loads(raw_respose_text)
        if 'error' in raw_response:
            error = ObjDict()
            return error

        sucs = ObjDict()
        sucs.response = raw_response['response']
        return sucs

    async def update_longpoll_data(self):
        longpoll = await self.request("groups.getLongPollServer", group_id=self.group_id)
        if longpoll.get("error", None):
            logger.Elog("Long poll not founded!!!!#$%#T#Crashed...waiting....")
            raise ValueError()

        self.longpoll = {
            **longpoll.response
        }

    async def receiver(self):
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.post(
                        self.longpoll_url.format(
                            self.longpoll["server"],
                            self.longpoll["key"],
                            self.longpoll["ts"],
                        )
                ) as resp:
                    response = await resp.json()

        except Exception as e:
            return ()

        if "ts" in response:
            self.longpoll["ts"] = response["ts"]

        if "failed" in response:
            if response["failed"] in (2, 3, 4):
                await self.update_longpoll_data()

            return ()

        updates = []

        for update in response["updates"]:
            if "type" not in update or "object" not in update:
                continue

            updates.append(update)

        return updates

    async def start(self):
        if not self.longpoll:
            await self.update_longpoll_data()

        store.wrappers.request = self.request

        while True:
            for update in await self.receiver():
                await self.yuiworker.process_update(update)
            await asyncio.sleep(0.01)
