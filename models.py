from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание базы
engine = create_engine("sqlite:///main.db", echo=True)  # Подключение к SQLite базе данных на диске
Base = declarative_base()  # Создание базового класса для моделей


# Определение модели
class Crypto(Base):
    __tablename__ = 'ctypto'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True)  # Первичный ключ
    name = Column(String)
    timestamp = Column(DateTime)
    cost = Column(Float)

    def __repr__(self):
        return f"<Crypto(name={self.name}, last_cost={self.cost})>"


# Создание таблиц в базе данных
Base.metadata.create_all(engine)  # Создает все таблицы, если они еще не существуют

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)  # Привязка сессии к engine
