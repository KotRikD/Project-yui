import json
import io
import traceback
from common import Logger
from common.Store import store


'''
Укажи какие значения нужно портировать из конфига, для работы бота
Обычно это:

VKToken

UseDB
DBSettings

UseRedis
DBRedis

CoolDownDelay
NeedLogMessage

Prefixes

'''
need_values = [
    'VKToken',
    'UseDB',
    'DBSettings',
    'UseRedis',
    'DBRedis',
    'CoolDownDelay',
    'NeedLogMessage',
    'Prefixes'
]

def load_config():
    config = None
    try:
        file = io.open('config.json', 'r', encoding="utf-8")
        config = json.loads(file.read())
        file.close()
    except:
        traceback.print_exc()
        Logger.Elog("Произошла ошибка при открытии файла конфига!")
        exit()

    for var in need_values:
        vr = config.get(var, None)
        if vr == None:
            Logger.Elog(f"В конфиге не хватает значения {var} для работы бота")
            exit()

        store.config[var] = vr

    Logger.Nlog("Конфиг был загружен в хранилиище")