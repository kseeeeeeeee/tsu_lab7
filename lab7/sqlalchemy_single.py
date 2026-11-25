from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    group: Mapped[str] = mapped_column(String(20), nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)


engine = create_engine("sqlite:///lab7/students.db", echo=False)

Base.metadata.create_all(engine)

with Session(engine) as session:
    students = [
        Student(name="Иван Иванов", group="221341", grade=5),
        Student(name="Анна Петрова", group="221341", grade=4),
        Student(name="Петр Сидоров", group="221341", grade=5)
    ]

    session.add_all(students)
    session.commit()

    print("Список студентов:")
    for student in session.query(Student).all():
        print(
            f"ID: {student.id}, "
            f"Имя: {student.name}, "
            f"Группа: {student.group}, "
            f"Оценка: {student.grade}"
        )
