from .LoadConfig import load_config

async def check_admin(store, update, peer_id, uid):
    req = await store.request('messages.getConversationMembers', peer_id=update.peer_id, fields="sex,screen_name,nickname,invited_by")
    if not 'items' in req.response:
        return False

    for x in req.response['items']:
        if x['member_id'] == uid*-1:
            if 'is_admin' in x and x['is_admin']:
                return True

            return False

        if x['member_id'] == uid:
            if 'is_admin' in x and x['is_admin']:
                return True

            return False

    return False