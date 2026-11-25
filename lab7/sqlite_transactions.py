import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().with_name("bank.db")


def show_balances(cursor, title):
    cursor.execute("SELECT * FROM accounts ORDER BY id")
    print(f"\n{title}")
    for account in cursor.fetchall():
        print(account)


def main():
    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    cursor = conn.cursor()

    try:
        # Пересоздание таблицы с ограничением на баланс
        cursor.execute("DROP TABLE IF EXISTS accounts")

        cursor.execute("""
            CREATE TABLE accounts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                balance REAL NOT NULL CHECK (balance >= 0)
            )
        """)

        cursor.executemany(
            "INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)",
            [
                (1, "Иван", 10000),
                (2, "Анна", 5000)
            ]
        )

        show_balances(cursor, "Начальное состояние счетов:")

        # Первая транзакция: успешный перевод
        try:
            conn.execute("BEGIN")

            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (2000, 1)
            )

            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (2000, 2)
            )

            conn.commit()
            print("\nПервый перевод успешно выполнен.")

        except Exception as error:
            conn.rollback()
            print("\nОшибка первого перевода:", error)

        show_balances(cursor, "После успешного перевода:")

        # Запоминаем состояние перед неудачной транзакцией
        cursor.execute("SELECT * FROM accounts ORDER BY id")
        before_rollback = cursor.fetchall()

        # Вторая транзакция: недостаточно средств
        try:
            conn.execute("BEGIN")

            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (20000, 1)
            )

            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (20000, 2)
            )

            conn.commit()
            print("\nВторой перевод успешно выполнен.")

        except Exception as error:
            conn.rollback()
            print("\nВторой перевод отменён.")
            print("Причина ошибки:", error)

        show_balances(cursor, "Состояние счетов после rollback:")

        cursor.execute("SELECT * FROM accounts ORDER BY id")
        after_rollback = cursor.fetchall()

        if before_rollback == after_rollback:
            print("\nПроверка пройдена: rollback восстановил исходные балансы.")
        else:
            print("\nОшибка: состояние счетов изменилось!")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
