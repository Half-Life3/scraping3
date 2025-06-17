from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

from models import Crypto

engine = create_engine('sqlite:///main.db')

Session = sessionmaker(bind=engine)
session = Session()

# Запрос данных из таблицы Crypto
query = session.query(Crypto.timestamp, Crypto.cost).order_by(Crypto.timestamp)

# Извлекаем данные
results = query.all()


session.close()

# Разделяем результаты на отдельные списки для дальнейшей обработки
timestamps = [result.timestamp for result in results]
costs = [result.cost for result in results]

# Преобразуем timestamp в числовой формат для построения графика
timestamps_numeric = [datetime.timestamp(ts) for ts in timestamps]

plt.figure(figsize=(10, 6))
plt.plot(timestamps, costs, marker='o', linestyle='-', color='b')

plt.title('Изменение стоимости криптовалюты по времени')
plt.xlabel('Время')
plt.ylabel('Стоимость')
plt.grid(True)

# Форматирование оси X как даты
plt.gcf().autofmt_xdate()  # Автоматически наклоняет подписи дат
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Формат даты

plt.tight_layout()
plt.show()
