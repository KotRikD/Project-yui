from utils import check_admin
from common.Store import store as gstore

class ChatData:
    def __init__(self, cid, admin_id, items, users, groups):
        self.id = cid
        self.admin_id = admin_id
        self.users = users
        self.groups = groups
        self.items = items
        self.previous_users = []
        self.previous_items = []
        self.previous_groups = []

chats = {}

async def get_chat_data(update, store, peer_id, refresh=False):
    if not refresh and peer_id in chats:
        return chats[peer_id]

    req = await store.request('messages.getConversationMembers', peer_id=peer_id, fields="sex,screen_name,nickname, invited_by")
    if not 'items' in req.response:
        return None
    chat = req.response
    if 'groups' in chat:
        result = chat['groups']
    else:
        result = 0

    chat_id = int(peer_id) - int(2000000000)
    admin_id = await check_admin(store, update, peer_id, gstore.config.group_id)
    chat_data = ChatData(chat_id, admin_id, chat['items'], chat["profiles"], result)

    if peer_id in chats:
        chat_data.previous_items = chats[peer_id].items
        chat_data.previous_users = chats[peer_id].users
        chat_data.previous_groups = chats[peer_id].groups

    return chat_data

def create_refresh(message, store, peer_id):
    async def func():
        return await get_chat_data(message, store, peer_id, True)

    return func


async def call_chat_meta(store, update):
    if not update.is_multichat:
        store.meta_data = None
        store.meta_refresh = None
        return None

    if not await check_admin(store, update, update.peer_id, gstore.config.group_id):
        store.meta_data = None
        store.meta_refresh = None
        return None

    store.meta_data = await get_chat_data(update, store, update.peer_id)
    store.meta_refresh = create_refresh(update, store, update.peer_id)
    if update.raw_update['object'].get('action', 0) != 0:
        if update.raw_update['object']['action']['type'] == 'chat_invite_user' or update.raw_update['object']['action']['type'] == "chat_kick_user":
            await store.meta_refresh()

    return True