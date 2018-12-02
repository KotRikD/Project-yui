## ProjectYui

> Асинхронный бот для ВКонтакте. Работает на python3.6+

![Sword Art Online персонаж Yui ;D](https://i.imgur.com/Ly0KpXw.jpg)

## Установка:

1. Устанавливаем зависимости `python3.6 -m pip install -r requirements.txt`
2. Редактируем конфиг. Только сначала не забудьте переименовать `config.json.sample`->`config.json`
3. Запускаем `python3.6 main.py`

## Плагины:

Как их писать? Что, где, откуда? Об этом можно узнать из `plugins/docs.py`

## Пример плагина:

```python
from common.Plugin import YPlugin

plugin = YPlugin(name="Эхо")

@plugin.on_command("эхо")
async def on_command(update, store):
    what_u_write = ' '.join(store.args)
    
    return await store.reply(f"Вы написали: {what_u_write}")
```

## Если возникли вопросы?

Можно написать [мне в личку,](https://vk.com/id311572436) помогу чем смогу ;D
