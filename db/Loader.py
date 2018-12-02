from common.Store import store
import asyncio

async def load():
    if store.config.get("UseDB", False):
        import peewee_async

        DBSettings = store.config.DBSettings
        driver = peewee_async.PostgresqlDatabase if DBSettings['DBDriver'] == "psql" else peewee_async.MySQLDatabase

        db = driver(
            DBSettings['DBName'],
            user=DBSettings['DBUser'],
            password=DBSettings['DBPassword'],
            host=DBSettings['DBHost'],
            port=DBSettings['DBPort']
        )

        manager = peewee_async.Manager(db)
        db.set_allow_sync(False)

        store.config.db = manager

        import db.Models

        created_model = db.Models.BaseModel.__subclasses__()
        for x in created_model:
            with manager.allow_sync():
                x.create_table(True)

    if store.config.get("UseRedis", False):
        import asyncio_redis
        loop = asyncio.get_event_loop()

        RedisSettings = store.config.DBRedis
        transport, protocol = await loop.create_connection(asyncio_redis.RedisProtocol,
                                                           RedisSettings['DBHost'],
                                                           RedisSettings['DBPort'])
        await protocol.auth(password=RedisSettings['DBPass'])
        await protocol.select(RedisSettings['DB'])

        store.config.redis = protocol

    return True