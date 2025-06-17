from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from datetime import datetime
from models import Session, Crypto


def scrape_item_prices(url: str):
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Firefox()
    session = Session()  # Создаем объект сессии

    try:
        driver.get(url)

        element = driver.find_element(By.CSS_SELECTOR,
                                      'span.sc-65e7f566-0.esyGGG.base-text[data-test="text-cdp-price-display"]')

        # Удаляем символы '$' и ',' из строки
        price_clean = element.text.replace("$", "").replace(",", "")
        # Преобразуем строку в число с плавающей точкой
        price_float = float(price_clean)

        new_item = Crypto(name="BTC", timestamp=datetime.now(),
                          cost=price_float)  # Создаем новый объект пользователя
        session.add(new_item)  # Добавляем объект в сессию
        session.commit()  # Подтверждаем изменения, записывая их в базу данных

    finally:
        driver.quit()
        # Закрытие сессии
        session.close()
