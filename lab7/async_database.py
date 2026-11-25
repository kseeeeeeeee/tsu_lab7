import asyncio
import databases
import sqlalchemy


DATABASE_URL = "sqlite+aiosqlite:///lab7/async.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(100), nullable=False)
)

engine = sqlalchemy.create_engine(
    "sqlite:///lab7/async.db"
)

metadata.create_all(engine)


async def main():
    await database.connect()

    try:
        # Добавление пользователей
        query = users.insert().values(
            name="Иван Иванов",
            email="ivan@example.com"
        )
        await database.execute(query)

        query = users.insert().values(
            name="Анна Петрова",
            email="anna@example.com"
        )
        await database.execute(query)

        # Получение всех пользователей
        query = users.select()
        rows = await database.fetch_all(query)

        print("Список пользователей:")
        for row in rows:
            print(dict(row))

    finally:
        await database.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
