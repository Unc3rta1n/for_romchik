from fastapi import FastAPI
from bs4 import BeautifulSoup
import aiohttp

from app.utils import logger
from app.schemas import DefaultResponse

app = FastAPI(
    debug=True,
    title="DOLBAEB DEVELOPMENT",
    version="2.2.8"
)


@app.get("/random")
async def random():
    """
    Получает случайный факт с сайта randstuff.ru.

    :return: DefaultResponse: Ответ с фактом или сообщением об ошибке.
    """
    try:
        logger.info(f"Get random fact")
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://randstuff.ru/fact/", timeout=aiohttp.ClientTimeout(total=10))
            if response.status != 200:
                logger.error(f"Status code from request: {response.status}")
                return DefaultResponse(error=True,
                                       message="Сервис вышел покурить",
                                       payload="Ромчик опять чето сломал")
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            fact_table = soup.find('table', class_='text')
            if not fact_table:
                return DefaultResponse(error=True,
                                       message="Сервис вернул 200, но факт не найден ватафак",
                                       payload="Ромчик опять чето сломал")

            fact_td = fact_table.find('td')
            if not fact_td:
                return DefaultResponse(error=True,
                                       message="Сервис вернул 200, но факт не найден ватафак",
                                       payload="Ромчик опять чето сломал")
            fact_text = fact_td.text.strip()
            logger.info(f"{fact_text = }")
            return DefaultResponse(error=False,
                                   message="OK",
                                   payload=fact_text)
    except Exception as error:
        logger.info(f"Error: {error}")
        return DefaultResponse(error=True,
                               message=str(error),
                               payload="Ромчик опять чето сломал")
