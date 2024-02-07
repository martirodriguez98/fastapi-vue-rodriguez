from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "notes" ADD "gen" VARCHAR(20);
        ALTER TABLE "notes" RENAME COLUMN "title" TO "patient_name";
        ALTER TABLE "notes" ADD "type" INT;
        ALTER TABLE "notes" DROP COLUMN "content";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "notes" RENAME COLUMN "patient_name" TO "title";
        ALTER TABLE "notes" ADD "content" TEXT NOT NULL;
        ALTER TABLE "notes" DROP COLUMN "gen";
        ALTER TABLE "notes" DROP COLUMN "type";"""
