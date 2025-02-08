import asyncio
from tortoise import Tortoise
from src.config import Config

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": Config.PG_DB,
                "host": Config.PG_HOST,
                "port": "5432",
                "user": Config.PG_USER,
                "password": Config.PG_PSW,
                "min_size": 1,
                "max_size": 5
            },
        }
    },
    "apps": {
        "models": {
            "models": ["src.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    print("✅ PostgreSQL bilan bog‘landi!")

async def close_db():
    await Tortoise.close_connections()

# Jupyter yoki FastAPI uchun
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(init_db())