import sqlite3

conn = sqlite3.connect("lab7/company.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        salary REAL NOT NULL
    )
""")

cursor.execute("DELETE FROM employees")

employees = [
    ("Иван Иванов", "Программист", 75000),
    ("Анна Петрова", "Дизайнер", 65000),
    ("Петр Сидоров", "Аналитик", 70000)
]

cursor.executemany(
    "INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)",
    employees
)

cursor.execute(
    "UPDATE employees SET salary = ? WHERE name = ?",
    (85000, "Иван Иванов")
)

conn.commit()

cursor.execute("SELECT * FROM employees")
print("Список сотрудников после обновления:")
for employee in cursor.fetchall():
    print(employee)

conn.close()
