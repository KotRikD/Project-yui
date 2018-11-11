from .Convert import convert_to_attachment
import aiohttp
import json
from objdict import ObjDict

'''
Code copied from ekonda/kutana
'''


async def send_message(store, message, peer_id, attachment=None,
                       sticker_id=None, payload=None, keyboard=None,
                       forward_messages=None):
    """Send message to target peer_id with parameters."""

    if isinstance(attachment, ObjDict):
        attachment = [attachment]

    if isinstance(attachment, (list, tuple)):
        new_attachment = ""

        for a in attachment:
            if isinstance(a, ObjDict):
                new_attachment += \
                    "{}{}_{}".format(a.type, a.owner_id, a.id) + \
                    ("_" + a.access_key if a.access_key else "")

            else:
                new_attachment += str(a)

            new_attachment += ","

        attachment = new_attachment

    return await store.wrappers.request(
        "messages.send",
        message=message,
        peer_id=peer_id,
        attachment=attachment,
        sticker_id=sticker_id,
        payload=payload,
        keyboard=keyboard,
        forward_messages=forward_messages
    )


async def upload_file_to_vk(store, upload_url, data):
    async with aiohttp.ClientSession() as sess:
        upload_result_resp = await sess.post(
            upload_url, data=data
        )
        await sess.close()

    if not upload_result_resp:
        return None

    upload_result_text = await upload_result_resp.text()

    if not upload_result_text:
        return None

    try:
        upload_result = json.loads(upload_result_text)

        if "error" in upload_result:
            raise Exception

    except Exception:
        return None

    return upload_result


def make_reply(store, peer_id, custom_store):

    async def reply(message, attachment=None, sticker_id=None,
            payload=None, keyboard=None, forward_messages=None):

        if custom_store and 'custom_message' in custom_store:
            message = custom_store['custom_message']+message

        if len(message) > 4096:
            result = []

            for i in range(0, len(message), 4096):
                result.append(
                    await send_message(
                        store,
                        message[i : i + 4096],
                        peer_id,
                        attachment,
                        sticker_id,
                        payload,
                        keyboard,
                        forward_messages
                    )
                )

            return True

        await send_message(
            store,
            message,
            peer_id,
            attachment,
            sticker_id,
            payload,
            keyboard,
            forward_messages
        )
        return True

    return reply


def make_upload_docs(store, ori_peer_id):

    async def upload_doc(file, peer_id=None, group_id=None,
            doctype="doc", filename=None):

        if filename is None:
            filename = "file.png"

        if peer_id is None:
            peer_id = ori_peer_id

        if isinstance(file, str):
            with open(file, "rb") as o:
                file = o.read()

        if peer_id:
            upload_data = await store.wrappers.request(
                "docs.getMessagesUploadServer", peer_id=peer_id, type=doctype
            )

        else:
            upload_data = await store.wrappers.request(
                "docs.getWallUploadServer",
                group_id=group_id or store.config.group_id
            )

        if "upload_url" not in upload_data.response:
            return None

        upload_url = upload_data.response["upload_url"]

        data = aiohttp.FormData()
        data.add_field("file", file, filename=filename)

        upload_result = await upload_file_to_vk(store, upload_url, data)

        if not upload_result:
            return None

        attachments = await store.wrappers.request(
            "docs.save", **upload_result
        )

        if not 'response' in attachments:
            return None

        return convert_to_attachment(
            attachments.response[0], "doc"
        )

    return upload_doc


def make_upload_photo(store, ori_peer_id):
    """Creates uploading photo coroutine for controller and peer_id"""

    async def upload_photo(file, peer_id=None):
        if peer_id is None:
            peer_id = ori_peer_id

        if isinstance(file, str):
            with open(file, "rb") as o:
                file = o.read()


        upload_data = await store.wrappers.request(
            "photos.getMessagesUploadServer", peer_id=peer_id
        )

        if "upload_url" not in upload_data.response:
            return None

        upload_url = upload_data.response["upload_url"]

        data = aiohttp.FormData()
        data.add_field("photo", file, filename="image.png")

        upload_result = await upload_file_to_vk(store, upload_url, data)

        if not upload_result:
            return None

        attachments = await store.wrappers.request(
            "photos.saveMessagesPhoto", **upload_result
        )

        if not 'response' in attachments:
            return None

        return convert_to_attachment(
            attachments.response[0], "photo"
        )

    return upload_photo