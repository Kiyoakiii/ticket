"""
Этот модуль содержит функции, генерирующие различные сообщения, используемые в билетном боте.
"""


import code_city


def reg() -> str:
    """
    Возвращает строку для приветствия пользователя и запроса направления отправления.
    """
    return "Вас приветствует бот мониторинга жд билетов. Выбирайте направление. Откуда:\n"


def to() -> str:
    """
    Возвращает строку с запросом выбора города прибытия.
    """
    return "Прибытие в город:"


def time(time_travel: str) -> str:
    """
    Возвращает строку с запросом выбора времени отправления.
    """
    return f"Выберите время отправления:\n{time_travel}"


def time_none(date_from: str) -> str:
    """
    Возвращает строку о том, что на указанную дату нет рейсов.
    """
    return f"На указанную дату: {date_from} рейсов нет. Пожалуйста, выберите другую"


def date() -> str:
    """
    Возвращает строку с запросом выбора даты отправления.
    """
    return "Выберите дату отправления:"


def time_departure(
        place_of_arrival: str,
        departure_place: str,
        arrival_date: str,
        time_from: str,
        seat_pass: str) -> str:
    """
    Возвращает строку с подтверждением выбранного времени и информацией о билете.
    """
    departure_place = departure_place.replace("-", "")
    return (
        f"Отлично! Теперь я сообщу вам, когда появится билет "
        f"{code_city.cities.get(departure_place)} - {code_city.cities.get(place_of_arrival)}\n"
        f"Полка: {seat_pass}\n{arrival_date}: {time_from}")


def ticket_is_ready(time_travel: str, ticket: str) -> str:
    """
    Возвращает строку о готовности билета.
    """
    return f"Билет на вашу поездку готов!\n{time_travel}\n{ticket}"


def cancel() -> str:
    """
    Возвращает строку остановки поиска.
    """
    return "Поиск остановлен"


def seat() -> str:
    """
    Возвращает строку с запросом номера полки.
    """
    return "Полка:"
