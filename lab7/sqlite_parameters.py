import sqlite3

conn = sqlite3.connect("lab7/company.db")
cursor = conn.cursor()

name = "Анна Петрова"

# Поиск сотрудника с использованием параметра
cursor.execute(
    "SELECT * FROM employees WHERE name = ?",
    (name,)
)

employee = cursor.fetchone()

if employee:
    print("Найден сотрудник:")
    print(employee)
else:
    print("Сотрудник не найден")

# Обновление должности с использованием параметров
cursor.execute(
    "UPDATE employees SET position = ? WHERE name = ?",
    ("Старший дизайнер", name)
)

conn.commit()

print("\nДанные после обновления:")
cursor.execute("SELECT * FROM employees")

for row in cursor.fetchall():
    print(row)

conn.close()
