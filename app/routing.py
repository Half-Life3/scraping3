from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
from datetime import datetime

from fastapi.responses import HTMLResponse

from models import Crypto
import plotly.express as px
import plotly.io as pio

# Подключение к существующей базе данных
engine = create_engine("sqlite:///main.db", echo=True)
Base = declarative_base()

# Создание сессии для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class CryptoBase(BaseModel):
    id: int
    name: str
    timestamp: datetime
    cost: float

    class Config:
        orm_mode = True  # Указываем, что модель может работать с объектами SQLAlchemy


app = FastAPI()


# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def plot_graph(db: Session = Depends(get_db)):
    # Извлечение данных из базы
    cryptos = db.query(Crypto).all()

    # Преобразование данных в формат для Plotly
    data = {
        "name": [crypto.name for crypto in cryptos],
        "timestamp": [crypto.timestamp for crypto in cryptos],
        "cost": [crypto.cost for crypto in cryptos]
    }

    # Создание графика с использованием Plotly
    fig = px.line(data, x="timestamp", y="cost", title="Cryptocurrency Cost Over Time",
                  labels={"cost": "Price (USD)", "timestamp": "Date"})

    # Конвертация графика в HTML
    graph_html = pio.to_html(fig, full_html=False)

    # Возвращаем HTML с графиком
    return graph_html

# Эндпоинт для фильтрации, сортировки и упорядочивания данных
@app.get("/cryptos/", response_class=HTMLResponse)
def get_cryptos(
        name: Optional[str] = None,
        min_cost: Optional[float] = None,
        max_cost: Optional[float] = None,
        sort_by: Optional[str] = Query('id', alias='sort'),
        order: Optional[str] = Query('asc', regex='^(asc|desc)$'),
        db: Session = Depends(get_db)
):
    query = db.query(Crypto)

    # Фильтрация по имени
    if name:
        query = query.filter(Crypto.name.ilike(f"%{name}%"))

    # Фильтрация по диапазону стоимости
    if min_cost:
        query = query.filter(Crypto.cost >= min_cost)
    if max_cost:
        query = query.filter(Crypto.cost <= max_cost)

    # Сортировка
    if order == 'asc':
        query = query.order_by(getattr(Crypto, sort_by).asc())
    else:
        query = query.order_by(getattr(Crypto, sort_by).desc())

    # Получаем все записи
    cryptos = query.all()

    # Преобразование данных в формат для Plotly
    data = {
        "name": [crypto.name for crypto in cryptos],
        "timestamp": [crypto.timestamp for crypto in cryptos],
        "cost": [crypto.cost for crypto in cryptos]
    }

    # Создание графика с использованием Plotly
    fig = px.line(data, x="timestamp", y="cost", title="Cryptocurrency Cost Over Time",
                  labels={"cost": "Price (USD)", "timestamp": "Date"})

    # Конвертация графика в HTML
    graph_html = pio.to_html(fig, full_html=False)

    # Возвращаем HTML с графиком
    return graph_html
