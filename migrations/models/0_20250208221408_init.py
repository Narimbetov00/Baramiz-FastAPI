from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "adverts" (
    "id" UUID NOT NULL PRIMARY KEY,
    "title" VARCHAR(150) NOT NULL,
    "file" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "link" VARCHAR(150) NOT NULL,
    "date" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "reviews" (
    "id" UUID NOT NULL PRIMARY KEY,
    "rating" INT NOT NULL,
    "text" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "routes" (
    "id" UUID NOT NULL PRIMARY KEY,
    "from_dan" VARCHAR(255) NOT NULL,
    "to_ga" VARCHAR(255) NOT NULL,
    "number" INT NOT NULL,
    "description" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "is_verified" BOOL NOT NULL DEFAULT False,
    "password_hash" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
