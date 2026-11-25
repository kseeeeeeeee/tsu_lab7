import sqlite3

conn = sqlite3.connect("lab7/bank.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        balance REAL NOT NULL
    )
""")

cursor.execute("DELETE FROM accounts")

cursor.executemany(
    "INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)",
    [
        (1, "Иван", 10000),
        (2, "Анна", 5000)
    ]
)

conn.commit()

try:
    # Начало транзакции
    conn.execute("BEGIN")

    # Перевод 2000 рублей от Ивана Анне
    cursor.execute(
        "UPDATE accounts SET balance = balance - ? WHERE id = ?",
        (2000, 1)
    )

    cursor.execute(
        "UPDATE accounts SET balance = balance + ? WHERE id = ?",
        (2000, 2)
    )

    conn.commit()
    print("Транзакция успешно выполнена.")

except sqlite3.Error as error:
    conn.rollback()
    print("Ошибка транзакции:", error)

# Вывод текущих балансов
cursor.execute("SELECT * FROM accounts")

print("\nСостояние счетов:")
for account in cursor.fetchall():
    print(account)

conn.close()
